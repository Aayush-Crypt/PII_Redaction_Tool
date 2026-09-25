import hashlib,re
from .pii_detector import Entity
FIRST=['Aarav','Diya','Kabir','Myra','Vivaan','Tara','Reyansh','Kiara','Aditya','Saanvi']
LAST=['Bansal','Desai','Khanna','Menon','Pillai','Saxena','Chawla','Reddy','Bose','Kulkarni']
COMP=['Silverline Components Limited','Orchid Data Systems Private Limited','Cedarstone Ventures Limited','Vertex Manufacturing Limited']
CITIES=['Lucknow','Vadodara','Nashik','Coimbatore']
class Anonymizer:
 def __init__(self,salt='pii-redaction-v1'): self.salt=salt; self.map={}
 def _idx(self,s,n): return int(hashlib.sha256((self.salt+s.lower()).encode()).hexdigest()[:12],16)%n
 def fake(self,e:Entity):
  key=(e.label,e.text.lower())
  if key in self.map:return self.map[key]
  i=self._idx(e.text,10000)
  if e.label=='PERSON': v=f'{FIRST[i%len(FIRST)]} {LAST[(i//7)%len(LAST)]}'
  elif e.label=='EMAIL': v=f'{FIRST[i%10].lower()}.{LAST[(i//7)%10].lower()}@example.com'
  elif e.label=='PHONE': v='+91 98%08d'%(i*7919%100000000)
  elif e.label=='COMPANY': v=COMP[i%len(COMP)]
  elif e.label=='ADDRESS': v=f'{100+i%899}, Lakeview Road, {CITIES[i%4]} - {300000+i%699999}, India'
  elif e.label=='SSN': v='888-%02d-%04d'%(i%100,i%10000)
  elif e.label=='CREDIT_CARD': v='5555 5555 5555 4444'
  elif e.label=='DOB': v='%02d/%02d/%04d'%(1+i%28,1+(i//3)%12,1970+i%30)
  elif e.label=='IP_ADDRESS': v=f'198.51.100.{1+i%253}'
  else:v='[REDACTED]'
  self.map[key]=v; return v
 def replace(self,text,entities):
  for e in sorted(entities,key=lambda x:x.start,reverse=True): text=text[:e.start]+self.fake(e)+text[e.end:]
  return text
