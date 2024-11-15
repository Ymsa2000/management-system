import tkinter as tk
from tkinter import ttk 
from tkcalendar import DateEntry
import mysql.connector
from tkinter import messagebox
from datetime import date
from employees import employee


def update(category,supplier,name,price,qty,status):
    selected=producttable.selection()
    if not selected:
        messagebox.showerror('error','no data selected')
    else:
        data=producttable.item(selected)
        old_data=data['values']
        old_data=old_data[0]
        query="""SELECT * FROM products WHERE id=%s"""
        mycursor.execute(query,(old_data,))
        fetched_data=mycursor.fetchone()
        fetched_data=fetched_data[1:]
        
        new_data=(category.get(),supplier.get(),name.get(),price.get(),qty.get(),status.get())
        print(fetched_data)
        print(new_data)

        if new_data==fetched_data:
            messagebox.showerror('error','no changes has been made')
        else:
            query="""UPDATE products SET category=%s , supplier=%s,name=%s,price=%s,qty=%s,status=%s WHERE id=%s"""
            values=(category.get(),supplier.get(),name.get(),price.get(),qty.get(),status.get(),old_data)
            mycursor.execute(query,values)
            db.commit()
            messagebox.showinfo('success','data has been updated')
            showdata()
            clear(category,supplier,name,price,qty,status,False)
            


def selectdata(event,category,supplier,name,price,qty,status):
    index=producttable.focus()
    data=producttable.item(index)
    row=data['values']
    clear(category,supplier,name,price,qty,status,False)
    category.set(row[1])
    supplier.set(row[2])
    name.insert(0,row[3])
    price.insert(0,row[4])
    qty.insert(0,row[5])
    status.set(row[6])
    



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
    query="""CREATE TABLE IF NOT EXISTS products (id INT AUTO_INCREMENT PRIMARY KEY,category VARCHAR(100) , supplier VARCHAR(100),name VARCHAR(100),
                price VARCHAR(100),qty VARCHAR(100),status VARCHAR(100))"""
    mycursor.execute(query)
    db.commit()




def category_fetch():
    """Fetches categories from the database and populates the category combobox."""
    category_list = []
    query = """SELECT category_name FROM categories"""
    mycursor.execute(query)
    names = mycursor.fetchall()
    
    for name in names:
        category_list.append(name[0])
    
    categoryentry.config(values=category_list)
    
    
def search(searchby,value):
    if searchby.get()=='Select':
        messagebox.showerror('error','please choose search data type')
    elif value.get() =="":
        messagebox.showerror('error','please insert search value')
    else :
        try:
            searchby=searchby.get()
            value=value.get()
            query=f"""SELECT * FROM products WHERE {searchby} LIKE %s """
            data=(f'%{value}%',)
            mycursor.execute(query,data)
            fetched_data=mycursor.fetchall()
            if not fetched_data:
                messagebox.showerror('error','no data found')
                showdata()
            else:
                producttable.delete(*producttable.get_children())
                for x in fetched_data:
                    producttable.insert("",tk.END,values=x)
        except Exception as e :
            messagebox.showerror('error',e)

def supplier_fetch(event):
    """Fetch suppliers based on the selected category and update the supplier combobox."""
    supplier_list = []
    query = """SELECT supplier_name FROM suppliers WHERE description LIKE %s"""
    mycursor.execute(query, (f'%{categoryentry.get()}%',))
    suppliernames = mycursor.fetchall()

    for name in suppliernames:
        supplier_list.append(name[0])
    
    supplierentry.config(values=supplier_list)




def addproduct(category,supplier,name,price,qty,status):
    if category=='Select':
        messagebox.showerror('error','Choose or add Category')
    elif supplier=='Select':
        messagebox.showerror('error','Choose or add Supplier')
    elif status=='Select':
        messagebox.showerror('error','Choose Status')        
    elif name=='' or price=='' or qty=='':
        messagebox.showerror('error','fill the data')        
    else : 
        query="""INSERT INTO products (category,supplier,name,price,qty,status) VALUES (%s,%s,%s,%s,%s,%s)"""
        data=(category,supplier,name,price,qty,status)
        mycursor.execute(query,data)
        db.commit()
        messagebox.showinfo('success','data has been added')
        showdata()
        


def showdata():
    query="""SELECT * FROM products """
    mycursor.execute(query)
    fetched_data=mycursor.fetchall()
    producttable.delete(*producttable.get_children())
    for x in fetched_data:
        producttable.insert("",tk.END,values=x)    


def delete(category,supplier,name,price,qty,status):
    selected=producttable.selection()
    if not selected:
        messagebox.showerror('error','no data selected')
    else:
        data_1=producttable.item(selected)
        row=data_1['values']
        id=row[0]
        data=(id)
        query="""DELETE FROM products WHERE id=%s """
        mycursor.execute(query,(data,))
        db.commit()
        messagebox.showinfo('success','data has been deleted')
        clear(category,supplier,name,price,qty,status,True)
        showdata()
        

def clear(category,supplier,name,price,qty,status,check):
    category.set('Select')
    supplier.set('Select')
    name.delete(0,tk.END)
    price.delete(0,tk.END)
    qty.delete(0,tk.END)
    status.set('Empty')
    if check:
        producttable.selection_remove(producttable.focus())

    

def product(window):
    global backimage ,categoryentry,supplierentry,nameentry,quantityentry,priceentry,statusentry,producttable

    productwindow=tk.Frame(window,bg='white')
    productwindow.place(x=250,y=98,width=950,height=622)


    backimage=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\arrow.png')
    backbutton=tk.Button(productwindow,image=backimage,bd=3,width=40,command=lambda: productwindow.place_forget())
    backbutton.place(x=5,y=40)


    leftframe=tk.Frame(productwindow,bg='white',bd=2,relief='ridge')
    leftframe.place(x=10,y=70,height=500,width=400)

    rightframe=tk.Frame(productwindow,bg='white')
    rightframe.place(x=430,y=150,width=490,height=430)

    headinglabel=tk.Label(leftframe,text='Manage Product Details',font=('times new roman',20,'bold'),bg='#0f4d7d',fg='white')
    headinglabel.place(x=0,y=0,relwidth=1)


    category=tk.Label(leftframe,text='Category ',font=('times new roman ',12,'bold'),bg='white')
    categoryentry=ttk.Combobox(leftframe,values=(),state='readonly',width=20,height=20,font=('times new roman ',12,'bold'))
    categoryentry.set('Select')

    category.place(x=20,y=50)
    categoryentry.place(x=120,y=50)

    supplier=tk.Label(leftframe,text='Supplier',font=('times new roman ',12,'bold'),bg='white')
    supplierentry=ttk.Combobox(leftframe,values=(),state='readonly',width=20,font=('times new roman ',12,'bold'))
    supplierentry.set('Select')
    supplier.place(x=20,y=100)
    supplierentry.place(x=120,y=100)

    name=tk.Label(leftframe,text='Name',font=('times new roman ',12,'bold'),bg='white')
    nameentry=tk.Entry(leftframe,width=35,bg='lightyellow')
    name.place(x=20,y=150)
    nameentry.place(x=120,y=150)

    price=tk.Label(leftframe,text='Price',font=('times new roman ',12,'bold'),bg='white')
    priceentry=tk.Entry(leftframe,width=35,bg='lightyellow')
    price.place(x=20,y=200)
    priceentry.place(x=120,y=200)

    quantity=tk.Label(leftframe,text='Qty',font=('times new roman ',12,'bold'),bg='white')
    quantityentry=tk.Entry(leftframe,width=35,bg='lightyellow')
    quantity.place(x=20,y=250)
    quantityentry.place(x=120,y=250)

    status=tk.Label(leftframe,text='Status',font=('times new roman ',12,'bold'),bg='white')
    statusentry=ttk.Combobox(leftframe,values=('Active','Inactive'),state='readonly',width=20,font=('times new roman ',12,'bold'))
    statusentry.set('Select')
    status.place(x=20,y=300)
    statusentry.place(x=120,y=300)

    button1=tk.Button(leftframe,text='Save',width=9,font=('times new roman',10,'bold'),bg='#0f4d7d',fg='white',command=lambda:
                      addproduct(categoryentry.get(),supplierentry.get(),nameentry.get(),priceentry.get(),quantityentry.get(),statusentry.get())
                      )
    button1.place(x=20,y=400)

    button2=tk.Button(leftframe,text='Update',width=9,font=('times new roman',10,'bold'),bg='#0f4d7d',fg='white',command=lambda:
                      update(categoryentry,supplierentry,nameentry,priceentry,quantityentry,statusentry)
                      
                      )
    button2.place(x=110,y=400)
    
    button3=tk.Button(leftframe,text='Delete',width=9,font=('times new roman',10,'bold'),bg='#0f4d7d',fg='white',command=lambda:
                      delete(categoryentry,supplierentry,nameentry,priceentry,quantityentry,statusentry))
    
    button3.place(x=200,y=400)
    
    button4=tk.Button(leftframe,text='Clear',width=9,font=('times new roman',10,'bold'),bg='#0f4d7d',fg='white',command=lambda:clear(
        categoryentry,supplierentry,nameentry,priceentry,quantityentry,statusentry,True
    )
                      )
    
    button4.place(x=290,y=400)

    search_frame=tk.LabelFrame(productwindow,text='Search Product',font=('times new roman',14),bg='white')
    search_frame.place(x=430,y=60)

    search_combobox=ttk.Combobox(search_frame,values=('category','supplier','name','status'),state='readonly')
    search_combobox.grid(row=0,column=0,padx=10)
    search_combobox.set('Select')

    searchentry=tk.Entry(search_frame,width=17,bg='lightyellow')
    searchentry.grid(row=0,column=1,padx=10,pady=10)

    searchbutton=tk.Button(search_frame,text='Search',width=8,font=('times new roman',11,'bold'),bg='#0f4d7d',fg='white'
                           ,command=lambda: search(search_combobox,searchentry))
    searchbutton.grid(row=0,column=3,padx=10,pady=10)
    
    showallbutton=tk.Button(search_frame,text='Show All',width=8,font=('times new roman',11,'bold'),bg='#0f4d7d',fg='white',command=lambda:showdata())
    showallbutton.grid(row=0,column=4,padx=10,pady=10)

    xscorll=ttk.Scrollbar(rightframe,orient='horizontal')
    yscroll=ttk.Scrollbar(rightframe,orient='vertical')
    
    

    producttable=ttk.Treeview(rightframe,columns=('id','category','supplier','name','price','qty','status'),show='headings',
                               yscrollcommand=yscroll.set,xscrollcommand=xscorll.set)
    
    producttable.place(relwidth=0.95,relheight=0.9)
    xscorll.pack(side='bottom',fill='x')
    yscroll.pack(side='right',fill='y')
    xscorll.config(command=producttable.xview)
    yscroll.config(command=producttable.yview)

    producttable.heading('id',text='ID')
    producttable.heading('category',text='Category ')
    producttable.heading('supplier',text='Supplier')
    producttable.heading('name',text='Name')
    producttable.heading('price',text='Price')
    producttable.heading('qty',text='Qty')
    producttable.heading('status',text='Status')

    producttable.column('id',width=40)
    producttable.column('category',width=110)
    producttable.column('supplier',width=150)
    producttable.column('name',width=150)
    producttable.column('price',width=60)
    producttable.column('qty',width=60)
    producttable.column('status',width=100)

    # Connect to the database
    conncectdb()

    # Fetch categories initially
    category_fetch()

    # Bind the category selection change event to update suppliers
   

    # Display the data in the table
    showdata()

    # Bind table selection to the selectdata function
    producttable.bind('<ButtonRelease-1>', lambda event: selectdata(event, categoryentry, supplierentry, nameentry, priceentry, quantityentry, statusentry))
    categoryentry.bind('<<ComboboxSelected>>', supplier_fetch)

