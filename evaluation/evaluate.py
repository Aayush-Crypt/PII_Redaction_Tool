from src.pii_detector import PIIDetector
CASES=[
('Contact Person: Rashi Patil', [('PERSON','Rashi Patil')]),
('Email rashi.patil@gmail.com', [('EMAIL','rashi.patil@gmail.com')]),
('Call +91 9876543210 now', [('PHONE','+91 9876543210')]),
('Vendor Acme Private Limited approved', [('COMPANY','Acme Private Limited')]),
('Office 201, Tower 2, Baner, Pune, Maharashtra - 411045, India', [('ADDRESS','Office 201, Tower 2, Baner, Pune, Maharashtra - 411045, India')]),
('DOB: 12/04/1992', [('DOB','12/04/1992')]),
('Host 192.168.1.20 responded', [('IP_ADDRESS','192.168.1.20')]),
('SSN 123-45-6789', [('SSN','123-45-6789')]),
('Card 4111 1111 1111 1111', [('CREDIT_CARD','4111 1111 1111 1111')]),
('Order 12345 is ready', []),('Ticket 98765 is closed',[])
]
d=PIIDetector(False);tp=fp=fn=0; rows=[]
for text,gold in CASES:
 pred={(x.label,x.text) for x in d.detect(text)}; gold=set(gold)
 tp+=len(pred&gold);fp+=len(pred-gold);fn+=len(gold-pred);rows.append((text,gold,pred))
precision=tp/(tp+fp) if tp+fp else 0; recall=tp/(tp+fn) if tp+fn else 0; f1=2*precision*recall/(precision+recall) if precision+recall else 0
accuracy=sum(set(g)==set(p) for _,g,p in rows)/len(rows)
print(f'TP={tp} FP={fp} FN={fn}\nPrecision={precision:.3f}\nRecall={recall:.3f}\nF1={f1:.3f}\nCaseAccuracy={accuracy:.3f}')
