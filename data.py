# Tic Tac Toe game with GUI
# using tkinter

# importing all necessary libraries
import random
import tkinter
from tkinter import *
from functools import partial
from tkinter import messagebox
from copy import deepcopy
from PIL import ImageTk, Image

# sign variable to decide the turn of which player
sign = 0

# Creates an empty board
global board
board = [[" " for x in range(3)] for y in range(3)]

# Check l(O/X) won the match or not
# according to the rules of the game
import mysql.connector

db = mysql.connector.connect(
  host="localhost",
  user="sqluser",
  password="password",
  database="tic_tac_toe"
)
cursor = db.cursor()

def login():
 global login_screen
 login_screen = Tk()
 login_screen.title("Login")
 login_screen.geometry("1200x1200")
 login_screen.configure(background="#90EE90")
 
 username_label = Label(login_screen,font=150, text="Username * ",bg="#90EE90")
 username_entry = Text(login_screen,height=2,width=30,wrap=NONE,font=30)
 password_label = Label(login_screen,font=150,text="Password * ",bg="#90EE90")
 password_entry = Entry(login_screen,width=30,font=30, show="*")

 username_label.place(x=150,y=130)
 username_entry.place(x=300,y=120)
 password_label.place(x=150,y=250)
 password_entry.place(x=300,y=240) 
 
 #new user
 def register_user():
  # check if username and password fields are not empty
  uid=username_entry.get("1.0", "end-1c")
  if not(username_entry.get("1.0", "end-1c")) or not (password_entry.get()):
    messagebox.showerror("Error", "Username and password fields cannot be empty.")
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
    

#Existing user
 def login_user():
  # check if username and password fields are not empty
  uid=username_entry.get("1.0", "end-1c")
  if not(username_entry.get("1.0", "end-1c")) or not (password_entry.get()):
    messagebox.showerror("Error", "Username and password fields cannot be empty.")
  else:
    # check if user exists in the database
    cursor.execute("SELECT * FROM user WHERE user_id = %s AND password = %s",
                   (username_entry.get("1.0", "end-1c"), password_entry.get()))
    user = cursor.fetchone()
    if user is not None:
      messagebox.showinfo("Success", "Login successful.")
      play(uid)
    else:
      messagebox.showerror("Error", "Invalid username or password.")
    db.commit()  
    
 # register and login buttons    
 register_button = Button(login_screen, text="Register", width=10, height=1, bg="#ffffff", fg="red", font=20, command=register_user).place(x=250,y=400)
 login_button = Button(login_screen, text="Login", width=10, height=1, bg="#ffffff", fg="red", font=20, command=login_user).place(x=400,y=400) 
 login_screen.mainloop()

def winner(b, l):
    return ((b[0][0] == l and b[0][1] == l and b[0][2] == l) or
            (b[1][0] == l and b[1][1] == l and b[1][2] == l) or
            (b[2][0] == l and b[2][1] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][0] == l and b[2][0] == l) or
            (b[0][1] == l and b[1][1] == l and b[2][1] == l) or
            (b[0][2] == l and b[1][2] == l and b[2][2] == l) or
            (b[0][0] == l and b[1][1] == l and b[2][2] == l) or
            (b[0][2] == l and b[1][1] == l and b[2][0] == l))


def isfree(i, j):
    return board[i][j] == " "

# Check the board is full or not


def isfull():
    flag = True
    for i in board:
        if(i.count(' ') > 0):
            flag = False
    return flag

# Decide the next move of system


def pc():
    possiblemove = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == ' ':
                possiblemove.append([i, j])
    move = []
    if possiblemove == []:
        return
    else:
        for let in ['O', 'X']:
            for i in possiblemove:
                boardcopy = deepcopy(board)
                boardcopy[i[0]][i[1]] = let
                if winner(boardcopy, let):
                    return i
        corner = []
        for i in possiblemove:
            if i in [[0, 0], [0, 2], [2, 0], [2, 2]]:
                corner.append(i)
        if len(corner) > 0:
            move = random.randint(0, len(corner)-1)
            return corner[move]
        edge = []
        for i in possiblemove:
            if i in [[0, 1], [1, 0], [1, 2], [2, 1]]:
                edge.append(i)
        if len(edge) > 0:
            move = random.randint(0, len(edge)-1)
            return edge[move]

# Configure text on button while playing with system


def get_text_pc(uid,i, j, gb, l1,l2):
    global sign
    if board[i][j] == ' ':
        if sign % 2 == 0:
            l1.config(state=DISABLED)
            l2.config(state=ACTIVE)
            board[i][j] = "X"
        else:
            button[i][j].config(state=ACTIVE)
            l2.config(state=DISABLED)
            l1.config(state=ACTIVE)
            board[i][j] = "O"
        sign += 1
        button[i][j].config(text=board[i][j])
    x = True
    if winner(board, "X"):
        gb.destroy()
        x = False
        cursor.execute("SELECT score FROM user WHERE user_id=%s", (uid,))
        user_score = cursor.fetchone()[0]
        box = messagebox.showinfo("Winner", "Player won the match")
        sq = "UPDATE user SET score = %s WHERE user_id = %s" 
        values = ((str(int(user_score)+1)),uid)
        cursor.execute(sq,values)
        messagebox.showinfo("Success", "Highest score updated")

    elif winner(board, "O"):
        gb.destroy()
        x = False
        box = messagebox.showinfo("Winner", "Computer won the match")
    elif(isfull()):
        gb.destroy()
        x = False
        box = messagebox.showinfo("Tie Game", "Tie Game")
    if(x):
        if sign % 2 != 0:
            move = pc()
            button[move[0]][move[1]].config(state=DISABLED)
            get_text_pc(uid,move[0], move[1], gb, l1,l2)

# Create the GUI of game board for play along with system


def gameboard_pc(game_board, l1,l2,uid):
    global button
    button = []
    for i in range(3):
        m = 3+i
        button.append(i)
        button[i] = []
        for j in range(3):
            n = j
            button[i].append(j)
            get_t = partial(get_text_pc,uid, i, j, game_board, l1,l2)
            button[i][j] = Button(
                game_board, bd=5, command=get_t, height=4, width=8)
            button[i][j].grid(row=m, column=n)
    game_board.mainloop()

# Initialize the game board to play with system


def withpc(uid,game_board):
    game_board.destroy()
    game_board = Tk()
    game_board.title("Tic Tac Toe")
    l1 = Button(game_board, text="Player : X", width=10)
    l1.grid(row=1, column=1)
    l2 = Button(game_board, text="Computer : O",
                width=10, state=DISABLED)

    l2.grid(row=2, column=1)
    gameboard_pc(game_board, l1, l2,uid)


# main function
def play(uid):
    login_screen.destroy()
    menu = Tk()
    menu.geometry("1550x1250")
    menu.title("Tic Tac Toe")
    menu.configure(background="#90EE90")
    #Declaring the commands when buttons Pressed

    wpc = partial(withpc,uid, menu)
    #wpl = partial(withplayer, menu)
    menu.option_add( "*font", "lucida 20 bold italic" )
    
    cursor = db.cursor()
    cursor.execute("SELECT score FROM user WHERE user_id=%s", (uid,))
    user_score = cursor.fetchone()[0]
    #Display Image
    #img = PhotoImage(file='pic.png')
    #labe = Label(menu, image = img)
    #labe.place(x=0,y=0)
    #img1 = PhotoImage(file='tac.png.py')
    #label = Label(menu, image = img1)
    #head = Button(menu, text="---Welcome to tic-tac-toe---",
    #            activeforeground='red',
     #           activebackground="#90EE90", bg="#90EE90",
      #          fg="red", height=3,width=30, font='Helvetica')
    head= Label(menu,font=300,text="---Welcome to tic-tac-toe---",bg="#90EE90",fg="red")
   # head.grid
    B1 = Button(menu, text="Single Player", command=wpc,
                activeforeground='red',
                activebackground="yellow", bg="Green",
                fg="yellow",height=2, width=20, font='summer')

    B3 = Button(menu, text="Exit", command=menu.quit, activeforeground='red',
                activebackground="yellow", bg="Green", fg="yellow",height=2,
                width=20, font='summer')
    #menu.resizable(False, False)
    head.pack(side='top')
    #labe.pack(side='top')
    B1.pack(side='left')
    B1.place(x=30,y=180)
    B3.pack(side='left')
    B3.place(x=30,y=380)
    highest_score_indicater=Label(menu,font=60,text="HIGHEST SCORE:",bg="#90EE90",fg="black")
    highest_score_indicater.place(x=1150,y=100)
    highestScore=Label(menu, text=f"{user_score}",font=100,bg="#90EE90",fg="red")
    highestScore.place(x=1350,y=100)

    #label.pack(side="top")
    #label.place(x=400,y=140)
    menu.mainloop()
login()

# Call main function
#if __name__ == '__main__':
    #play()