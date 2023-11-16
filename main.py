#from matplotlib import pyplot
from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox as msg
from math import *

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


def MainFrame():
    global window
    global c
    window=Tk()
    window.title('proj_pharma')
    window.geometry('500x550')
    window.minsize(420,450)
    window.configure(bg='#04002e')
    L0=Label(window,text='Project Pharma ',font=('Verdana',30,'bold'),bg='#04002e',fg = '#ff0000')
    L0.pack(side=TOP,fill='x')
    L0.bind('<Enter>',lambda x : L0.configure(fg='#ff9000'))
    L0.bind('<Leave>',lambda x : L0.configure(fg='#ff0000'))
    nf=Frame(window,bg='#04002e')
    nf.pack(side=BOTTOM,fill='x')
    L1=Label(nf,text='By Yasir Ahmad\n[ 22MIA1064 ]',font=('Courier',8,'normal'),bg='#04002e',fg='#ffffff')
    L1.pack(side=RIGHT)
    L1.bind('<Enter>',lambda x : L1.configure(fg='#ff0000'))
    L1.bind('<Leave>',lambda x : L1.configure(fg='#ffffff'))
    Menu()
    window.mainloop()

def ButtonGraphics(B,dTail):
    print(dTail)
    f=B['font'].split(' ')
    r=B['relief']
    if r=='flat':
        r=RAISED
        f[2]='bold'
        B['fg'] = "#ffff00"
    elif r=='raised':
        r=FLAT
        f[2]='normal'
        B['fg'] = "#ff0000"
    f=' '.join(f)
    B.configure(font=f,relief=r)

def Menu():

    def DataEntry():
        def EntryDone():
            DataEntryframe.destroy()
            Menu()
            pass
        
        def EnterData():
            [r,n,dr,q,t] = [E00.get(),E01.get(),E02.get(),E03.get(),E04.get()]
            #val = (r,n,d,q,t)
            #print("Entring data:",r,n,d,q,t)
            
            val = (int(r),n,dr,q,float(t),(d.date()),str(d.time()))
            print("Entring data:",val)    
            query = "insert into "+TableName+"(ID,Cust_name,Drugs,Quantity,total,saleDate,saleTime) values(%s,%s,%s,%s,%s,%s,%s);"

            Csr.execute(query,val)
            DB.commit()
            query='select * from '+ TableName + ' where Cust_name = \'' + n + "\';"
            Csr.execute(query)
            Response=Csr.fetchall()
            if Response==[]:
                msg.showinfo('Message from Yasir','Operation Failed!\nData not submitted sucessfully! ')
            else:
                msg.showinfo('Message from Yasir','Data has been submitted sucessfully! ')
                print(Response)


            s = str(d.date()) + n
            hash_object.update(bytes(s,"UTF-8"))

            # Get the hexadecimal digest of the hash
            hex_dig = hash_object.hexdigest()
            print(hex_dig)

            records.document(hex_dig).set({
                'Drugs': dr.split(","),
                'Quantity': q.split(","),
                'State': "Chennai",
                'Date': str(d.date())
                })


            msg.showinfo('Message from Yasir','Data Entered.')
            EntryDone()
            pass

        print('<Button Pressed> ',B0['text'])
        menuframe.destroy()
        DataEntryframe=Frame(window,bg='#04002e')
        DataEntryframe.pack()
        L000=Label(DataEntryframe,text="",width=10,height=3,bg='#04002e'); #spacer
        L001=Label(DataEntryframe,text="",width=10,height=3,bg='#04002e'); #spacer
        msg.showinfo('Message from Yasir','Enter the sales data')
        L00=Label(DataEntryframe,text='Enter ID: ',width=15,font=('Verdana',12,'normal'),activebackground='#04002e',activeforeground='#696969',bg='#000020',fg='#ff0000',relief=FLAT)
        L01=Label(DataEntryframe,text='Cust_Name: ',width=10,font=('Verdana',12,'normal'),activebackground='#04002e',activeforeground='#696969',bg='#000020',fg='#ff0000',relief=FLAT)
        L02=Label(DataEntryframe,text='Drugs: ',width=10,font=('Verdana',12,'normal'),activebackground='#04002e',activeforeground='#696969',bg='#000020',fg='#ff0000',relief=FLAT)
        L03=Label(DataEntryframe,text='Quantity: ',width=10,font=('Verdana',12,'normal'),activebackground='#04002e',activeforeground='#696969',bg='#000020',fg='#ff0000',relief=FLAT)
        L04=Label(DataEntryframe,text='Total Bill: ',width=10,font=('Verdana',12,'normal'),activebackground='#04002e',activeforeground='#696969',bg='#000020',fg='#ff0000',relief=FLAT)
        

        E00=Entry(DataEntryframe,width=15,bd=3)
        E01=Entry(DataEntryframe,width=15,bd=3)
        E02=Entry(DataEntryframe,width=15,bd=3)
        E03=Entry(DataEntryframe,width=15,bd=3)
        E04=Entry(DataEntryframe,width=15,bd=3)
        

        B00=Button(DataEntryframe,width=10,text='Enter Data',fg='Blue',command=EnterData)
        
        L000.grid(column=0,row=1)
        L00.grid(column=0,row=2)
        L001.grid(column=0,row=3)
        L01.grid(column=0,row=4)
        L02.grid(column=0,row=5)
        L03.grid(column=0,row=6)
        L04.grid(column=0,row=7)

        E00.grid(column=1,row=2)
        E01.grid(column=1,row=4)
        E02.grid(column=1,row=5)
        E03.grid(column=1,row=6)
        E04.grid(column=1,row=7)

        
        E00.grid(column=1,row=2)
        B00.grid(column=0,row=9)
        
        pass
    def DataView():

        def ViewDone():
            DataViewframe.destroy()
            Menu()
            pass
        def DataViewFethcer():
            r = E00.get()
            print("Fetch Data from ID:",r)
            query ='select * from '+ TableName + ' where ID' + ' = ' + r
            Csr.execute(query)
            response=Csr.fetchall()
            print(*response)   
            if response!=[]:
                [r,n,d,q,t,da,ti] = response[0]
                L01.configure(text='Patient Name: '+n,width=len(n)+20)
                L02.configure(text='Name of Drugs: '+d,width=len(d)+20)
                L03.configure(text='Quantity: '+str(q),width=len(q)+20)
                L04.configure(text='Total Bill: '+str(t),width=len(q)+20)
                L05.configure(text='Date: '+str(da),width=len(q)+20)
                L06.configure(text='Time: '+str(ti),width=len(q)+20)
                
            else:
                L01.configure(text='Patient Name: No Matching Data found',width= 2+ len('Name: No Matching Data found'))
                L02.configure(text='Name of Drugs: No Matching Data found',width= 2+ len('Gender: No Matching Data found'))
                L03.configure(text='Quantity: No Matching Data found',width= 2+ len('Age: No Matching Data found'))
                L04.configure(text='Total Bill: No Matching Data found',width= 2+ len('Age: No Matching Data found'))
                L05.configure(text='Date: No Matching Data found',width= 2+ len('Age: No Matching Data found'))
                L06.configure(text='Time: No Matching Data found',width= 2+ len('Age: No Matching Data found'))

            E00.destroy()
            L00.configure(text='ID: '+str(r),width=len(str(r))+4)
            B00.configure(text='Ok!',command=ViewDone)#or command ViewDone
            #B00.grid(column=0,row=8)
            pass

        print('<Button Pressed> ',B1['text'])
        menuframe.destroy()
        DataViewframe=Frame(window,bg='#04002e')
        DataViewframe.pack()
        L000=Label(DataViewframe,text="",width=10,height=3,bg='#04002e'); #spacer
        L001=Label(DataViewframe,text="",width=10,height=3,bg='#04002e'); #spacer
        msg.showinfo('Message from Yasir','Enter the ID of the required data')
        L00=Label(DataViewframe,text='Enter ID: ',width=15,font=('Verdana',12,'normal'),activebackground='#04002e',activeforeground='#696969',bg='#000020',fg='#ff0000',relief=FLAT)
        L01=Label(DataViewframe,text='Cust_Name: ',width=10,font=('Verdana',12,'normal'),activebackground='#04002e',activeforeground='#696969',bg='#000020',fg='#ff0000',relief=FLAT)
        L02=Label(DataViewframe,text='Drugs: ',width=10,font=('Verdana',12,'normal'),activebackground='#04002e',activeforeground='#696969',bg='#000020',fg='#ff0000',relief=FLAT)
        L03=Label(DataViewframe,text='Quantity: ',width=10,font=('Verdana',12,'normal'),activebackground='#04002e',activeforeground='#696969',bg='#000020',fg='#ff0000',relief=FLAT)
        L04=Label(DataViewframe,text='Total Bill: ',width=10,font=('Verdana',12,'normal'),activebackground='#04002e',activeforeground='#696969',bg='#000020',fg='#ff0000',relief=FLAT)
        L05=Label(DataViewframe,text='Date: ',width=10,font=('Verdana',12,'normal'),activebackground='#04002e',activeforeground='#696969',bg='#000020',fg='#ff0000',relief=FLAT)
        L06=Label(DataViewframe,text='Time: ',width=10,font=('Verdana',12,'normal'),activebackground='#04002e',activeforeground='#696969',bg='#000020',fg='#ff0000',relief=FLAT)


        E00=Entry(DataViewframe,width=10,bd=4)

        B00=Button(DataViewframe,text='Check',fg='Blue',command=DataViewFethcer)
        
        L000.grid(column=0,row=1)
        L00.grid(column=0,row=2)
        L001.grid(column=0,row=3)
        L01.grid(column=0,row=4)
        L02.grid(column=0,row=5)
        L03.grid(column=0,row=6)
        L04.grid(column=0,row=7)
        L05.grid(column=0,row=8)

        
        E00.grid(column=1,row=2)
        B00.grid(column=2,row=2)
        
        pass
    
    def ChangeCreds():
        print('<Button Pressed>',B2['text'])
        msg.showinfo('Message from Yasir','Place the JSON file of credentials in root folder.')
        pass
    def HelpDoc():
        print('<Button Pressed>',B3['text'])
        pass
    def exit():
        print('<Button Pressed>',B4['text'])
        try:
            #pyplot.close()
            pass
        except:
            pass
        window.destroy()


    menuframe=Frame(window,bg='#04002e')
    menuframe.pack()

    L0=Label(menuframe,text='MENU',font=('Verdana',30),bg='#04002e',fg = "#fff000")

    B0=Button(menuframe,text='Enter Data',command=DataEntry,width=30,font=('Verdana',12,'normal'),activebackground='#04002e',activeforeground='#696969',bg='#000020',fg='#ff0000',relief=FLAT)
    B1=Button(menuframe,text='View Data',command=DataView,width=30,font=('Verdana',12,'normal'),bg='#000020',activebackground='#04002e',activeforeground='#696969',fg='#ff0000',relief=FLAT)
    B2=Button(menuframe,text='Change Credentials',command=ChangeCreds,width=30,font=('Verdana',12,'normal'),bg='#000020',activebackground='#04002e',activeforeground='#696969',fg='#ff0000',relief=FLAT)
    B3=Button(menuframe,text='Help Docs',command=HelpDoc,width=30,font=('Verdana',12,'normal'),bg='#000020',activebackground='#04002e',activeforeground='#696969',fg='#ff0000',relief=FLAT)
    B4=Button(menuframe,text='Exit',command=exit,width=30,font=('Verdana',12,'normal'),bg='#000020',activebackground='#04002e',activeforeground='#696969',fg='#ff0000',relief=FLAT)

    L0.pack(pady=10)
    B0.pack(pady=3,ipady=5)
    B1.pack(pady=3,ipady=5)
    B2.pack(pady=3,ipady=5)
    B3.pack(pady=3,ipady=5)
    B4.pack(pady=3,ipady=5)


    B0.bind('<Enter>',lambda x: ButtonGraphics(B0,x))
    B1.bind('<Enter>',lambda x: ButtonGraphics(B1,x))
    B2.bind('<Enter>',lambda x: ButtonGraphics(B2,x))
    B3.bind('<Enter>',lambda x: ButtonGraphics(B3,x))
    B4.bind('<Enter>',lambda x: ButtonGraphics(B4,x))


    B0.bind('<Leave>',lambda x: ButtonGraphics(B0,x))
    B1.bind('<Leave>',lambda x: ButtonGraphics(B1,x))
    B2.bind('<Leave>',lambda x: ButtonGraphics(B2,x))
    B3.bind('<Leave>',lambda x: ButtonGraphics(B3,x))
    B4.bind('<Leave>',lambda x: ButtonGraphics(B4,x))

MainFrame()