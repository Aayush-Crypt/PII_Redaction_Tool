import argparse,json
from .document_processor import redact_docx
p=argparse.ArgumentParser(description='Hybrid PII anonymizer for DOCX files')
p.add_argument('input');p.add_argument('output');p.add_argument('--no-spacy',action='store_true');p.add_argument('--report',default='redaction_run.json')
a=p.parse_args(); stats,mapping=redact_docx(a.input,a.output,not a.no_spacy)
with open(a.report,'w',encoding='utf8') as f: json.dump({'counts':stats,'unique_replacements':len(mapping)},f,indent=2)
print(json.dumps(stats,indent=2))
