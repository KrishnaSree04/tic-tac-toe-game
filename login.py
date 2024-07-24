def login():
 global login_screen
 login_screen = Tk()
 login_screen.title("Login")
 login_screen.geometry("700x500")
 login_screen.configure(background="#9b59b6")
 
 username_label = Label(login_screen,font=150, text="Username * ",bg="#9b59b6")
 username_entry = Text(login_screen,height=2,width=30,wrap=NONE,font=30)
 password_label = Label(login_screen,font=150,text="Password * ",bg="#9b59b6")
 password_entry = Entry(login_screen,width=30,font=30, show="*")

 username_label.place(x=150,y=130)
 username_entry.place(x=300,y=120)
 password_label.place(x=150,y=250)
 password_entry.place(x=300,y=240)
 
 def home():
   # check if username and password fields are not empty
  uid=username_entry.get("1.0", "end-1c")
  if not(username_entry.get("1.0", "end-1c")) or not (password_entry.get()):
    messagebox.showerror("Error", "Username and password fields cannot be empty.")
  else:  
    # insert data into the database
    cursor.execute("INSERT INTO user (user_id, password) VALUES (%s, %s)",
                   (username_entry.get("1.0", "end-1c"), password_entry.get()))
    db.commit()
    db.close
    messagebox.showinfo("Success", "Data inserted successfully.")
    startgame(uid)

 def startgame(uid):
  login_screen.destroy()
  root = Tk()
  root.title("Rock Paper Scissor")
  root.configure(background="#9b59b6")
