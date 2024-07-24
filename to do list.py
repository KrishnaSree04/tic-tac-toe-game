import random
import tkinter
from tkinter import *
from functools import partial
from tkinter import messagebox
from copy import deepcopy
from PIL import ImageTk, Image
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="sqluser",
  #password="password",
  database="input"
)
cursor = db.cursor()

def register_user():
  # check if username and password fields are not empty
  uid=username_entry.get("1.0", "end-1c")
  if not(inputtxt.get("1.0", "end-1c")):
    messagebox.showerror("Error", "List cannot be empty.")
  else:
    # check if user already exists in the database
            cursor.execute("SELECT * FROM user WHERE user_id = %s", (username_entry.get("1.0", "end-1c"),))
            result = cursor.fetchone()
            if result:
                messagebox.showerror("Error", "Username already exists.")
            else:
                # insert data into the database
                cursor.execute("INSERT INTO user (user_id, password) VALUES (%s, %s)",
                               (username_entry.get("1.0", "end-1c"), password_entry.get()))
                db.commit()
                messagebox.showinfo("Success", "Registration successful.")
                play(uid)
    
#def printInput():
    #inp = inputtxt.get(1.0, "end-1c")


def main():
    root=Tk()
    root.geometry("300x300")
    root.title("To Do List")
    head=Label(root,text="Welcome",bg="Yellow",height=4,width=30)
    b1=Button(root,text="Things You want to do:",bg="Yellow",activebackground="Red",activeforeground="Blue") 
    #b2=Button(root,text="Add here",bg="Yellow",activebackground="Red",activeforeground="Blue") 
    b3=Button(root,text="Submit",bg="Yellow",activebackground="Red",activeforeground="Blue") 
    inputtxt = Text(root,height = 1,width = 20)
    inputtxt.place(x=180,y=180)
    head.pack(side="top")
    b1.pack(side="left")
    b1.place(x=30,y=180)
    #b2.pack(side="left")
    #b2.place(x=30,y=240)
    b3.pack(side="left")
    b3.place(x=30,y=300)
    root.mainloop()
if __name__ == '__main__':
	main()