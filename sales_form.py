import tkinter as tk
from tkinter import ttk 
from tkcalendar import DateEntry
import mysql.connector
from tkinter import messagebox
from datetime import date
import os

def search():
    for i in os.listdir('bills'):
        bill=os.path.splitext(i)[0].replace(" ","")
        print(bill)
        if bill==invoicenoentry.get():
            billarea.delete("1.0",tk.END)
            with  open(f"C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\bills\\ {bill}.txt",'r') as file:
                content=file.read()
                billarea.insert(tk.END,content)
                table.selection_remove(table.selection())

        


    



def selectbill(event):
    billarea.delete("1.0",tk.END)
    index=table.focus()
    data=table.item(index)
    bill=data['values'][0]
    with open(f"C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\bills\\ {bill}.txt",'r') as file:

        content=file.read()

    billarea.insert(tk.END,content)



def showbills():
    for i in os.listdir('bills'):
        bill=os.path.splitext(i)
        table.insert("",tk.END,values=bill)




def sales(window):
    global backimage,table,billarea,invoicenoentry
    saleswindow=tk.Frame(window,bg='white')
    saleswindow.place(x=250,y=98,width=950,height=622)


    backimage=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\arrow.png')
    backbutton=tk.Button(saleswindow,image=backimage,bd=3,width=40,command=lambda: saleswindow.place_forget())
    backbutton.place(x=5,y=40)

    frame_1=tk.Frame(saleswindow,bg='red')
    frame_1.place(y=200,x=50,width=240,height=350)

    frame_2=tk.Frame(saleswindow,bg='red')
    frame_2.place(y=200,x=340,width=350,height=350)

    searchframe=tk.Frame(saleswindow,bg='white')
    searchframe.place(y=80,x=50,width=600,height=100)

    invoiceno=tk.Label(searchframe,font=('times new roman',14,'bold'),text='Invoice No.',bg='white')
    invoiceno.grid(row=0,column=0)


    invoicenoentry=tk.Entry(searchframe,font=('times new roman',11,'bold'),bg='lightyellow')
    invoicenoentry.grid(row=0,column=1,padx=10)


    searchbutton=tk.Button(searchframe,font=('times new roman',11,'bold'),bg='#0f4d7d',width=12,text='Search',fg='white',command=lambda:search())
    searchbutton.grid(row=0,column=2,padx=10)

    showallbutton=tk.Button(searchframe,font=('times new roman',11,'bold'),bg='#0f4d7d',width=12,text='Show All',fg='white')
    showallbutton.grid(row=0,column=3,padx=10)

    yscroll=ttk.Scrollbar(frame_1,orient='vertical')
    table=ttk.Treeview(frame_1,yscrollcommand=yscroll.set,columns=('id'),show='headings')
    yscroll.pack(side='right',fill='y')
    table.pack(fill='both',expand=1,side='left')


    yscroll1=ttk.Scrollbar(frame_2,orient='vertical')

    billarea=tk.Text(frame_2,yscrollcommand=yscroll1.set)
    yscroll1.pack(side='right',fill='y')

    billarea.pack(side='left',fill='both',expand=1)


    showbills()
    table.bind('<ButtonRelease-1>',lambda event:selectbill(event))