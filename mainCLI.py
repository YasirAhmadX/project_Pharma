import mysql.connector
from datetime import datetime as dt
import hashlib
import pp
import firebase_admin
from firebase_admin import firestore
from firebase_admin import credentials

#CLOUD DATABASE
cred = credentials.Certificate("F:\Vaio\Code_Sheet\WorkLAB\ProjectPharma\SWengg_project\project-phrama-3d2d2a0fd6bc.json")
#initialize firebase
firebase_admin.initialize_app(cred)

db = firestore.client()

records = db.collection("pharmacy_records")

# Create a hash object using SHA-256 algorithm
hash_object = hashlib.sha256()
d = dt.now()

#LOCAL DATABASE
Host = 'localhost'
port = 3360
User = 'root'
Password = pp.pswd ;#input("User: root\nPassword: ")

Database = 'projectpharma'
TableName = 'sales'

cols = []

DB = mysql.connector.connect(host=Host,port=port,user=User,passwd=Password,database=Database)
Csr = DB.cursor()

################################################
name = input("Enter customer name: ")
state = input("Enter state: ")
drugs = input("Drugs: ")
qnty = input("Quantity of each drug: ")
total = float(input("Enter total: "))
t = (name,drugs,qnty,total,d.date(),str(d.time()))


query = "insert into "+TableName+"(Cust_name,Drugs,Quantity,total,saleDate,saleTime) values(%s,%s,%s,%s,%s,%s);"

Csr.execute(query,t)
DB.commit()
query='select * from '+ TableName + ' where Cust_name = \'' + name + "\';"
Csr.execute(query)
Response=Csr.fetchall()
if Response==[]:
    print('Message from Yasir','Operation Failed!\nData not submitted sucessfully! ')
else:
    print('Message from Yasir','Data has been submitted sucessfully! ')
    print(Response)


s = str(d.date()) + name
hash_object.update(bytes(s,"UTF-8"))

# Get the hexadecimal digest of the hash
hex_dig = hash_object.hexdigest()
print(hex_dig)

records.document(hex_dig).set({
    'Drugs': drugs.split(","),
    'Quantity': qnty.split(","),
    'State': state,
    'Date': str(d.date())
    })



