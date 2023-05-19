from tkinter import *
from tkinter import messagebox
from pages.login import LoginPage
from pages.register import RegisterPage
from pages.plantviewheader import PlantViewHeader
import sqlite3
import os
import bcrypt


class AppController:
    def __init__(self,root):
        self.root = root

        self.db_user_path = os.path.join('database','users.db')
        self.db_plant_path = os.path.join('database','plants.db')
        self.create_user_table()
        self.create_plant_table()

        self.pages = {
            "login": LoginPage(self.root,self),
            "register":RegisterPage(self.root,self),
            "plant_view_header": PlantViewHeader(self.root,self)
        }

        self.current_pages = []

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.switch_to_page("login")
    
    def switch_to_page(self,*page_names):
        pages = [self.pages.get(page_name) for page_name in page_names]
        if all(pages):
            for page in self.current_pages:
                page.hide()
            self.current_pages = pages

            for page in self.current_pages:
                page.show()
        else:
            messagebox.showerror("Critical Error!",f"One or more pages could not be found: {page_names}")
    
    def switch_to_register(self):
        self.switch_to_page("register")

    def switch_to_login(self):
        self.switch_to_page("login")

    def switch_to_plant_view(self):
        self.switch_to_page("plant_view_header")
    

    def create_plant_table(self):
        conn = sqlite3.connect(self.db_plant_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plants(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                picture BLOB,
                soil_moisture FLOAT,
                ideal_temperature FLOAT,
                substrate_recommendation TEXT
            )  
        ''')


        conn.commit()
        conn.close()

    
    def create_user_table(self):
        conn = sqlite3.connect(self.db_user_path)
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
        
    
    def register_user(self,name,surname,username,password):
        if not name or not surname or not username or not password:
            messagebox.showerror("Registration failed!","Please enter all the values")
            return


        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        conn = sqlite3.connect(self.db_user_path)
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
        if not username or not password:
            messagebox.showerror("Login failed!", "Please enter the login values")
            return


        conn = sqlite3.connect(self.db_user_path)
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username=?",(username,))
        result = cursor.fetchone()

        conn.close()

        if result is None:
            messagebox.showerror("Login failed!", "Invalid username or password!")
        else:
            hashed_saved_password = result[0].encode('utf-8')

            if bcrypt.checkpw(password.encode('utf-8'),hashed_saved_password):
                messagebox.showinfo("Login succesfull!", "You have sucessfully logged in!")
                #Logic for showing the main plant page
                self.switch_to_plant_view()
            else:
                messagebox.showerror("Login failed!", "Invalid username or password")

    
        


def main():
    root = Tk()
    root.title("PyFlora")
    root.geometry("640x480")
    root.eval('tk::PlaceWindow . center')

    app = AppController(root)

    root.mainloop()
    

if __name__ == "__main__":
    os.makedirs("database",exist_ok=True)

    main()