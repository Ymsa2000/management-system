import tkinter as tk
from tkinter import ttk 
from tkcalendar import DateEntry
import mysql.connector
from tkinter import messagebox
from datetime import date



def search(search_option,value):
    if search_option=="Search by" :
        messagebox.showerror('error','data type must be selected')
    elif value=="":
        messagebox.showerror('error','search value must be inserted')
    else:

        query=f"""SELECT * FROM employeesdata WHERE {search_option} like %s  """
        data_1=(f'%{value}%',)
        mycursor.execute(query,data_1)
        record=mycursor.fetchall()
        table.delete(*table.get_children())
        for x in record : 
            table.insert('',tk.END,values=x)



def delete(empid,name,email,contact,password,salary,gender,employment_type,address,usertype,workshift,dob,doj,education):

    selected=table.selection()
    if not selected :
       messagebox.showerror('error','No data was selected')
    else:
        result=messagebox.askyesno('Confirm','DO YOU REALLY WANT TO DELETE THIS employee')
        if result:
   
            query="""DELETE  FROM employeesdata WHERE empid=%s"""
            mycursor.execute(query,(empid.get(),))
            db.commit()
            clear(empid,name,email,contact,password,salary,gender,employment_type,address,usertype,workshift,dob,doj,education,False)
            showdata()


def update(empid,name,email,contact,password,salary,gender,employment_type,address,usertype,workshift,dob,doj,education):
    select=table.selection()

    if not select:
        messagebox.showerror('error','No data selected')
    else:
        query="""SELECT * FROM employeesdata WHERE empid=%s """
        mycursor.execute(query,(empid,))
        old_data=mycursor.fetchone()
        old_data=old_data[1:]
        # print(old_data)
        address=address.strip()
        new_data=(name,email,gender,dob,contact,employment_type,workshift,address,doj,salary,usertype,password,education)
        # print(new_data)
        if new_data==old_data:
            messagebox.showerror('error','No Change Detected')
        else:

            query="""UPDATE  employeesdata SET name=%s , email=%s, contact=%s , password=%s , salary=%s , gender=%s , employment_type=%s , workshift=%s,
            doj=%s,address=%s,user_type=%s,education=%s,dob=%s WHERE empid=%s"""
            data=(name,email,contact,password,salary,gender,employment_type,workshift,doj,address,usertype,education,dob,empid)
                
            mycursor.execute(query,data)
            db.commit()
            messagebox.showinfo('success','data updated')
            showdata()


def showdata():
    query="""SELECT * FROM employeesdata """
    mycursor.execute(query)
    fetcheddata=mycursor.fetchall()
    table.delete(*table.get_children())

    for x in fetcheddata:
        table.insert('',tk.END,values=x)

def select_data(event,empident,nameident,emailident,contactident,
                passwordident,salaryident,genderident,employmenttypeident,addressident,usertypeident,workshiftident,dobentry,dojentry,education):
    clear(empident,nameident,emailident,contactident,
                passwordident,salaryident,genderident,employmenttypeident,addressident,usertypeident,workshiftident,dobentry,dojentry,education,False)
    index=table.focus()
    content=table.item(index)
    data=content['values']
    empident.insert(0,data[0])
    nameident.insert(0,data[1])
    emailident.insert(0,data[2])
    contactident.insert(0,data[5])
    passwordident.insert(0,data[12])
    salaryident.insert(0,data[10])
    genderident.set(data[3])
    dobentry.set_date(data[4])
    workshiftident.set(data[7])
    employmenttypeident.set(data[6])
    addressident.insert("1.0",data[8])
    dojentry.set_date(data[9])
    usertypeident.set(data[11])
    education.set(data[13])





def clear(empident,nameident,emailident,contactident,passwordident,salaryident,genderident,employmenttypeident,addressident,usertypeident,workshiftident,dobentry,dojentry,education,check):
    empident.delete(0,tk.END)
    nameident.delete(0,tk.END)
    emailident.delete(0,tk.END)
    contactident.delete(0,tk.END)
    passwordident.delete(0,tk.END)
    salaryident.delete(0,tk.END)
    genderident.set('Select Gender')
    employmenttypeident.set('Select Type')
    addressident.delete("1.0",tk.END)
    usertypeident.set('Select Type')
    workshiftident.set('Select Shift')
    dobentry.set_date(date.today())
    dojentry.set_date(date.today())
    education.set('Select Education')
    if check :
        table.selection_remove(table.selection())
    


def addemployee(empid,name,email,contact,password,salary,gender,employment_type,address,usertype,workshift,dob,doj,education):
    address=address.strip()

    if empid=='' or name=='' or email=='' or contact=='' or password=='' or salary=='' or gender=='Select Gender' or employment_type=='Select Type' or  address=='\n' or usertype=='Select type' or workshift=='Select Shift'   :
        messagebox.showerror('error','all fields must be full ')
    else:   
        try:
            connecttodatabase()
            query="""INSERT INTO employeesdata (empid ,name ,email ,gender ,dob , Contact ,employment_type ,workshift ,address ,doj ,salary ,
                    user_type ,password,education) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
            data=(empid,name,email,gender,dob,contact,employment_type,workshift,address,doj,salary,usertype,password,education)
            mycursor.execute(query,data)
            db.commit()
            messagebox.showinfo('success','data has been added')
            showdata()

        except Exception as e :
            messagebox.showerror('error',f"error due to {e}")

def connecttodatabase():
    
    global mycursor,db
    try:
        db=mysql.connector.connect(
            host='localhost',
            user='root',
            password='root' )
    except:
        messagebox.showerror('error','cannot find database')

    mycursor=db.cursor()
    query='CREATE DATABASE IF NOT EXISTS inventory_mangment_system'
    mycursor.execute(query)
    query="USE inventory_mangment_system"
    mycursor.execute(query)
    query="""CREATE TABLE IF NOT EXISTS employeesdata (empid INT (10) PRIMARY KEY ,name Varchar (100) ,email Varchar (100) ,gender Varchar (100) ,dob Varchar (100) ,
                contact Varchar (100) ,employment_type Varchar (100) ,workshift Varchar (100) ,address Varchar (100) ,doj Varchar (100) ,salary Varchar (100) ,
                user_type Varchar (100) ,password Varchar (100),education VARCHAR(100) )"""
    mycursor.execute(query)

connecttodatabase()



def employee(window):
    global backimage,table,table,empident,nameident,passwordident,addressident,genderident,dobentry,dojentry,contactident,emailident,salaryident,passwordident,workshiftident,employmenttypeident
    employeewindow=tk.Frame(window,bg='white')
    employeewindow.place(x=250,y=98,width=950,height=622)
    headinglabel=tk.Label(employeewindow,text='Manage Employee Details',font=('times new roman',20,'bold'),bg='#0f4d7d',fg='white')
    headinglabel.place(x=0,y=0,relwidth=1)

    backimage=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\arrow.png')
    backbutton=tk.Button(employeewindow,image=backimage,bd=3,width=40,command=lambda: employeewindow.place_forget())
    backbutton.place(x=5,y=40)

    topframe=tk.Frame(employeewindow,bg='white')
    topframe.place(x=0,y=67,relwidth=1,height=250)

    searchframe=tk.Frame(topframe,bg='white')
    searchframe.pack()

    searchbar=ttk.Combobox(searchframe,values=('empid','name','email'),font=('times new roman',11,'bold'),state='readonly')
    searchbar.set('Search by')
    searchbar.grid(row=0,column=0)

    searchentry=tk.Entry(searchframe,width=20,bg='lightyellow',fg='black',font=('times new roman',11,'bold'))
    searchentry.grid(row=0,column=1,padx=15)

    searchbutton=tk.Button(searchframe,width=15,bg='#0f4d7d',fg='white',text='Search',font=('times new roman',11,'bold'),
                           command=lambda:search(searchbar.get(),searchentry.get()))
    searchbutton.grid(row=0,column=2,padx=15)

    showallbutton=tk.Button(searchframe,width=15,bg='#0f4d7d',fg='white',text='Show All',font=('times new roman',11,'bold'),command=lambda:showdata())
    showallbutton.grid(row=0,column=3,padx=15)

    xscrollbar=tk.Scrollbar(topframe,orient='horizontal')
    yscrollbar=tk.Scrollbar(topframe,orient='vertical')
    table=ttk.Treeview(topframe,columns=('id','name','email','gender','dob','contact','employment_type','work_shift','address','doj','salary','usertype','password','education'),show='headings',yscrollcommand=yscrollbar.set,xscrollcommand=yscrollbar.set)
    
    xscrollbar.pack(side='bottom',fill='x')
    yscrollbar.pack(side='right',fill='y')
    xscrollbar.config(command=table.xview)
    yscrollbar.config(command=table.yview)
    table.pack(pady=10)

    table.heading('id',text='Id')
    table.heading('name',text='Name')
    table.heading('email',text='Email')
    table.heading('gender',text='Gender')
    table.heading('dob',text='Dob')
    table.heading('contact',text='Contact')

    table.heading('employment_type',text='Employment type')
    table.heading('education',text='Education')
    table.heading('work_shift',text='Work shift')
    table.heading('address',text='Address')
    table.heading('doj',text='Doj')
    table.heading('salary',text='Salary')
    table.heading('usertype',text='User type')
    table.heading('password',text='Password')


    details=tk.Frame(employeewindow,bg='white')
    details.place(x=0,y=315,relwidth=1,height=280)

    empid=tk.Label(details,text=('Emp ID'),font=('times new roman',12,'bold'),bg='white')
    empident=tk.Entry(details,width=20,bg='lightyellow',font=('times new roman',12,'bold'))
    empid.grid(row=0,column=0,padx=30,pady=10,sticky='w')
    empident.grid(row=0,column=1,pady=10,sticky='w')

    

    nameid=tk.Label(details,text=('Name'),font=('times new roman',12,'bold'),bg='white')
    nameident=tk.Entry(details,width=20,bg='lightyellow',font=('times new roman',12,'bold'))
    nameid.grid(row=0,column=2,padx=30,pady=10,sticky='w')
    nameident.grid(row=0,column=3,pady=10,sticky='w')
    

    emailid=tk.Label(details,text=('Email'),font=('times new roman',12,'bold'),bg='white')
    emailident=tk.Entry(details,width=20,bg='lightyellow',font=('times new roman',12,'bold'))
    emailid.grid(row=0,column=4,padx=30,pady=10,sticky='w')
    emailident.grid(row=0,column=5,pady=10,sticky='w')


    contactid=tk.Label(details,text=('Contact'),font=('times new roman',12,'bold'),bg='white')
    contactident=tk.Entry(details,width=20,bg='lightyellow',font=('times new roman',12,'bold'))
    contactid.grid(row=1,column=4,padx=30,pady=10,sticky='w')
    contactident.grid(row=1,column=5,pady=10,sticky='w')


    salaryid=tk.Label(details,text=('Salary'),font=('times new roman',12,'bold'),bg='white')
    salaryident=tk.Entry(details,width=20,bg='lightyellow',font=('times new roman',12,'bold'))
    salaryid.grid(row=4,column=4,padx=30,pady=10,sticky='w')
    salaryident.grid(row=4,column=5,pady=10,sticky='w')


    passwordid=tk.Label(details,text=('Password'),font=('times new roman',12,'bold'),bg='white')
    passwordident=tk.Entry(details,width=20,bg='lightyellow',font=('times new roman',12,'bold'))
    passwordid.grid(row=3,column=4,padx=30,pady=10,sticky='w')
    passwordident.grid(row=3,column=5,pady=10,sticky='w')
    

    addressid=tk.Label(details,text=('Address'),font=('times new roman',12,'bold'),bg='white')
    addressident=tk.Text(details,width=20,height=3,bg='lightyellow',font=('times new roman',12,'bold'))
    addressid.grid(row=3,column=0,padx=30,pady=10,sticky='w')
    addressident.grid(row=3,column=1,pady=10,sticky='w')

    genderid=tk.Label(details,text=('Gender'),font=('times new roman',12,'bold'),bg='white')
    genderident=ttk.Combobox(details,values=('Male','Female'),state='readonly',width=23)
    genderident.set('Select Gender')
    genderid.grid(row=1,column=0,padx=30,pady=10,sticky='w')
    genderident.grid(row=1,column=1,pady=10,sticky='w')

    dobid=tk.Label(details,text=('D.O.B'),font=('times new roman',12,'bold'),bg='white')
    dobid.grid(row=1,column=2,padx=30,pady=10,sticky='w')
    dobentry=DateEntry(details,width=23,state='readonly',date_pattern='dd/mm/yyyy')
    dobentry.grid(row=1,column=3,sticky='w')
    
    
    workshiftid=tk.Label(details,text=('Work Shift'),font=('times new roman',12,'bold'),bg='white')
    workshiftident=ttk.Combobox(details,values=('Morning','Evening'),state='readonly',width=23)
    workshiftident.set('Select Shift')
    workshiftid.grid(row=2,column=4,padx=30,pady=10,sticky='w')
    workshiftident.grid(row=2,column=5,pady=10,sticky='w')

    educationid=tk.Label(details,text=('Education'),font=('times new roman',12,'bold'),bg='white')
    educationident=ttk.Combobox(details,values=('ainshams','cairo'),state='readonly',width=23)
    educationident.set('Select Education')
    educationid.grid(row=2,column=2,padx=30,pady=10,sticky='w')
    educationident.grid(row=2,column=3,pady=10,sticky='w')

    dojid=tk.Label(details,text=('D.O.J'),font=('times new roman',12,'bold'),bg='white')
    dojid.grid(row=4,column=2,padx=30,pady=10,sticky='w')
    dojentry=DateEntry(details,width=23,state='readonly',date_pattern='dd/mm/yyyy')
    dojentry.grid(row=4,column=3,sticky='w')

    usertypeid=tk.Label(details,text=('User Type'),font=('times new roman',12,'bold'),bg='white')
    usertypeident=ttk.Combobox(details,values=('Admin','Employee'),state='readonly',width=23)
    usertypeident.set('Select Type')
    usertypeid.grid(row=3,column=2,padx=30,pady=10,sticky='w')
    usertypeident.grid(row=3,column=3,pady=10,sticky='w')

    employmenttypeid=tk.Label(details,text=('Emp.Type'),font=('times new roman',12,'bold'),bg='white')
    employmenttypeident=ttk.Combobox(details,values=('Full time','part Time'),state='readonly',width=23)
    employmenttypeident.set('Select Type')
    employmenttypeid.grid(row=2,column=0,padx=30,pady=10,sticky='w')
    employmenttypeident.grid(row=2,column=1,pady=10,sticky='w')

    button1=tk.Button(employeewindow,text=('Add'),width=12,font=('times new roman',11,'bold'),bg='#0f4d7d',fg='white',
                      command=lambda:addemployee(empident.get(),nameident.get(),emailident.get(),contactident.get(),
                        passwordident.get(),salaryident.get(),genderident.get(),employmenttypeident.get()
                        ,addressident.get("1.0",tk.END),usertypeident.get(),workshiftident.get(),dobentry.get(),dojentry.get(),educationident.get())
    )
    button1.place(x=100,y=580)

    button2=tk.Button(employeewindow,text=('Update'),width=12,font=('times new roman',11,'bold'),bg='#0f4d7d',fg='white',command=lambda:update(
                        empident.get(),nameident.get(),emailident.get(),contactident.get(),
                        passwordident.get(),salaryident.get(),genderident.get(),employmenttypeident.get()
                        ,addressident.get("1.0",tk.END),usertypeident.get(),workshiftident.get(),dobentry.get(),dojentry.get(),educationident.get()))
    button2.place(x=300,y=580)    

    button3=tk.Button(employeewindow,text=('clear'),width=12,font=('times new roman',11,'bold'),bg='#0f4d7d',fg='white',command=lambda:clear(empident,nameident,emailident,contactident,passwordident,salaryident,genderident,employmenttypeident,addressident,usertypeident,workshiftident,dobentry,dojentry,educationident,True))
    button3.place(x=500,y=580)

    button4=tk.Button(employeewindow,text=('delete'),width=12,font=('times new roman',11,'bold'),bg='#0f4d7d',fg='white',command=lambda: delete
                      (empident,nameident,emailident,contactident,passwordident,
                       salaryident,genderident,employmenttypeident,addressident,usertypeident,workshiftident,dobentry,dojentry,educationident))
    button4.place(x=700,y=580)
    


    


    showdata()



    table.bind("<ButtonRelease-1>", lambda event:select_data(event,empident,nameident,emailident,contactident,passwordident,salaryident,genderident,employmenttypeident,addressident,usertypeident,workshiftident,dobentry,dojentry,educationident))