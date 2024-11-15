import tkinter as tk
import time
from tkinter import ttk 
from tkcalendar import dateentry
from tkinter import messagebox
import mysql.connector
import random
import os,tempfile





if not os.path.exists('bills'):
    os.mkdir('bills')

def print():
    if billarea.get("1.0",tk.END)=='\n':
        messagebox.showerror('error','no bill found')
    else:
        try:
        

            file=tempfile.mktemp('.txt')
            open(file,'w').write(billarea.get("1.0",tk.END))
            
            os.startfile(file,'print')
        except:
            messagebox.showerror('error','bill was not printed')

def saved():
    result=messagebox.askyesno('confirm','do you want to save the bill')
    if result:

        bill_content=billarea.get("1.0",tk.END)
        file=open(f'bills/ {billnumber}.txt','w')
        file.write(bill_content)

        file.close()
        messagebox.showinfo('succes',f'{billnumber}saved succefully')




def clearall():
    billarea.delete("1.0",tk.END)

def logout():
    timelabel.after_cancel(clockid)
    window2.destroy()
    import login


def generate():
    global billnumber
    feched_data=buytable.get_children()
    if nameentry.get()==""or contactentry.get()=="":
        messagebox.showerror('error','Please add name and contact')
    elif not feched_data:
        messagebox.showerror('error','Please add something to cart')
    else:
        billnumber=random.randint(500,50000)

        billarea.insert(tk.END,'\t   **WELCOME CUSTOMER**\n\n')
        billarea.insert(tk.END,'========================================\n\n')
        billarea.insert(tk.END,f'Customer name:  {nameentry.get()}\n')
        billarea.insert(tk.END,f'Phone no.:  {contactentry.get()}\n')
        billarea.insert(tk.END,f'Bill no.:{billnumber}\t        Date:{currentdate}\n\n')
        billarea.insert(tk.END,'========================================\n\n')
        billarea.insert(tk.END,'Id      name     Price     qty     net\n')
        billarea.insert(tk.END,'========================================\n\n')



        pay=0
        for index in feched_data:
            data=buytable.item(index)
            data=data['values']
            qty=int(data[3])
            
            price=int(data[2])
            
            net=qty*price
            
            pay+=net
            billarea.insert(tk.END,f'{data[0]}\t')
            billarea.insert(tk.END,f'{data[1]}\t')
            billarea.insert(tk.END,f'  {data[2]}\t')
            billarea.insert(tk.END,f'    {data[3]}\t')
            billarea.insert(tk.END,f'  {net}\n')


        billarea.insert(tk.END,'========================================\n\n')
        billarea.insert(tk.END,f'Bill amount: {pay} L.E\n')

        
        buytable.delete(*buytable.get_children())
        saved()

                        
       



def delete():
    index=buytable.focus()
    fetched_Data=buytable.item(index)
    fetched_Data=fetched_Data['values']
    qtyadded=int(fetched_Data[3])
    query="""SELECT qty FROM products WHERE id=%s"""
    idd=int(fetched_Data[0])
    mycursor.execute(query,(idd,))
    fetched_Data2=mycursor.fetchone()

    qtyfromdata=int(fetched_Data2[0])
 

    qtyfinal=qtyfromdata+qtyadded
    query="""UPDATE products SET qty=%s WHERE id=%s """
    
    mycursor.execute(query,(qtyfinal,idd,))
    db.commit()
    showdata()
    clear(pname2entry,priceentry,qtyentry,instock,False)

    buytable.delete(index)

def add():
    global save
    index=producttable2.focus()
    data=producttable2.item(index)
    exactdata=data['values']
    if pname2entry.get()=="":
        messagebox.showerror('error','please choose product first')
    elif int(qtyentry.get())>int(exactdata[3]):
        messagebox.showerror('error','there is not enough good in storage')
    else:
        index=producttable2.focus()
        data=producttable2.item(index)
        exactdata=data['values']
        buytable.insert("",tk.END,values=(exactdata[0],pname2entry.get(),priceentry.get(),qtyentry.get()))
        save=int(qtyentry.get())
        priceentry.config(state='normal')
        pname2entry.config(state='normal')
        clear(pname2entry,priceentry,qtyentry,instock,False)
        query="""UPDATE  products SET qty=%s WHERE id=%s"""
        value=((int(exactdata[3])-save),(exactdata[0]),)
        mycursor.execute(query,value)
        db.commit()
        showdata()
        # index=producttable2.focus()
        # data=producttable2.item(index)
        # exactdata=data['values']
        # instock.config(text=f'Instock {exactdata[3]}')




def select(event,name,price,qty,instock):
    priceentry.config(state='normal')
    nameentry.config(state='normal')
    clear(name,price,qty,instock,False)

    index=producttable2.focus()
    data=producttable2.item(index)
    exactdata=data['values']
    name.insert(0,exactdata[1])
    price.insert(0,exactdata[2])
    qty.insert(0,int(1))
    instock.config(text=f'Instock {exactdata[3]}')
    priceentry.config(state='disabled')
    name.config(state='disabled')
    

   
    
def clear(pname2entry,priceentry,qtyentry,instock,check):
    pname2entry.config(state='normal')
    priceentry.config(state='normal')
    priceentry.delete(0,tk.END)
    pname2entry.delete(0,tk.END)
    qtyentry.delete(0,tk.END)
    instock.config(text='Instock')

    if check:
        producttable2.selection_remove(producttable2.selection())



def search(value):
    if value=="":
        messagebox.showerror('error','please enter value to search')
    else:
        query="""SELECT id , name , price , qty , status FROM products WHERE name LIKE %s"""
        data=(f'%{value}%',)
        mycursor.execute(query,data)
        fetched_data=mycursor.fetchall()
        if not fetched_data:
            messagebox.showerror('error','no data found')
            
        producttable2.delete(*producttable2.get_children())

        for x in fetched_data:
            producttable2.insert("",tk.END,values=x)
        



def condb():
    global db , mycursor
    try:
        db=mysql.connector.connect(
            host='localhost',
            user='root',
            password='root'
        )
    except:
        messagebox.showerror('error','database not found')

    
    mycursor=db.cursor()
    mycursor.execute("""USE inventory_mangment_system""")



# def search():
#     query="""SELECT id , name , price , qty , status FROM products WHERE name"""


def showdata():
    query="""SELECT id , name , price , qty , status FROM products WHERE status=%s"""
    mycursor.execute(query,('Active',))
    fetched_data=mycursor.fetchall()
    producttable2.delete(*producttable2.get_children())
    for column in fetched_data:
        producttable2.insert("",tk.END,values=column)

    


def clock():
    global currentdate,currenttime,clockid
    currentdate=time.strftime('%d/%m/%Y')
    currenttime= time.strftime('%H:%M:%S')
    timelabel.config(text=f'Welcome \t\tdate:{currentdate}\t\ttime:{currenttime}')
    clockid=timelabel.after(1000,clock)


window2=tk.Tk()
window2.geometry('1540x795+-10+-3')
window2.title('retail')
window2.resizable(False,False)
window2.config(bg='white')

image1=tk.PhotoImage(file='inventory.png')
imslabel=tk.Label(window2,image=image1,compound='right' ,text='Inventory Managment System',font=('times new roman',40,'bold'),
bg='#010c48',fg='white',anchor='w',padx=40)
imslabel.place(x=0,y=0,relwidth=1)

logoutlabel=tk.Button(window2,text='Logout',font=('times new roman',20,'bold'),fg='#010c48',cursor='hand2',command=lambda:logout())
logoutlabel.place(x=1400,y=10)


timelabel=tk.Label(window2,font=('times new roman',20,'bold'),fg='#010c48',bg='grey')
timelabel.place(x=0,y=70,relwidth=1)
clock()

frame_1=tk.Frame(window2,bg='white')
frame_1.place(x=30,y=150,width=450,height=600)


frame_2=tk.Frame(window2,bg='white')
frame_2.place(x=500,y=150,width=650,height=600)

frame_3=tk.Frame(window2,bd=2,relief='ridge')
frame_3.place(x=1170,y=150,width=350,height=600)


searchframe=tk.Frame(frame_1,bg='white',bd=2,relief='ridge')
searchframe.place(height=150,relwidth=1)


heading=tk.Label(searchframe,text='All Products',font=('times new roman',18,'bold'),bg='#0f4d7d',fg='white')
heading.place(relwidth=1)

pname=tk.Label(searchframe,text='Product Name',font=('times new roman',15,'bold'),bg='white')
pname.place(x=20,y=45)

pentry=tk.Entry(searchframe,width=20,font=('times new roman',12,'bold'),bg='lightyellow')
pentry.place(y=48,x=190)

searchbutton=tk.Button(searchframe,width=12,bg='#0f4d7d',fg='white',text='Search',font=('times new roman',12,'bold'),cursor='hand2',
                       command=lambda: search(pentry.get()))
searchbutton.place(y=100,x=90)

showallbutton=tk.Button(searchframe,width=12,bg='#0f4d7d',fg='white',text='Show All',font=('times new roman',12,'bold'),cursor='hand2',
                        command=lambda:showdata())
showallbutton.place(y=100,x=260)




xscorll=ttk.Scrollbar(frame_1,orient='horizontal')
yscroll=ttk.Scrollbar(frame_1,orient='vertical')


producttable2=ttk.Treeview(frame_1,columns=('id','name','price','qty','status'),show='headings',xscrollcommand=xscorll.set,yscrollcommand=yscroll.set)
producttable2.place(y=160,height=400,x=20,width=400)

xscorll.pack(side='bottom',fill='x')
yscroll.place(x=430,y=160,height=420)
xscorll.config(command=producttable2.xview)
yscroll.config(command=producttable2.yview)



producttable2.heading('id',text='Id')
producttable2.heading('name',text='Name')
producttable2.heading('price',text='Price')
producttable2.heading('qty',text='Quantity')
producttable2.heading('status',text='Status')

producttable2.column('id',width=60,anchor='center')
producttable2.column('name',width=100,anchor='center')
producttable2.column('price',width=70,anchor='center')
producttable2.column('qty',width=70,anchor='center')
producttable2.column('status',width=90,anchor='center')



searchframe2=tk.Frame(frame_2,bg='white',bd=3,relief='ridge')
searchframe2.place(height=100,relwidth=1,y=0)


heading2=tk.Label(searchframe2,text='Customer Details',font=('times new roman',18,'bold'),bg='#0f4d7d',fg='white')
heading2.place(relwidth=1)

name=tk.Label(searchframe2,text='Name',font=('times new roman',13,'bold'),bg='white')
name.place(x=20,y=45)

nameentry=tk.Entry(searchframe2,width=20,font=('times new roman',11,'bold'),bg='lightyellow')
nameentry.place(y=48,x=90)

contact=tk.Label(searchframe2,text='Contact',font=('times new roman',13,'bold'),bg='white')
contact.place(x=300,y=45)

contactentry=tk.Entry(searchframe2,width=20,font=('times new roman',11,'bold'),bg='lightyellow')
contactentry.place(y=48,x=370)




addframe=tk.Frame(frame_2,bg='white',bd=3,relief='ridge')
addframe.place(height=145,relwidth=1,y=455)

pname2=tk.Label(addframe,text='Product Name',font=('times new roman',15,'bold'),bg='white')
pname2.place(x=10,y=10)

pname2entry=tk.Entry(addframe,width=16,font=('times new roman',11,'bold'),bg='lightyellow')
pname2entry.place(y=40,x=10)

price=tk.Label(addframe,text='Price',font=('times new roman',15,'bold'),bg='white')
price.place(x=210,y=10)

priceentry=tk.Entry(addframe,width=16,font=('times new roman',11,'bold'),bg='lightyellow')
priceentry.place(y=40,x=210)

qty=tk.Label(addframe,text='Quantity',font=('times new roman',15,'bold'),bg='white')
qty.place(x=410,y=10)

qtyentry=tk.Entry(addframe,width=16,font=('times new roman',11,'bold'),bg='lightyellow')
qtyentry.place(y=40,x=410)


addbutton=tk.Button(addframe,width=13,bg='#0f4d7d',fg='white',text='Add to Cart',font=('times new roman',12,'bold'),cursor='hand2',
                    command=lambda:add())
addbutton.place(y=80,x=210)

clearbutton=tk.Button(addframe,width=13,bg='#0f4d7d',fg='white',text='Clear',font=('times new roman',12,'bold'),cursor='hand2',
                      command=lambda:clear(pname2entry,priceentry,qtyentry,instock,True))
clearbutton.place(y=80,x=410)

del2button=tk.Button(addframe,width=7,bg='#0f4d7d',fg='white',text='Delete',font=('times new roman',12,'bold'),cursor='hand2',
                     command=lambda:delete())
del2button.place(y=60,x=550)


instock=tk.Label(addframe,text='Instock',font=('times new roman',15,'bold'),bg='white')
instock.place(x=10,y=85)



xscorll=ttk.Scrollbar(frame_2,orient='horizontal')
yscroll=ttk.Scrollbar(frame_2,orient='vertical')


buytable=ttk.Treeview(frame_2,columns=('id','name','price','qty'),show='headings',xscrollcommand=xscorll.set,yscrollcommand=yscroll.set)
buytable.place(y=110,height=320,x=320,width=310)

xscorll.place(x=320,y=430,width=320)
yscroll.place(x=630,y=110,height=320)
xscorll.config(command=buytable.xview)
yscroll.config(command=buytable.yview)



buytable.heading('id',text='Id')
buytable.heading('name',text='Name')
buytable.heading('price',text='Price')
buytable.heading('qty',text='Quantity')


buytable.column('id',width=60,anchor='center')
buytable.column('name',width=100,anchor='center')
buytable.column('price',width=70,anchor='center')
buytable.column('qty',width=70,anchor='center')



heading2=tk.Label(frame_3,text='Customer Details',font=('times new roman',18,'bold'),bg='#0f4d7d',fg='white')
heading2.pack(fill='x')
yscorll1=ttk.Scrollbar(frame_3,orient='vertical')

billarea=tk.Text(frame_3,yscrollcommand=yscorll1.set)
billarea.place(x=0,y=32,relwidth=0.95,relheight=0.819)

yscorll1.pack(side='right',fill='y')
yscorll1.config(command=billarea.yview)

billframe=tk.Frame(frame_3,bg='white')
billframe.place(x=0,y=520,width=347,height=77)

generatebutton=tk.Button(billframe,width=10,bg='#0f4d7d',fg='white',text='Generate Bill',font=('times new roman',12,'bold'),cursor='hand2',
                         command=lambda:generate())
generatebutton.grid(row=0,column=0,padx=8,pady=16)

printbutton=tk.Button(billframe,width=10,bg='#0f4d7d',fg='white',text='Print',font=('times new roman',12,'bold'),cursor='hand2',
                      command=lambda:print())
printbutton.grid(row=0,column=1,padx=8,pady=16)


clearallbutton=tk.Button(billframe,width=10,bg='#0f4d7d',fg='white',text='Clear All',font=('times new roman',12,'bold'),cursor='hand2',
                         command=lambda:clearall())
clearallbutton.grid(row=0,column=2,padx=8,pady=16)

condb()
showdata()
producttable2.bind('<ButtonRelease-1>', lambda event:select(event,pname2entry,priceentry,qtyentry,instock))
window2.mainloop()