from collections import defaultdict
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.pii_detector import PIIDetector
from evaluation.synthetic_tabular import ROWS, gold_for_row

detector=PIIDetector(False)
tp=fp=fn=0
per=defaultdict(lambda:[0,0,0])
cell_ok=0; cells=0; record_ok=0
failures=[]
fields=['company','address','contact','email','phone','dob','ssn','card','ip','record_id','website']
for r in ROWS:
    goldmap=gold_for_row(r); rec_good=True
    for field in fields:
        text=r[field]
        pred={(e.label,e.text) for e in detector.detect(text)}
        gold=set(goldmap[field])
        hits=pred&gold; extras=pred-gold; misses=gold-pred
        tp+=len(hits); fp+=len(extras); fn+=len(misses); cells+=1
        if pred==gold: cell_ok+=1
        else:
            rec_good=False
            if len(failures)<30: failures.append({'record_id':r['record_id'],'field':field,'text':text,'gold':sorted(gold),'pred':sorted(pred)})
        for label,_ in hits: per[label][0]+=1
        for label,_ in extras: per[label][1]+=1
        for label,_ in misses: per[label][2]+=1
    record_ok += rec_good
precision=tp/(tp+fp) if tp+fp else 0
recall=tp/(tp+fn) if tp+fn else 0
f1=2*precision*recall/(precision+recall) if precision+recall else 0
cell_accuracy=cell_ok/cells
record_accuracy=record_ok/len(ROWS)
result={'records':len(ROWS),'cells':cells,'tp':tp,'fp':fp,'fn':fn,'precision':precision,'recall':recall,'f1':f1,'cell_accuracy':cell_accuracy,'record_accuracy':record_accuracy,'per_category':{},'sample_failures':failures}
for label in sorted(per):
    a,b,c=per[label]; p=a/(a+b) if a+b else 0; rr=a/(a+c) if a+c else 0; ff=2*p*rr/(p+rr) if p+rr else 0
    result['per_category'][label]={'tp':a,'fp':b,'fn':c,'precision':p,'recall':rr,'f1':ff}
out=os.path.join(os.path.dirname(__file__),'synthetic_results.json')
with open(out,'w') as f: json.dump(result,f,indent=2)
print(json.dumps(result,indent=2))
