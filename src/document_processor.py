from docx import Document
from .pii_detector import PIIDetector
from .anonymizer import Anonymizer

def _paragraphs(doc):
 for p in doc.paragraphs: yield p
 for table in doc.tables:
  for row in table.rows:
   for cell in row.cells:
    for p in cell.paragraphs: yield p
 for sec in doc.sections:
  for part in (sec.header,sec.footer):
   for p in part.paragraphs: yield p
   for table in part.tables:
    for row in table.rows:
     for cell in row.cells:
      for p in cell.paragraphs: yield p

def redact_docx(src,dst,use_spacy=True):
 doc=Document(src); det=PIIDetector(use_spacy); anon=Anonymizer(); stats={}
 seen=set()
 for p in _paragraphs(doc):
  if p._p in seen: continue
  seen.add(p._p); text=p.text
  if not text: continue
  ents=det.detect(text)
  if not ents: continue
  new=anon.replace(text,ents)
  # paragraph-level replacement is reliable; first run retains dominant formatting
  if p.runs:
   p.runs[0].text=new
   for r in p.runs[1:]: r.text=''
  else:p.add_run(new)
  for e in ents: stats[e.label]=stats.get(e.label,0)+1
 doc.save(dst)
 return stats,anon.map
