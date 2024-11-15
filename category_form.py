import tkinter as tk
from tkinter import ttk 
from tkcalendar import DateEntry
import mysql.connector
from tkinter import messagebox
from datetime import date
from employees import employee



def clear(catid,catname,desc):
    catid.delete(0,tk.END)
    catname.delete(0,tk.END)
    desc.delete("1.0",tk.END)
    categorytable.selection_remove(categorytable.focus())

def delete():
    selected=categorytable.selection()
    if not selected:
        messagebox.showerror("error","No Data Selected")
    else:    
        data=categorytable.item(selected)
        row=data['values']
        print(row)
        if len(row)>0:
            id=row[0]

            query="""DELETE  FROM categories WHERE category_id=%s """
            mycursor.execute(query,(id,))
            db.commit()
            messagebox.showinfo('success','data has been deleted')
            showdata()
        else:
            messagebox.showerror('error','no data found')

def add(catid,catname,desc):
    desc=desc.strip()
    if catid==""or catname=="" or desc=="":
        messagebox.showerror('error','fill the fields')
    else:
        try:
            query="""INSERT INTO categories VALUES (%s,%s,%s)"""
            data=(catid,catname,desc)
            mycursor.execute(query,data)
            db.commit()
            showdata()
        except Exception as e :
            messagebox.showerror("error",e)

def showdata():
    query="""SELECT * FROM categories"""
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    categorytable.delete(*categorytable.get_children())
    for x in fetched_data:
        categorytable.insert("",tk.END,values=x)

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
    query="""CREATE TABLE IF NOT EXISTS categories (category_id INT  PRIMARY KEY , category_name VARCHAR(100),
    description VARCHAR(100))"""
    mycursor.execute(query)
    db.commit()


def category(window):
    global backimage,logoimage,categorytable
    categorywindow=tk.Frame(window,bg='white')
    categorywindow.place(x=250,y=98,width=950,height=622)
    headinglabel=tk.Label(categorywindow,text='Category managing details',font=('times new roman',20,'bold'),bg='#0f4d7d',fg='white')
    headinglabel.place(x=0,y=0,relwidth=1)

    backimage=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\arrow.png')
    backbutton=tk.Button(categorywindow,image=backimage,bd=3,width=40,command=lambda: categorywindow.place_forget())
    backbutton.place(x=5,y=40)


    leftframe=tk.Frame(categorywindow,bg='white')
    leftframe.place(x=0,y=70,height=620,width=470)

    logoimage=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\product_category.png')
    image=tk.Label(leftframe,image=logoimage,bg="white")
    image.place(x=50,y=80)

    rightframe=tk.Frame(categorywindow,bg='white')
    rightframe.place(x=480,y=40,width=460,height=580)

    cat_id=tk.Label(rightframe,text='Category Id',font=('times new roman ',10,'bold'),bg='white')
    cat_identry=tk.Entry(rightframe,width=35,bg='lightyellow')
    cat_id.place(x=0,y=50)
    cat_identry.place(x=150,y=50)

    cat_name=tk.Label(rightframe,text='Category Name',font=('times new roman ',10,'bold'),bg='white')
    cat_nameentry=tk.Entry(rightframe,width=35,bg='lightyellow')
    cat_name.place(x=0,y=100)
    cat_nameentry.place(x=150,y=100)

    xscroll=tk.Scrollbar(rightframe,orient='horizontal')
    yscroll=tk.Scrollbar(rightframe,orient='vertical')

    description=tk.Label(rightframe,text='Description',font=('times new roman ',10,'bold'),bg='white')
    descriptionentry=tk.Text(rightframe,width=25,bg='lightyellow',height=5)
    description.place(x=0,y=150)
    descriptionentry.place(x=150,y=150)  

    categorytable=ttk.Treeview(rightframe,columns=('categoryid','categoryname','description'),show='headings',xscrollcommand=xscroll.set,
                               yscrollcommand=yscroll.set)
    categorytable.place(width=400,height=250,y=300)

    xscroll.pack(side='bottom',fill='x')
    yscroll.pack(side='right',fill='y')

    xscroll.config(command=categorytable.xview)
    yscroll.config(command=categorytable.yview)

    categorytable.heading('categoryid',text='Category Id')
    categorytable.heading('categoryname',text='Category name')
    categorytable.heading('description',text='Description')

    button3=tk.Button(rightframe,text='Add',width=10,font=('times new roman',11,'bold'),bg='#0f4d7d',fg='white',command=lambda:
                      add(cat_identry.get(),cat_nameentry.get(),descriptionentry.get("1.0",tk.END)))
                      
    button3.place(x=80,y=250)
    
    button4=tk.Button(rightframe,text='Delete',width=10,font=('times new roman',11,'bold'),bg='#0f4d7d',fg='white',command=lambda:delete())
    
    button4.place(x=200,y=250)

    button5=tk.Button(rightframe,text='Clear',width=10,font=('times new roman',11,'bold'),bg='#0f4d7d',fg='white',
                      command=lambda:clear(cat_identry,cat_nameentry,descriptionentry))
    
    button5.place(x=320,y=250)
    conncectdb()
    showdata()