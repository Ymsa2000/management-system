import tkinter as tk
import time
from tkinter import ttk 
from tkcalendar import dateentry
from tkinter import messagebox
import mysql.connector

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

def loginn():

    if empidentry.get()=="" or passwordentry.get()=="" or usertypeentry.get()=="Select":
        messagebox.showerror('error','Please fill the enteries')
    else:
        if usertypeentry.get()=='Admin':
            query=""" SELECT * FROM employeesdata WHERE user_type=%s AND empid=%s AND password=%s """
            data=(usertypeentry.get(),empidentry.get(),passwordentry.get())
            mycursor.execute(query,data)
            fetched_data=mycursor.fetchone()
            if not fetched_data:
                messagebox.showerror('error','Emp id or Password is Wrong')
            else:
                window1.destroy()
                import dashboard
        else:
            query=""" SELECT * FROM employeesdata WHERE user_type=%s AND empid=%s AND password=%s """
            data=(usertypeentry.get(),empidentry.get(),passwordentry.get())
            mycursor.execute(query,data)
            fetched_data=mycursor.fetchone()
            if not fetched_data:
                messagebox.showerror('error','Emp id or Password is Wrong')
            else:
                window1.destroy()
                import sell






window1=tk.Tk()
window1.geometry('1200x720+150+40')
window1.title('Sign IN')
window1.resizable(False,False)
window1.config(bg='white')


heading=tk.Label(window1,font=('times new roman',25,'bold'),bg='#0f4d7d',fg='white',text='Enterprise Managing System')
heading.pack(fill='x',anchor='center')

left_frame=tk.Frame(window1,bg='white')
left_frame.place(x=60,y=90,width=600,height=600)

right_frame=tk.Frame(window1,bd=2,relief='ridge',bg='#0f4d7d')
right_frame.place(x=760,y=130,width=350,height=500)

def photo1():
    global image1, image1label,id1
    image1=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\coordinator.png')
    image1label=tk.Label(left_frame,image=image1,bg='white')
    image1label.pack()


# def photo2():
#     global image2 ,image2label,id2
#     image1label.destroy()
#     image2=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\task-management.png')
#     image2label=tk.Label(left_frame,image=image2,bg='white')
#     image2label.pack()
#     id2=image2label.after(4000,photo3)

# def photo3():
#     global image3,image3label,id3
#     image2label.destroy()
#     image3=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\time.png')
#     image3label=tk.Label(left_frame,image=image3,bg='white')
#     image3label.pack()
#     id3=image3label.after(4000,photo4)

# def photo4():
#     global image4,image4label,id4
#     image3label.destroy()
#     image4=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\planning.png')
#     image4label=tk.Label(left_frame,image=image4,bg='white')
#     image4label.pack()
#     id4=image4label.after(4000,destroy4)

# def destroy4():
#     global id5
#     image4label.destroy()
#     id5=left_frame.after(1,photo1)
    
photo1()

loginimage=tk.PhotoImage(file='C:\\Users\\ymsa2\\OneDrive\\Desktop\\projects\\inventory managment\\user.png')
loginlogo=tk.Label(right_frame,image=loginimage,bg='#0f4d7d')
loginlogo.pack()

empidlabel=tk.Label(right_frame,font=('times new roman',12,'bold'),fg='white',text='Employee Id',bg='#0f4d7d')
empidlabel.place(x=120,y=140)

empidentry=tk.Entry(right_frame,font=('times new roman',12,'bold'),fg='black')
empidentry.place(x=90,y=170)

passwrodlabel=tk.Label(right_frame,font=('times new roman',12,'bold'),fg='white',text='Password',bg='#0f4d7d')
passwrodlabel.place(x=120,y=240)

passwordentry=tk.Entry(right_frame,font=('times new roman',12,'bold'),fg='black')
passwordentry.place(x=90,y=270)

usertypelabel=tk.Label(right_frame,font=('times new roman',12,'bold'),fg='white',text='User type',bg='#0f4d7d')
usertypelabel.place(x=120,y=340)

usertypeentry=ttk.Combobox(right_frame,font=('times new roman',12,'bold'),values=('Admin','Employee'),state='readonly')
usertypeentry.place(x=90,y=370)
usertypeentry.set('Select')

loginbutton=tk.Button(right_frame,font=('times new roman',12,'bold'),fg='white',text='Log In',bg='green',width=11,bd=2,cursor='hand2',
                      command=lambda:loginn())
loginbutton.place(x=120,y=440)



condb()
window1.mainloop()