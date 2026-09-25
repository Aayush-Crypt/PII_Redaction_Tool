from src.pii_detector import PIIDetector

def test_required_types():
 d=PIIDetector(False)
 cases={
 'PERSON':'Contact Person: Rashi Patil','EMAIL':'rashi.patil@gmail.com','PHONE':'+91 9876543210',
 'COMPANY':'Acme Private Limited','DOB':'DOB: 12/04/1992','IP_ADDRESS':'192.168.1.20','SSN':'123-45-6789',
 'CREDIT_CARD':'4111 1111 1111 1111','ADDRESS':'Office 201, Tower 2, Baner, Pune, Maharashtra - 411045, India'}
 for label,text in cases.items(): assert label in {x.label for x in d.detect(text)}, (label,text,d.detect(text))
