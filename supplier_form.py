import tkinter as tk
from tkinter import ttk 
from tkcalendar import DateEntry
import mysql.connector
from tkinter import messagebox
from datetime import date
from employees import employee




def search(invoice2):
    if invoice2=="":
        messagebox.showerror('error',"add value to search for ")
    else:
        try:
            query=f"""SELECT * FROM suppliers WHERE invoice_no LIKE {invoice2}"""
            mycursor.execute(query)
            fetched_data=mycursor.fetchall()
            if not fetched_data:
                messagebox.showerror('error','No data found')
            else:
                suppliertable.delete(*suppliertable.get_children())
                for x in fetched_data:
                    suppliertable.insert("",tk.END,values=x)
        except Exception as e :
            messagebox.showerror('error',f"error due to {e}")

def update(invoice_no,suppliername,contact,description):
    description=description.strip()
    selected=suppliertable.selection()
    if not selected:
        messagebox.showerror("error","No Data Selected")
    else:
        
        query="""SELECT * FROM suppliers WHERE invoice_no=%s"""
        mycursor.execute(query,(invoice_no,))
        fetched_data=mycursor.fetchone()
        old_data=fetched_data[1:]
        print(old_data)
        new_data=(suppliername,contact,description)
        print (new_data)
        if new_data==old_data:
            messagebox.showerror("error","No changes were made")
        else:
            query="""UPDATE suppliers Set supplier_name=%s ,contact=%s,description=%s WHERE invoice_no = %s"""
            mycursor.execute(query,(suppliername,contact,description,invoice_no))
            db.commit()
            messagebox.showinfo('success','Data has been Updated')
            showdata()


def delete(invoice_no,suppliername,contact,description):
    selected=suppliertable.selection()
    if not selected:
        messagebox.showerror("error","No Data Selected")
    else:
        query="""DELETE  FROM suppliers WHERE invoice_no=%s """
        mycursor.execute(query,(invoice_no.get(),))
        db.commit()
        clear(invoice_no,suppliername,contact,description,False)
        showdata()


def selectdata(event,invoice_no,suppliername,contact,description):
    clear(invoice_no,suppliername,contact,description,False)
    index=suppliertable.focus()
    content=suppliertable.item(index)
    data=content['values']
    invoice_no.insert(0,data[0])
    suppliername.insert(0,data[1])
    contact.insert(0,data[2])
    description.insert("1.0",data[3])




def clear(invoice_no,suppliername,contact,description,check):
    invoice_no.delete(0,tk.END)
    suppliername.delete(0,tk.END)
    contact.delete(0,tk.END)
    description.delete("1.0",tk.END)
    if check:
        suppliertable.selection_remove(suppliertable.selection())

def showdata():
    query="""SELECT * FROM suppliers"""
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    suppliertable.delete(*suppliertable.get_children())
    for x in fetched_data:
        suppliertable.insert("",tk.END,values=x)
    



def addsupplier(invoice_no,suppliername,contact,description):
    description=description.strip()
    try:
        if invoice_no=="" or suppliername=="" or contact=="" or description=="":
            messagebox.showerror('error','all fields must be filled')
        
        else:
            query="INSERT INTO suppliers VALUES (%s,%s,%s,%s)"
            
            data=(invoice_no,suppliername,contact,description)
            mycursor.execute(query,data)
            db.commit()
            
            showdata()

    except Exception as e :
        messagebox.showerror('error',e)










def conncectdb():
        global db, mycursor
        try:
            db=mysql.connector.connect(
                host='localhost',
                user='root',
                password='root')
            
        except:
            messagebox.showerror('error''Cannot find database')
            return
        mycursor=db.cursor()
        query="""CREATE DATABASE IF NOT EXISTS inventory_mangment_system """
        mycursor.execute(query)
        query="""USE inventory_mangment_system"""
        mycursor.execute(query)
        query="""CREATE TABLE IF NOT EXISTS suppliers (invoice_no INT  PRIMARY KEY , supplier_name VARCHAR(100),contact VARCHAR(100)
        ,description VARCHAR(100))"""
        mycursor.execute(query)





def supplier(window):
   
    global backimage,suppliertable
    supplierwindow=tk.Frame(window,bg='white')
    supplierwindow.place(x=250,y=98,width=950,height=622)
    headinglabel=tk.Label(supplierwindow,text='supplier managing details',font=('times new roman',20,'bold'),bg='#0f4d7d',fg='white')
    headinglabel.place(x=0,y=0,relwidth=1)

    backimage=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\arrow.png')
    backbutton=tk.Button(supplierwindow,image=backimage,bd=3,width=40,command=lambda: supplierwindow.place_forget())
    backbutton.place(x=5,y=40)

    leftframe=tk.Frame(supplierwindow,bg='white')
    leftframe.place(x=0,y=70,height=620,width=470)

    rightframe=tk.Frame(supplierwindow,bg='white')
    rightframe.place(x=480,y=40,width=460,height=580)

    invoice=tk.Label(leftframe,text='Invoice no.',font=('times new roman ',10,'bold'),bg='white')
    invoiceentry=tk.Entry(leftframe,width=35,bg='lightyellow')
    invoice.place(x=40,y=50)
    invoiceentry.place(x=180,y=50)

    suppliername=tk.Label(leftframe,text='Supplier name.',font=('times new roman ',10,'bold'),bg='white')
    suppliernameentry=tk.Entry(leftframe,width=35,bg='lightyellow')
    suppliername.place(x=40,y=120)
    suppliernameentry.place(x=180,y=120)

    contact=tk.Label(leftframe,text='Contact.',font=('times new roman ',10,'bold'),bg='white')
    contactentry=tk.Entry(leftframe,width=35,bg='lightyellow')
    contact.place(x=40,y=190)
    contactentry.place(x=180,y=190)

    description=tk.Label(leftframe,text='Description',font=('times new roman ',10,'bold'),bg='white')
    descriptionentry=tk.Text(leftframe,width=30,height=7,bg='lightyellow')
    description.place(x=40,y=260)
    descriptionentry.place(x=180,y=260)

    

    button1=tk.Button(leftframe,text='Save',width=10,font=('times new roman',11,'bold'),bg='#0f4d7d',fg='white',command=lambda:
                      addsupplier(invoiceentry.get(),suppliernameentry.get(),contactentry.get(),descriptionentry.get("1.0",tk.END)))
    button1.place(x=40,y=450)

    button2=tk.Button(leftframe,text='Update',width=10,font=('times new roman',11,'bold'),bg='#0f4d7d',fg='white',
                      command=lambda:
                      update(invoiceentry.get(),suppliernameentry.get(),contactentry.get(),descriptionentry.get("1.0",tk.END)))
    button2.place(x=150,y=450)
    
    button3=tk.Button(leftframe,text='Delete',width=10,font=('times new roman',11,'bold'),bg='#0f4d7d',fg='white',
                      command=lambda:delete(invoiceentry,suppliernameentry,contactentry,descriptionentry))
    button3.place(x=260,y=450)
    
    button4=tk.Button(leftframe,text='Clear',width=10,font=('times new roman',11,'bold'),bg='#0f4d7d',fg='white',command=lambda:
                      clear(invoiceentry,suppliernameentry,contactentry,descriptionentry,True))
    
    button4.place(x=370,y=450)

    xscorll=ttk.Scrollbar(rightframe,orient='horizontal')
    yscroll=ttk.Scrollbar(rightframe,orient='vertical')
    
    

    suppliertable=ttk.Treeview(rightframe,columns=('invoiceno','name','contact','description'),show='headings',
                               yscrollcommand=yscroll.set,xscrollcommand=xscorll.set)
    
    suppliertable.place(x=0,y=190,width=420,height=330)
    xscorll.pack(side='bottom',fill='x')
    yscroll.pack(side='right',fill='y')
    xscorll.config(command=suppliertable.xview)
    yscroll.config(command=suppliertable.yview)

    suppliertable.heading('invoiceno',text='InVoice no.')
    suppliertable.heading('name',text='Name')
    suppliertable.heading('contact',text='Contact')
    suppliertable.heading('description',text='Description')

    suppliertable.column('invoiceno',width=110)
    suppliertable.column('name',width=150)
    suppliertable.column('contact',width=200)
    suppliertable.column('description',width=200)

    invoiceno2=tk.Label(rightframe,text='Invoice no.',font=('times new roman ',10,'bold'),bg='white')
    invoiceno2entry=tk.Entry(rightframe,width=20,bg='lightyellow')
    invoiceno2.place(x=0,y=100)
    invoiceno2entry.place(x=80,y=100)

    searchbutton1=tk.Button(rightframe,width=10,bg='#0f4d7d',fg='white',text='Search',font=('times new roman',11,'bold'),command=lambda:
                            search(invoiceno2entry.get()))
    searchbutton1.place(x=220,y=95)

    showallbutton1=tk.Button(rightframe,width=10,bg='#0f4d7d',fg='white',text='Show All',font=('times new roman',11,'bold'),command=lambda:showdata())
    showallbutton1.place(x=330,y=95)
    
    suppliertable.bind("<ButtonRelease-1>",lambda event: selectdata(event,invoiceentry,suppliernameentry,contactentry,descriptionentry))

    conncectdb()

    showdata()    