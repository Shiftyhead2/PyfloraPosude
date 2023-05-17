from tkinter import *
from tkinter import messagebox
from pages.login import LoginPage
from pages.register import RegisterPage
import sqlite3
import os
import bcrypt


class AppController:
    def __init__(self,root):
        self.root = root

        self.db_path = os.path.join('database','users.db')
        self.create_user_table()


        padding_frame = Frame(root, padx=50, pady=50)
        padding_frame.grid(row=0, column=0)

        self.login_page = LoginPage(padding_frame, self)
        self.register_page = RegisterPage(padding_frame, self)

        self.switch_to_login()
    
    def create_user_table(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute('''
          CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            surname TEXT,
            username TEXT,
            password TEXT
          )''')
        
        conn.commit()
        conn.close()
        
    def switch_to_register(self):
        self.login_page.hide()
        self.register_page.show()

    def switch_to_login(self):
        self.register_page.hide()
        self.login_page.show()
    
    def register_user(self,name,surname,username,password):
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        

        cursor.execute(''' 
            INSERT INTO users(name,surname,username,password)
            VALUES(?,?,?,?)
        ''',(name,surname,username,hashed_password.decode('utf-8')))

        conn.commit()
        conn.close()

        messagebox.showinfo("Registration successful","You have sucessfully registered to the app!")
        self.switch_to_login()
    
    def login_user(self,username,password):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username=?",(username,))
        result = cursor.fetchone()

        conn.close()

        if result is None:
            messagebox.showerror("Login failed!", "Invalid username,password or the account doesn't exist!")
        else:
            hashed_saved_password = result[0].encode('utf-8')

            if bcrypt.checkpw(password.encode('utf-8'),hashed_saved_password):
                messagebox.showinfo("Login succesfull!", "You have sucessfully logged in!")
                #Logic for showing the main plant page
            else:
                messagebox.showerror("Login failed!", "Invalid username or password")

    
        


def main():
    root = Tk()
    root.title("PyFlora Posuda")   

    app = AppController(root)

    root.mainloop()
    

if __name__ == "__main__":

    os.makedirs("database",exist_ok=True)

    main()