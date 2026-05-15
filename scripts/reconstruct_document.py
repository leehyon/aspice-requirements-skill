#!/usr/bin/env python3
"""Reconstruct one document or a directory of extracted customer requirement documents.
Supported input: .txt, .md, .markdown file or directory. This script does not generate CRS, SRS, or SWRS.
"""
from __future__ import annotations
import argparse, json, re
from collections import Counter
from dataclasses import dataclass, asdict
from datetime import date
from pathlib import Path
from typing import List

SUPPORTED_SUFFIXES={'.txt','.md','.markdown'}
EXCLUDE_DIRS={'.git','node_modules','__pycache__','reconstruct-output','preprocess-output'}
DOMAINS={'Diagnostics':['diagnostic','uds','dtc','did','obd','negative response','service 0x'],'Communication':['communication','can','lin','ethernet','flexray','signal','message','pdu'],'Interfaces':['interface','input','output','connector','api','port'],'Safety':['safety','asil','safe state','hazard','fault reaction','fail-safe'],'Security':['security','cybersecurity','authentication','encryption','secure','crypto'],'Calibration and Configuration':['calibration','calibratable','configuration','configurable','variant','coding','parameter'],'Timing and Performance':['timing','timeout','response time','latency','period','cycle','deadline','performance'],'Data and Error Handling':['data','invalid','error','fault','fallback','range','value'],'Verification':['verification','validation','test','acceptance criteria']}
REQ_CUES=['shall','must','is required to','are required to','has to','have to','should','may','supports','support','provides','provide','enables','enable']
AMB=['fast','suitable','appropriate','user-friendly','robust','optimized','as needed','sufficient','easy','minimal','normal condition','if possible','where applicable']

@dataclass
class SectionInfo:
    section_id:str; document_id:str; number:str; title:str; level:int; start_line:int; end_line:int; domains:List[str]; potential_requirement_region:bool; warnings:List[str]
@dataclass
class DocumentModel:
    document_id:str; source_file:str; relative_path:str; extraction_tool:str; reconstruction_date:str; extraction_quality:str; title:str; outline:List[dict]; section_groups:dict; potential_requirement_regions:List[dict]; table_or_structured_regions:List[dict]; extraction_warnings:List[str]

def normalize(text):
    text=text.replace('\r\n','\n').replace('\r','\n'); text=re.sub(r'[\t\u00a0]+',' ',text); text=re.sub(r'\n{4,}','\n\n\n',text)
    return '\n'.join(x.rstrip() for x in text.split('\n')).strip()+'\n'
def collect(path:Path, recursive=True):
    if path.is_file():
        if path.suffix.lower() not in SUPPORTED_SUFFIXES: raise ValueError(f'Unsupported suffix {path.suffix}')
        return [path]
    if not path.is_dir(): raise FileNotFoundError(path)
    it=path.rglob('*') if recursive else path.glob('*')
    return sorted([p for p in it if p.is_file() and p.suffix.lower() in SUPPORTED_SUFFIXES and not any(part in EXCLUDE_DIRS for part in p.parts)], key=lambda p:p.as_posix().lower())
def is_heading(line):
    s=line.strip()
    if not s: return None
    m=re.match(r'^(#{1,6})\s+(.+)$',s)
    if m:
        raw=m.group(2).strip(); n=re.match(r'^([0-9]+(?:\.[0-9]+)*\.?)\s+(.+)$',raw)
        return (n.group(1).rstrip('.'),n.group(2).strip(),len(m.group(1))) if n else ('N/A',raw,len(m.group(1)))
    n=re.match(r'^([0-9]+(?:\.[0-9]+)*\.?)\s+([A-Z][A-Za-z0-9][^\.]{2,120})$',s)
    if n:
        num=n.group(1).rstrip('.'); return num,n.group(2).strip(),num.count('.')+1
    if len(s)<=80 and s.isupper() and len(s.split())<=10: return 'N/A',s.title(),1
    return None
def table(line):
    s=line.strip(); return bool(s and (s.count('|')>=2 or re.search(r'\S\s{2,}\S\s{2,}\S',s)))
def list_or_id(line): return bool(re.match(r'^([-*•]|\d+[.)]|[A-Z]{2,}-?\d+[:.)])\s+',line.strip()))
def sentence_end(line): return bool(re.search(r'[.!?;:]$',line.strip()))
def repair(lines):
    out=[]; i=0
    while i<len(lines):
        cur=lines[i].rstrip()
        if not cur.strip() or is_heading(cur) or table(cur) or list_or_id(cur): out.append(cur); i+=1; continue
        while i+1<len(lines):
            nxt=lines[i+1].rstrip()
            if not nxt.strip() or is_heading(nxt) or table(nxt) or list_or_id(nxt) or sentence_end(cur): break
            if (len(cur)<120 and re.match(r'^[a-z,(]',nxt.strip())) or (len(cur)>=40 and re.match(r'^[A-Za-z0-9]',nxt.strip())):
                cur=cur+' '+nxt.strip(); i+=1; continue
            break
        out.append(cur); i+=1
    return out
def remove_repeated(lines,min_count=3):
    c=Counter([l.strip() for l in lines if 0<len(l.strip())<=80]); rep={t for t,n in c.items() if n>=min_count and not is_heading(t) and not list_or_id(t)}
    warnings=[]; out=[]; removed=Counter()
    for l in lines:
        if l.strip() in rep: removed[l.strip()]+=1
        else: out.append(l)
    for t,n in removed.items(): warnings.append(f"Removed repeated possible header/footer '{t}' ({n} occurrences).")
    return out,warnings
def has_req(text):
    low=text.lower(); return any(re.search(r'\b'+re.escape(c)+r'\b',low) for c in REQ_CUES)
def domains(text):
    low=text.lower(); ds=[d for d,ks in DOMAINS.items() if any(k in low for k in ks)]
    return ds or ['Unknown']
def detect_sections(lines,docid):
    pos=[]
    for i,l in enumerate(lines):
        h=is_heading(l)
        if h: pos.append((i,*h))
    if not pos:
        text='\n'.join(lines); return [SectionInfo(f'{docid}-SEC-0001',docid,'N/A','Unstructured Document',1,0,len(lines),domains(text),has_req(text),['No explicit headings detected.'])]
    secs=[]
    for idx,(start,num,title,level) in enumerate(pos):
        end=pos[idx+1][0] if idx+1<len(pos) else len(lines); body='\n'.join(lines[start:end]); warns=[]
        if any(table(l) for l in lines[start:end]): warns.append('Contains table-like content; verify structure if requirements depend on table values.')
        secs.append(SectionInfo(f'{docid}-SEC-{len(secs)+1:04d}',docid,num,title,level,start,end,domains(title+'\n'+body),has_req(body),warns))
    return secs
def quality(lines,warns):
    non=[l for l in lines if l.strip()]
    if not non: return 'Poor'
    short=sum(1 for l in non if len(l.strip())<25)/len(non); tr=sum(1 for l in non if table(l))/len(non)
    return 'Poor' if len(warns)>10 or short>.65 else ('Partial' if len(warns)>3 or tr>.2 or short>.45 else 'Good')
def model_for(docid,file,rel,tool,lines,secs,warns):
    title=next((s.title for s in secs if s.title!='Unstructured Document'),file.stem); outline=[{'section_id':s.section_id,'document_id':docid,'number':s.number,'title':s.title,'level':s.level,'domains':s.domains} for s in secs]
    groups={}; potential=[]; tables=[]
    for s in secs:
        for d in s.domains: groups.setdefault(d,[]).append({'document_id':docid,'section_id':s.section_id,'number':s.number,'title':s.title})
        if s.potential_requirement_region: potential.append({'document_id':docid,'section_id':s.section_id,'number':s.number,'title':s.title,'domains':s.domains})
        if any(table(l) for l in lines[s.start_line:s.end_line]): tables.append({'document_id':docid,'section_id':s.section_id,'title':s.title,'note':'Table-like content detected.'})
        for w in s.warnings: warns.append(f'{s.section_id} {s.title}: {w}')
    amb=[w for w in AMB if w in '\n'.join(lines).lower()]
    if amb: warns.append('Ambiguous wording found: '+', '.join(sorted(set(amb)))+'.')
    return DocumentModel(docid,file.name,rel,tool,date.today().isoformat(),quality(lines,warns),title,outline,groups,potential,tables,warns)
def write_doc_md(path,model):
    lines=['# Document Analysis Model','','## Document Metadata','',f'- Document ID: `{model.document_id}`',f'- Document Title: `{model.title}`',f'- Source File: `{model.source_file}`',f'- Relative Path: `{model.relative_path}`',f'- Extraction Quality: `{model.extraction_quality}`','','## High-Level Outline','']
    for it in model.outline:
        indent='  '*(max(it['level']-1,0)); num='' if it['number']=='N/A' else it['number']; lines.append(f"{indent}- `{it['section_id']}` {num} {it['title']} — {', '.join(it['domains'])}")
    lines+=['','## Extraction Warnings','']+([f'- {w}' for w in model.extraction_warnings] if model.extraction_warnings else ['- None.']); path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
def safe(s): return re.sub(r'[^A-Za-z0-9_.-]+','_',s)[:80]
def process(file,base,out,docid,tool,rm):
    lines=normalize(file.read_text(encoding='utf-8',errors='replace')).splitlines(); warns=[]
    if rm:
        lines,w=remove_repeated(lines); warns+=w
    lines=repair(lines); secs=detect_sections(lines,docid); rel=file.relative_to(base).as_posix() if file.is_relative_to(base) else file.name; m=model_for(docid,file,rel,tool,lines,secs,warns)
    folder=out/'documents'/docid; folder.mkdir(parents=True,exist_ok=True); rec=folder/f'{docid}_{safe(file.stem)}_reconstructed.md'; rec.write_text('\n'.join(lines).strip()+'\n',encoding='utf-8')
    (folder/'document_model.json').write_text(json.dumps(asdict(m),ensure_ascii=False,indent=2),encoding='utf-8'); write_doc_md(folder/'document_model.md',m)
    return {'document_id':docid,'file':file.name,'relative_path':rel,'title':m.title,'quality':m.extraction_quality,'domains':sorted({d for x in m.outline for d in x['domains']}),'potential_requirement_regions':len(m.potential_requirement_regions),'reconstructed_reference':rec.as_posix(),'model_reference':(folder/'document_model.md').as_posix()},m
def write_registry(path,docs):
    lines=['# Source Document Registry','','| Document ID | File | Relative Path | Title | Quality | Domains | Potential Requirement Regions |','|---|---|---|---|---|---|---:|']
    for d in docs: lines.append(f"| {d['document_id']} | {d['file']} | {d['relative_path']} | {d['title']} | {d['quality']} | {', '.join(d['domains'])} | {d['potential_requirement_regions']} |")
    path.write_text('\n'.join(lines)+'\n',encoding='utf-8')
def write_combined(out,portfolio):
    lines=['# Combined Document Analysis Model','','## Portfolio Metadata','',f"- Portfolio ID: `{portfolio['portfolio_id']}`",f"- Input Path: `{portfolio['input_path']}`",f"- Document Count: `{portfolio['document_count']}`",'','## Source Documents','']
    for d in portfolio['documents']: lines.append(f"- `{d['document_id']}` {d['relative_path']} — {d['title']} — Quality: `{d['quality']}`")
    lines+=['','## Domain Index','']
    for dom,secs in portfolio['domain_index'].items():
        lines.append(f'### {dom}')
        for s in secs: lines.append(f"- `{s['document_id']}` / `{s['section_id']}` {s.get('number','')} {s['title']}")
        lines.append('')
    lines+=['## Potential Requirement Regions','']
    for r in portfolio['potential_requirement_regions']: lines.append(f"- `{r['document_id']}` / `{r['section_id']}` {r.get('number','')} {r['title']} — {', '.join(r['domains'])}")
    lines+=['','## Extraction Warnings','']+([f'- {w}' for w in portfolio['extraction_warnings']] if portfolio['extraction_warnings'] else ['- None.']); (out/'combined_document_model.md').write_text('\n'.join(lines)+'\n',encoding='utf-8'); (out/'combined_document_model.json').write_text(json.dumps(portfolio,ensure_ascii=False,indent=2),encoding='utf-8')
def write_brief(out,portfolio):
    domains=[d for d in portfolio['domain_index'] if d!='Unknown'] or ['Unknown']; lines=['# Global Requirement Brief','','## 1. Document Purpose','TBD based on the source document set.','','## 2. Scope and System Context','TBD.','','## 3. Source Document Set','']
    for d in portfolio['documents']: lines.append(f"- `{d['document_id']}` {d['relative_path']} — {d['title']}")
    lines+=['','## 4. Main Requirement Domains','']+[f'- {d}' for d in domains]+['','## 5. Relevant Sections and Source Areas','']
    for r in portfolio['potential_requirement_regions'][:80]: lines.append(f"- `{r['document_id']}` / `{r['section_id']}` {r.get('number','')} {r['title']} — {', '.join(r['domains'])}")
    lines+=['','## 6. Terminology and Abbreviations','TBD.','','## 7. Key Assumptions','- Do not invent missing thresholds, units, interfaces, safety assumptions, or security assumptions.','','## 8. Extraction Quality Notes','TBD from extraction warnings.','','## 9. Duplicate, Overlap, and Conflict Risks','TBD during CRS extraction.','','## 10. Major Open Questions','TBD.','','## 11. Recommended Derivation Strategy','- Extract CRS Working Set by domain across all source documents.','- Preserve source document IDs in CRS source references.','- Consolidate duplicates and flag conflicts.','- Derive one coherent SRS and SWRS unless module-specific outputs are requested.']; (out/'global_requirement_brief_skeleton.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('input',type=Path); ap.add_argument('--out',type=Path,default=Path('reconstruct-output')); ap.add_argument('--document-id-prefix',default='SRC'); ap.add_argument('--document-id'); ap.add_argument('--portfolio-id',default='REQ-PORTFOLIO-0001'); ap.add_argument('--extraction-tool',default='manual-or-extracted-text'); ap.add_argument('--remove-repeated',action='store_true'); ap.add_argument('--no-recursive',action='store_true')
    a=ap.parse_args(); files=collect(a.input,not a.no_recursive)
    if not files: raise FileNotFoundError(f'No supported files found under: {a.input}')
    a.out.mkdir(parents=True,exist_ok=True); base=a.input if a.input.is_dir() else a.input.parent; docs=[]; models=[]
    for i,f in enumerate(files,1):
        docid=a.document_id if len(files)==1 and a.document_id else f'{a.document_id_prefix}-{i:04d}'; d,m=process(f,base,a.out,docid,a.extraction_tool,a.remove_repeated); docs.append(d); models.append(m)
    domain_index={}; potential=[]; warnings=[]
    for d,m in zip(docs,models):
        for dom,secs in m.section_groups.items(): domain_index.setdefault(dom,[]).extend(secs)
        potential.extend(m.potential_requirement_regions); warnings += [f"{d['document_id']}: {w}" for w in m.extraction_warnings]
    portfolio={'portfolio_id':a.portfolio_id,'reconstruction_date':date.today().isoformat(),'input_path':a.input.as_posix(),'document_count':len(docs),'documents':docs,'domain_index':domain_index,'potential_requirement_regions':potential,'extraction_warnings':warnings}
    write_registry(a.out/'source_document_registry.md',docs); write_combined(a.out,portfolio); write_brief(a.out,portfolio); (a.out/'extraction_warnings.md').write_text('# Extraction Warnings\n\n'+('\n'.join(f'- {w}' for w in warnings) if warnings else '- None.')+'\n',encoding='utf-8')
    print(f'Reconstruction complete: {a.out}'); print(f'Documents: {len(docs)} | Potential requirement regions: {len(potential)}')
if __name__=='__main__': main()
