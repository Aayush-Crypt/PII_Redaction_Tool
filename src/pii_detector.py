import re
from dataclasses import dataclass
from typing import List

@dataclass(frozen=True)
class Entity:
    start:int; end:int; label:str; text:str; confidence:float=1.0

PATTERNS = {
 'EMAIL': re.compile(r'(?i)\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b'),
 'IP_ADDRESS': re.compile(r'(?<!\d)(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)(?!\d)'),
 'SSN': re.compile(r'(?<!\d)\d{3}-\d{2}-\d{4}(?!\d)'),
 'CREDIT_CARD': re.compile(r'(?<!\d)(?:\d[ -]*?){13,19}(?!\d)'),
 'PHONE': re.compile(r'(?<!\w)(?:\+?\d{1,3}[\s.-]?)?(?:\(?\d{2,4}\)?[\s.-]?)?\d{3,4}[\s.-]?\d{4}(?!\w)'),
 'DOB': re.compile(r'(?i)\b(?:date\s+of\s+birth|dob|born\s+on)\s*[:\-]?\s*((?:0?[1-9]|[12]\d|3[01])[-/.](?:0?[1-9]|1[0-2])[-/.](?:19|20)\d{2}|(?:19|20)\d{2}[-/.](?:0?[1-9]|1[0-2])[-/.](?:0?[1-9]|[12]\d|3[01])|(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|Jun(?:e)?|Jul(?:y)?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\s+\d{1,2},\s+(?:19|20)\d{2})'),
}
COMPANY = re.compile(r'(?i)\b(?:[A-Z][A-Za-z&.-]*(?:\s+[A-Z][A-Za-z&.-]*){0,7}\s+(?:Private\s+Limited|Public\s+Limited|Limited|Ltd\.?|LLP|Inc\.?|Corporation|Corp\.?|Bank))\b')
ADDRESS = re.compile(r'(?i)\b(?:plot\s+no\.?\s*[^;,.]{1,50}[,;]\s*)?(?:\d{1,4}[/-][\d/]+|\d{1,4})?\s*[A-Za-z0-9 .()/-]{3,80},\s*[A-Za-z .()-]{2,40},\s*[A-Za-z .()-]{2,40}\s*[-–]?\s*\d{6},\s*(?:Maharashtra|India)\b')
PERSON_CTX = re.compile(r'(?:(?i:contact\s+person|chairman|director|officer|promoter|secretary|ceo|cfo|being|namely))\s*[:,-]?\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})')

class PIIDetector:
    def __init__(self, use_spacy=True):
        self.nlp=None
        if use_spacy:
            try:
                import spacy
                self.nlp=spacy.load('en_core_web_sm')
            except Exception: pass
    def detect(self,text:str)->List[Entity]:
        out=[]
        for label,p in PATTERNS.items():
            for m in p.finditer(text):
                s,e=m.span(1) if label=='DOB' and m.lastindex else m.span()
                val=text[s:e]
                if label=='CREDIT_CARD' and not self._luhnish(val): continue
                if label=='PHONE' and len(re.sub(r'\D','',val))<10: continue
                out.append(Entity(s,e,label,val))
        for label,p in [('COMPANY',COMPANY),('ADDRESS',ADDRESS)]:
            for m in p.finditer(text):
                s,e=m.start(),m.end(); val=m.group()
                if label=='COMPANY':
                    lead=re.match(r'(?i)^(?:vendor|client|customer|issuer)\s+',val)
                    if lead: s+=lead.end(); val=text[s:e]
                out.append(Entity(s,e,label,val))
        for m in PERSON_CTX.finditer(text):
            s,e=m.span(1); out.append(Entity(s,e,'PERSON',text[s:e],.85))
        # Uppercase comma-separated person names, common in promoter/shareholder lists.
        for um in re.finditer(r'(?:(?<=:)|(?<=,))\s*([A-Z]{2,}(?:\s+[A-Z]{2,}){1,3})(?=\s*,|$)', text):
            val=um.group(1).strip()
            if not any(w in val for w in ('TRUST','LIMITED','PRIVATE','COMPANY','OFFER','SHAREHOLDER')):
                s0,e0=um.span(1); out.append(Entity(s0,e0,'PERSON',text[s0:e0],.7))
        # Leading person name followed by a corporate role (common in table cells).
        lm=re.match(r'^\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})\s+(?:Company Secretary|Compliance Officer|Director|Chief|CEO|CFO)', text)
        if lm:
            s0,e0=lm.span(1); out.append(Entity(s0,e0,'PERSON',text[s0:e0],.85))
        # Conservative standalone-name fallback for DOCX table cells where labels are in adjacent cells.
        stripped=text.strip()
        role_words={'company secretary','compliance officer','registered office','corporate office','red herring prospectus','book running lead managers','registrar to the offer','national stock exchange','reserve bank of india'}
        if re.fullmatch(r'[A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3}', stripped) and stripped.lower() not in role_words:
            pos=text.find(stripped); out.append(Entity(pos,pos+len(stripped),'PERSON',stripped,.65))
        # Mailing-address fallback: redact a complete address-like paragraph containing an Indian PIN code.
        if re.search(r'\b[1-9]\d{2}[ -]?\d{3}\b', text) and (',' in text or re.search(r'(?i)\b(?:road|street|village|taluka|tower|building|office|marg|nagar|pune|mumbai|maharashtra)\b',text)):
            out.append(Entity(0,len(text),'ADDRESS',text,.75))
        if self.nlp:
            for ent in self.nlp(text).ents:
                lab={'PERSON':'PERSON','ORG':'COMPANY'}.get(ent.label_)
                if lab: out.append(Entity(ent.start_char,ent.end_char,lab,ent.text,.8))
        return self._resolve(out)
    def _luhnish(self,s):
        ds=re.sub(r'\D','',s)
        if not 13<=len(ds)<=19:return False
        nums=list(map(int,ds[::-1])); total=sum(n if i%2==0 else (n*2 if n<5 else n*2-9) for i,n in enumerate(nums))
        return total%10==0
    def _resolve(self,ents):
        priority={'EMAIL':10,'IP_ADDRESS':9,'SSN':9,'CREDIT_CARD':9,'PHONE':8,'DOB':8,'ADDRESS':7,'COMPANY':6,'PERSON':5}
        chosen=[]
        for e in sorted(ents,key=lambda x:(x.start,-(x.end-x.start),-priority.get(x.label,0))):
            if any(not(e.end<=c.start or e.start>=c.end) for c in chosen): continue
            chosen.append(e)
        return sorted(chosen,key=lambda x:x.start)
