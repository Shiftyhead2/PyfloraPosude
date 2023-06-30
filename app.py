from tkinter import *
from tkinter import messagebox
from pages.login import LoginPage
from pages.register import RegisterPage
from pages.plantviewheader import PlantViewHeader
from pages.plantsview import PlantsView
from pages.plantsform import PlantsForm
from pages.individualplantview import IndividualPlantView
import sqlite3
import os
import bcrypt
import shutil


IMAGES_FOLDER = "images"

class AppController:
    def __init__(self,root):
        self.root = root

        

        self.db_user_path = os.path.join('database','users.db')
        self.db_plant_path = os.path.join('database','plants.db')
        self.create_user_table()
        self.create_plant_table()

        self.plant_id = None

        self.pages = {
            "login": LoginPage(self.root,self),
            "register":RegisterPage(self.root,self),
            "plant_view_header": PlantViewHeader(self.root,self),
            "plants_view": PlantsView(self.root,self),
            "plants_form": PlantsForm(self.root,self),
            "plant_view": IndividualPlantView(self.root,self)
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
                page.show(self.plant_id)
        else:
            messagebox.showerror("Critical Error!",f"One or more pages could not be found: {page_names}")
    
    def switch_to_register(self):
        self.switch_to_page("register")

    def switch_to_login(self):
        self.switch_to_page("login")

    def switch_to_plant_view(self):
        self.switch_to_page("plant_view_header","plants_view")
        self.plant_id = None
    
    def switch_to_plant_form(self):
        self.switch_to_page("plants_form")
        
    

    def create_plant_table(self):
        conn = sqlite3.connect(self.db_plant_path)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS plants(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                picture TEXT,
                soil_moisture TEXT,
                ideal_temperature REAL,
                ideal_light REAL,
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
            messagebox.showerror("Registracija ne uspješna!","Molimo vas unesite sve podatke!")
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

        messagebox.showinfo("Registracija uspješna!","Uspješno ste se registrilali u aplikaciju!")
        self.switch_to_login()
    
    def login_user(self,username,password):
        if not username or not password:
            messagebox.showerror("Prijava nije uspjela!", "Molimo vas unesite sve podatke!")
            return


        conn = sqlite3.connect(self.db_user_path)
        cursor = conn.cursor()

        cursor.execute("SELECT password FROM users WHERE username=?",(username,))
        result = cursor.fetchone()

        conn.close()

        if result is None:
            messagebox.showerror("Prijava nije uspjela!", "Netočno korisničko ime ili lozinka!")
        else:
            hashed_saved_password = result[0].encode('utf-8')

            if bcrypt.checkpw(password.encode('utf-8'),hashed_saved_password):
                messagebox.showinfo("Uspješna prijava!", "Uspješno ste se prijavili u aplikaciju!")
                #Logic for showing the main plant page
                self.switch_to_plant_view()
            else:
                messagebox.showerror("Prijava nije uspjela!", "Netočno korisničko ime ili lozinka")
    
    def add_or_update_plants(self,name,picture,soil,temperature,light,substrate,plant_id):
        if not name or not picture or not soil or not temperature or not light or not substrate:
            messagebox.showerror("Dodavanje biljke nije uspjelo!", "Molimo vas da unesete sve podatke!")
            return
        
        try:
            temperature = float(temperature)
            light = float(light)
        except ValueError:
            messagebox.showerror("Dodavanje biljke nije uspjelo!", "Unesite ispravne vrijednosti za temperaturu i svjetlost!")
            return
        
        self.plant_id = plant_id

        conn = sqlite3.connect(self.db_plant_path)
        cursor = conn.cursor()

        if self.plant_id is not None:

            cursor.execute('''
                UPDATE plants SET name=?, picture=?, soil_moisture=?, ideal_temperature=?, ideal_light=?, substrate_recommendation=?
                WHERE id=?
            ''', (name, self.save_image_locally(picture,name), soil, float(temperature), float(light), substrate, self.plant_id))
            messagebox.showinfo("Uspjeh!", "Uspješno ste ažurirali biljku")
        else:
            cursor.execute('''
                INSERT INTO plants (name, picture, soil_moisture, ideal_temperature, ideal_light, substrate_recommendation)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (name, self.save_image_locally(picture,name), soil, float(temperature), float(light), substrate))
            messagebox.showinfo("Uspjeh!", "Uspješno ste dodali biljku")
        
        conn.commit()
        cursor.close()
        
        self.switch_to_plant_view()
    
    def save_image_locally(self, picture, plant_name):
        # Create the images folder if it doesn't exist
        if not os.path.exists(IMAGES_FOLDER):
            os.makedirs(IMAGES_FOLDER)

        # Generate a unique filename based on the plant name
        filename = f"{plant_name}.jpg"  # Change the extension as per your image format

        # Construct the full file path
        file_path = os.path.join(IMAGES_FOLDER, filename)

        try:
            # Copy the image file to the local folder
            shutil.copy2(picture, file_path)
        except shutil.SameFileError:
            print("Files are the same")

        return file_path

        
    

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