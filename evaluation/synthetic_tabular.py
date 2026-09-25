from itertools import cycle

FIRST = ['Aarav','Ananya','Rohan','Priya','Vikram','Meera','Kabir','Ishita','Arjun','Neha','Siddharth','Kavya','Rahul','Nisha','Dev','Tanvi','Aditya','Pooja','Karan','Riya']
LAST = ['Sharma','Sen','Dey','Nair','Rao','Kapoor','Mehta','Iyer','Verma','Joshi','Malhotra','Patel','Gupta','Kulkarni','Singh','Bose','Agarwal','Menon','Desai','Reddy']
COMPANIES = ['Asterline Technologies Limited','Northstar Analytics Private Limited','Meridian Data Systems Limited','BlueRiver Solutions Private Limited','OrbitWorks Consulting LLP','Pinnacle Infra Private Limited','Vertex Digital Limited','SilverOak Finance Limited','Crestview Logistics Private Limited','Nimbus Research LLP']
CITIES = [('Pune','Maharashtra','411045'),('Mumbai','Maharashtra','400051'),('Bengaluru','Karnataka','560001'),('Hyderabad','Telangana','500081'),('Chennai','Tamil Nadu','600096'),('Delhi','Delhi','110001'),('Noida','Uttar Pradesh','201301'),('Gurugram','Haryana','122002'),('Kolkata','West Bengal','700091'),('Ahmedabad','Gujarat','380015')]
STREETS = ['MG Road','Park Street','Baner Road','Link Road','Residency Road','Station Road','Ring Road','Lake View Road','Industrial Area','Tech Park Road']
VALID_CARDS = ['4111 1111 1111 1111','5555 5555 5555 4444','4012 8888 8888 1881','4539 1488 0343 6467','6011 1111 1111 1117']

ROWS=[]
for i in range(1,101):
    first=FIRST[(i-1)%len(FIRST)]; last=LAST[(i*3-1)%len(LAST)]
    full=f'{first} {last}'
    # Deliberately vary some person formats to challenge conservative name rules.
    contact = full if i%10 not in (0,7) else (f'{first[0]}. {last}' if i%10==7 else first)
    company=COMPANIES[(i-1)%len(COMPANIES)]
    if i%12==0: company=company.replace('Private Limited','Pvt. Ltd.')
    city,state,pin=CITIES[(i-1)%len(CITIES)]
    address=f'{100+i}, {STREETS[(i-1)%len(STREETS)]}, {city}, {state} - {pin}, India'
    if i%15==0: address=f'Flat {i%9+1}B, {20+i} {STREETS[(i+2)%len(STREETS)]}, {city} {pin}, {state}, India'
    email=f'{first.lower()}.{last.lower()}{i}@example{i%7+1}.com'
    phone=f'+91 {70+(i%20):02d}{100+i:03d} {4000+i:04d}'
    dob=f'DOB: {1980+(i%20):04d}-{(i%12)+1:02d}-{(i%27)+1:02d}'
    if i%11==0: dob=f'{(i%27)+1:02d}/{(i%12)+1:02d}/{1980+(i%20):04d}'  # unlabeled date: intentional hard case
    ssn=f'{100+(i*7)%899:03d}-{10+(i*3)%89:02d}-{1000+(i*37)%8999:04d}'
    card=VALID_CARDS[(i-1)%len(VALID_CARDS)]
    ip=f'10.{i%250}.{(i*3)%250}.{(i*7)%250}'
    website=f'www.synthetic-company-{i}.example'
    ROWS.append({
        'record_id':f'R{i:03d}','company':company,'address':address,'contact':contact,
        'email':email,'phone':phone,'dob':dob,'ssn':ssn,'card':card,'ip':ip,'website':website
    })

# Ground truth by cell. Website and record_id are intentionally non-PII for this assignment.
def gold_for_row(r):
    dob_value = r['dob'][5:] if r['dob'].startswith('DOB: ') else r['dob']
    return {
        'company':[('COMPANY',r['company'])],
        'address':[('ADDRESS',r['address'])],
        'contact':[('PERSON',r['contact'])],
        'email':[('EMAIL',r['email'])],
        'phone':[('PHONE',r['phone'])],
        'dob':[('DOB',dob_value)],
        'ssn':[('SSN',r['ssn'])],
        'card':[('CREDIT_CARD',r['card'])],
        'ip':[('IP_ADDRESS',r['ip'])],
        'record_id':[], 'website':[]
    }
