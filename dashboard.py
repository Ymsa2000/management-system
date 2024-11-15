import tkinter as tk
import time
from tkinter import ttk 
from tkcalendar import DateEntry
from employees import employee
from supplier_form import supplier
from category_form import category
from product_form import product
from sales_form import sales
import os
#functions

#employee fuctions


def logout():
    timelabel.after_cancel(clockid)
    window.destroy()
    import login
    
#clock
def exit():
    window.destroy()
def clock():
    global clockid
    currentdate=time.strftime('%d/%m/%Y')
    currenttime= time.strftime('%H:%M:%S')
    timelabel.config(text=f'Welcome admin \t\tdate:{currentdate}\t\ttime:{currenttime}')
    clockid=timelabel.after(1000,clock)
#window
window=tk.Tk()
window.geometry('1200x720+150+40')
window.title('Sign IN')
window.resizable(False,False)
#frame
frame1=tk.Frame()
frame1.place(x=0,y=180,width=250,height=600)
# frame1.config(bg='white')

image1=tk.PhotoImage(file='inventory.png')
imslabel=tk.Label(window,image=image1,compound='right' ,text='Inventory Managment System',font=('times new roman',30,'bold'),bg='#010c48',fg='white',anchor='w',padx=20)
imslabel.place(x=0,y=0,relwidth=1)

logoutlabel=tk.Button(window,text='Logout',font=('times new roman',20,'bold'),fg='#010c48',command=lambda:logout())
logoutlabel.place(x=1050,y=10)

timelabel=tk.Label(window,font=('times new roman',15,'bold'),fg='#010c48',bg='grey')
timelabel.place(x=0,y=70,relwidth=1)
clock()
 
book=tk.PhotoImage(file='books.png')
booklabel=tk.Label(frame1,image=book)
booklabel.pack()
menulabel=tk.Label(frame1,text='Menu',font=('times new roman',20,'bold'),bg='#009688',fg='white')
menulabel.pack(fill='x')

employeeimage=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\man.png')
employeelabel=tk.Button(frame1,text='Employees',font=('times new roman',20,'bold'),image=employeeimage,compound='left',bd=5,anchor='w',padx=10,command=lambda:employee(window))
employeelabel.pack(fill='x')

supplierimage=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\tracking.png')
supplierlabel=tk.Button(frame1,text='Supplier',font=('times new roman',20,'bold'),image=supplierimage,compound='left',bd=5,anchor='w',padx=10,command=lambda:supplier(window))
supplierlabel.pack(fill='x')

categoryimage=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\categorization.png')
categorylabel=tk.Button(frame1,text='Category',font=('times new roman',20,'bold'),image=categoryimage,compound='left',bd=5,anchor='w',padx=10,command=lambda:category(window))
categorylabel.pack(fill='x')

productimage=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\package.png')
productlabel=tk.Button(frame1,text='Product',font=('times new roman',20,'bold'),image=productimage,compound='left',bd=5,anchor='w',padx=10,command=lambda:product(window))
productlabel.pack(fill='x')

salesimage=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\trend.png')
saleslabel=tk.Button(frame1,text='Sales',font=('times new roman',20,'bold'),image=salesimage,compound='left',bd=5,anchor='w',padx=10,
                     command=lambda:sales(window))
saleslabel.pack(fill='x')

exitimage=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\logout.png')
exitlabel=tk.Button(frame1,text='EXIT',font=('times new roman',20,'bold'),image=exitimage,compound='left',bd=5,anchor='w',padx=10,command=lambda:exit())
exitlabel.pack(fill='x')


frame_1=tk.Frame(window,bg='#2C3E50',bd=3,relief='ridge')
frame_1.place(x=370,y=140,width=250,height=150)
frame_1image=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\employee.png')
frame_1label=tk.Label(frame_1,image=frame_1image,bg='#2C3E50')
frame_1label.pack()
frame_1text=tk.Label(frame_1,text='Employees',font=('times new roman',20,'bold'),bg='#2C3E50',fg='white')
frame_1text.pack()
frame_1no=tk.Label(frame_1,text='0',font=('times new roman',30,'bold'),bg='#2C3E50',fg='white')
frame_1no.pack()


frame_2=tk.Frame(window,bg='#8e44ad',bd=3,relief='ridge')
frame_2.place(x=700,y=140,width=250,height=150)
frame_2image=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\supplier.png')
frame_2label=tk.Label(frame_2,image=frame_2image,bg='#8e44ad')
frame_2label.pack()
frame_2text=tk.Label(frame_2,text='Total Suppliers',font=('times new roman',20,'bold'),bg='#8e44ad',fg='white')
frame_2text.pack()
frame_2no=tk.Label(frame_2,text='0',font=('times new roman',30,'bold'),bg='#8e44ad',fg='white')
frame_2no.pack()


frame_3=tk.Frame(window,bg='#27ae60',bd=3,relief='ridge')
frame_3.place(x=370,y=340,width=250,height=150)
frame_3image=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\cate.png')
frame_3label=tk.Label(frame_3,image=frame_3image,bg='#27ae60')
frame_3label.pack()
frame_3text=tk.Label(frame_3,text='Categories',font=('times new roman',20,'bold'),bg='#27ae60',fg='white')
frame_3text.pack()
frame_3no=tk.Label(frame_3,text='0',font=('times new roman',30,'bold'),bg='#27ae60',fg='white')
frame_3no.pack()


frame_4=tk.Frame(window,bg='#e74c3c',bd=3,relief='ridge')
frame_4.place(x=700,y=340,width=250,height=150)
frame_4image=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\products.png')
frame_4label=tk.Label(frame_4,image=frame_4image,bg='#e74c3c')
frame_4label.pack()
frame_4text=tk.Label(frame_4,text='Products',font=('times new roman',20,'bold'),bg='#e74c3c',fg='white')
frame_4text.pack()
frame_4no=tk.Label(frame_4,text='0',font=('times new roman',30,'bold'),bg='#e74c3c',fg='white')
frame_4no.pack()


frame_5=tk.Frame(window,bg='#2C3E50',bd=3,relief='ridge')
frame_5.place(x=540,y=530,width=250,height=150)
frame_5image=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\trends.png')
frame_5label=tk.Label(frame_5,image=frame_5image,bg='#2C3E50')
frame_5label.pack()
frame_5text=tk.Label(frame_5,text='Sales',font=('times new roman',20,'bold'),bg='#2C3E50',fg='white')
frame_5text.pack()
frame_5no=tk.Label(frame_5,text='0',font=('times new roman',30,'bold'),bg='#2C3E50',fg='white')
frame_5no.pack()









window.mainloop()