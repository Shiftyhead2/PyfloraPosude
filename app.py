from tkinter import *
from tkinter import messagebox
from pages.loginpage import LoginPage
from pages.registerpage import RegisterPage
from pages.applicationheaderpage import ApplicationHeader
from pages.plantviewheader import PlantViewHeader
from pages.plantsviewpage import PlantsViewPage
from pages.plantsform import PlantsForm
from pages.plantviewpage import PlantViewPage
from pages.potviewheader import PotViewHeader
from pages.potsviewpage import PotsViewPage
from pages.potsform import PotsForm
from pages.syncbutton import SyncButton
from pages.potviewpage import PotViewPage
import sqlite3
import os
import bcrypt
import shutil
import random
import re


IMAGES_FOLDER = "images"
IMAGES_EXTENSION = "jpg"
DATABASES_FOLDER = "database"



class App:
    def __init__(self,root):
        self.root = root

       
        
        
        self.user_database_location = os.path.join(DATABASES_FOLDER,'users_data.db') 
        self.plant_database_location = os.path.join(DATABASES_FOLDER,'plants_data.db')
        self.pot_database_location = os.path.join(DATABASES_FOLDER,"pots_data.db")
        self.sensor_database_location = os.path.join(DATABASES_FOLDER,"sensor_data.db")
        self.create_users_database()
        self.create_plants_database()
        self.create_pots_database()
        self.create_sensors_database()

        self.plant_id = 0


        self.pot_id = 0


        self.pages_dict = {
            "application_header": ApplicationHeader(self.root,self),
            "login_page": LoginPage(self.root,self),
            "register_page":RegisterPage(self.root,self),
            "plant_view_header": PlantViewHeader(self.root,self),
            "plants_view_page": PlantsViewPage(self.root,self),
            "plants_form_page": PlantsForm(self.root,self),
            "plant_view_page": PlantViewPage(self.root,self),
            "pot_view_header":PotViewHeader(self.root,self),
            "pots_view_page": PotsViewPage(self.root,self),
            "pot_form_page": PotsForm(self.root,self),
            "pot_view_page":PotViewPage(self.root,self),
            "sync_button":SyncButton(self.root,self),
        }


        self.current_pages = []
        
       
        
       

        self.switch_to_login_page()

        self.root.configure(bg="#c8d6e5")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)


    def configure(self, color):
        for page in self.pages_dict.values():
            page.configure(bg=color)
    
    
    
    def switch_to_register_page(self):
        self.show_current_pages("application_header","register_page")

    def switch_to_login_page(self):
        self.show_current_pages("application_header","login_page")


    def switch_to_plants_page(self):
        self.show_current_pages("plant_view_header","plants_view_page", "sync_button")
        self.plant_id = 0
    

    def switch_to_plants_form(self):
        self.show_current_pages("plant_view_header","plants_form_page")
    

    def switch_to_pots_form(self):
        self.show_current_pages("pot_view_header","pot_form_page")


    def switch_to_individual_plant_page(self):
        self.show_current_pages("plant_view_header","plant_view_page")


    def switch_to_pots_page(self):
        self.show_current_pages("pot_view_header","sync_button", "pots_view_page")
        self.pot_id = 0
    

    def switch_to_individual_pot_page(self):
        self.show_current_pages("pot_view_header","pot_view_page")

    
    def show_current_pages(self,*page_strings):
        pages = [self.pages_dict.get(page_string) for page_string in page_strings]
        if all(pages):
            for page in self.current_pages:
                page.hide_page()
            self.current_pages = pages

            for page in self.current_pages:
                page.show_page(self.plant_id,self.pot_id)
        else:
            messagebox.showerror("Greška!",f"Jedna ili više stranica nije pronađena: {page_strings}")
    

    def create_plants_database(self):
        with sqlite3.connect(self.plant_database_location) as conn_plants:
            cursor = conn_plants.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS plants(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    picture TEXT,
                    min_soil_pH REAL,
                    max_soil_pH REAL,
                    required_ground_moisture INT,
                    ideal_min_temperature REAL,
                    ideal_max_temperature REAL,
                    ideal_light_hours INT,
                    substrate_recommendation TEXT
                )  
            ''')
            conn_plants.commit()

    def create_users_database(self):
        with sqlite3.connect(self.user_database_location) as conn_users:
            cursor = conn_users.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    surname TEXT,
                    username TEXT,
                    password TEXT
                )''')
            conn_users.commit()

    def create_pots_database(self):
        with sqlite3.connect(self.pot_database_location) as conn_pots:
            cursor = conn_pots.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS pots (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    location TEXT,
                    plant_id INT,
                    plant_name TEXT,
                    plant_picture_location TEXT,       
                    status TEXT
                    )''')
            conn_pots.commit()
    

    def create_sensors_database(self):
        with sqlite3.connect(self.sensor_database_location) as conn_sensors:
            cursor = conn_sensors.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sensors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ground_moisture INT,
                    pH_ground FLOAT,
                    light_hours INT,
                    temperature FLOAT
                )''')
            conn_sensors.commit()

    def is_valid_username(self,username):
        # Define the regex pattern for the username
        username_pattern = r'^[a-zA-Z0-9]{4,20}$'
        return re.match(username_pattern, username) is not None

    def is_valid_password(self,password):
        # Define the regex pattern for the password
        password_pattern = r'^\S{4,}$'
        return re.match(password_pattern, password) is not None
        

    def register_user(self,name,surname,username,password):

        if not name or not surname:
            messagebox.showerror("Registracija neuspješna!", "Upišite ime i prezime!")
            return

        if not self.is_valid_username(username):
            messagebox.showerror("Registracija neuspješna!", "Korisničko ime nije ispravnog formata!")
            return

        if not self.is_valid_password(password):
            messagebox.showerror("Registracija neuspješna!", "Lozinka nije ispravnog formata!")
            return
    
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        
        try:
            with sqlite3.connect(self.user_database_location) as conn:
                cursor = conn.cursor()
                cursor.execute(''' 
                    INSERT INTO users(name,surname,username,password)
                    VALUES(?,?,?,?)
                    ''',(name,surname,username,hashed_password.decode('utf-8')))
            conn.commit()
            self.switch_to_login_page()
        except sqlite3.Error as e:
            messagebox.showerror("Registracija ne uspješna!",f"Nešto je otišlo po zlu: {e}")
            return
            
    def login_user(self,username,password):
        if not username or not password:
            messagebox.showerror("Prijava nije uspjela!", "Molimo vas unesite sve podatke!")
            return
        
        if username.lower() == "admin" and password.lower() == "admin":
            self.switch_to_plants_page()
            return

        try:
            with sqlite3.connect(self.user_database_location) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT password FROM users WHERE username=?",(username,))
                result = cursor.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror("Prijava nije uspjela!", f"Nešto je otišlo po zlu: {e}")
            return
       
        if result is None:
            messagebox.showerror("Prijava nije uspjela!", "Netočno korisničko ime ili lozinka!")
        else:
            hashed_saved_password = result[0].encode('utf-8')
            if bcrypt.checkpw(password.encode('utf-8'),hashed_saved_password):
                self.switch_to_plants_page()
            else:
                messagebox.showerror("Prijava nije uspjela!", "Netočno korisničko ime ili lozinka")
    
    def add_or_update_plants(self,name,picture,min_soil,max_soil, required_moisture,min_temperature,max_temperature,light,substrate,plant_id = 0):

        if not name or not picture or not min_soil or not max_soil or not min_temperature or not light or not substrate or not max_temperature or not required_moisture:
            messagebox.showerror("Dodavanje ili ažuriranje biljke nije uspjelo!", "Molimo vas da unesete sve podatke!")
            return
        
        try:
            min_temperature = float(min_temperature)
            max_temperature = float(max_temperature)
            light = int(light)
            min_soil = float(min_soil)
            max_soil = float(max_soil)
            required_moisture = int(required_moisture)
        except ValueError:
            messagebox.showerror("Dodavanje ili ažuriranje biljke nije uspjelo!", "Unesite ispravne vrijednosti za tlo, vlažnost, temperaturu i svjetlost!")
            return
   
        self.plant_id = plant_id


        with sqlite3.connect(self.plant_database_location) as conn:
            cursor = conn.cursor()
            if self.plant_id != 0:
                try:
                    cursor.execute('''
                        UPDATE plants SET name=?, picture=?, min_soil_pH=?, max_soil_pH = ?, required_ground_moisture=?, ideal_min_temperature=?,ideal_max_temperature=?, ideal_light_hours=?, substrate_recommendation=?
                        WHERE id=?
                    ''', (name, self.save_image(picture,name), float(min_soil),float(max_soil),int(required_moisture), float(min_temperature),float(max_temperature), int(light), substrate, self.plant_id))
                except (sqlite3.Error, FileNotFoundError) as e:
                    messagebox.showerror("Greška!", f"Nešto je otišlo po zlu: {e}")
                    return
                else:
                    messagebox.showinfo("Uspjeh!", "Uspješno ste ažurirali biljku") 
            else:
                try:
                    cursor.execute('''
                        INSERT INTO plants (name, picture, min_soil_pH,max_soil_ph, required_ground_moisture, ideal_min_temperature,ideal_max_temperature, ideal_light_hours, substrate_recommendation)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
                    ''', (name, self.save_image(picture,name), float(min_soil),float(max_soil), int(required_moisture), float(min_temperature),float(max_temperature), int(light), substrate))
                except (sqlite3.Error, FileNotFoundError) as e:
                    messagebox.showerror("Greška!", f"Nešto je otišlo po zlu: {e}")
                    return
                else:
                    messagebox.showinfo("Uspjeh!", "Uspješno ste dodali biljku")
            conn.commit()
             
        self.switch_to_plants_page()
    

    def delete_the_plant(self,plant_name): 
        try:
            with sqlite3.connect(self.plant_database_location) as conn_plants, sqlite3.connect(self.pot_database_location) as conn_pots:
                cursor_pots = conn_pots.cursor()
                cursor_plants = conn_plants.cursor()
                cursor_plants.execute('DELETE FROM plants WHERE id= ?' ,(self.plant_id,))
                cursor_pots.execute('''UPDATE pots SET plant_id = ?, plant_name=?, plant_picture_location= ?,  status = ? WHERE plant_id = ?''',(0,"","","Status: \n Prazna posuda", self.plant_id))
                conn_pots.commit()
                conn_plants.commit()

                cursor_plants.execute('SELECT id FROM plants')
                remaining_plants = cursor_plants.fetchall()

                for index,plant in enumerate(remaining_plants,start=1):
                    cursor_plants.execute('UPDATE plants SET id=? WHERE id=?' , (index,plant[0]))

                self.delete_image(plant_name)

            messagebox.showinfo("Biljka izbrisana!" , "Uspješno ste izbrisali biljku!")
            self.switch_to_plants_page()  
        except (OSError, sqlite3.Error) as e:
            messagebox.showerror("Greška!",f"Nešto je pošlo po zlu pri brisanju biljke: {e}")
            self.switch_to_individual_plant_page()
            return

    def sync_sensor(self):
        moisture = random.randint(0, 100)
        pH = round(random.uniform(1.0, 14.0), 2) 
        light_hours = random.randint(1, 12)
        current_temp = round(random.uniform(-20.0, 50.0), 2)
        
        try:
            with sqlite3.connect(self.sensor_database_location) as conn_sensor:
                cursor_sensor = conn_sensor.cursor()
                cursor_sensor.execute('''
                INSERT INTO sensors (ground_moisture, pH_ground, light_hours, temperature)
                VALUES (?, ?, ?, ?)
            ''', (moisture, pH, light_hours, current_temp))   
        except sqlite3.Error as e:
            messagebox.showerror("Greška!", f"Nešto je otišlo po zlu: {e}")
        else:
            messagebox.showinfo("Uspjeh!", "Uspješno ste dodali nove podatke sa sensora!")

    def add_or_update_pot(self,location,plant_id,plant_name,plant_picture_location,status, pot_id = 0):
        if not location or not plant_id:
            messagebox.showerror("Greška!", "Molimo vas da unesete sve podatke!")
            return


        self.pot_id = pot_id

        try:
            with sqlite3.connect(self.pot_database_location) as conn:
                cursor = conn.cursor()
                if self.pot_id != 0:
                    cursor.execute('''UPDATE pots SET location = ?, plant_id = ?, plant_name=?, plant_picture_location= ?,  status = ? WHERE id = ?''',
                                (location, plant_id, plant_name, plant_picture_location, status, self.pot_id))
                else:
                    cursor.execute('''INSERT INTO pots (location, plant_id, plant_name, plant_picture_location, status) VALUES (?,?,?,?,?)''',
                                (location, plant_id, plant_name, plant_picture_location, status))
                if self.pot_id != 0:
                    messagebox.showinfo("Uspjeh!", "Uspješno ste ažurirali posudu")
                else:
                    messagebox.showinfo("Uspjeh!", "Uspješno ste dodali posudu")
                conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Greška!", f"Nešto je otišlo po zlu: {e}")
            return
        else:
            self.switch_to_pots_page()


    def delete_the_pot(self):
        try:
            with sqlite3.connect(self.pot_database_location) as conn_pots:
                cursor_pots = conn_pots.cursor()
                cursor_pots.execute('DELETE FROM pots WHERE id= ?' ,(self.pot_id,))
                conn_pots.commit()

                cursor_pots.execute('SELECT id FROM pots')
                remaining_pots = cursor_pots.fetchall()

                for index, pot in enumerate(remaining_pots, start=1):
                    cursor_pots.execute('UPDATE pots SET id=? WHERE id=?', (index, pot[0]))
                conn_pots.commit()

            messagebox.showinfo("Posuda izbrisana!" , "Uspješno ste izbrisali posudu!")
            self.switch_to_pots_page()
        except sqlite3.Error as e:
            messagebox.showerror("Greška!",f"Nešto je pošlo po zlu pri brisanju posude: {e}")
            self.switch_to_individual_pot_page()
            return
        
    
    
    def save_image(self, picture, plant_name):
        filename = f"{plant_name}.{IMAGES_EXTENSION}"  
        file_path = os.path.join(IMAGES_FOLDER, filename)

        try:
            shutil.copy2(picture, file_path)
        except shutil.SameFileError:
            pass
        except FileNotFoundError:
            return FileNotFoundError

        return file_path
    
    def delete_image(self,plant_name):
        filename = f"{plant_name}.{IMAGES_EXTENSION}" 
        file_path = os.path.join(IMAGES_FOLDER, filename)

        try:
            os.remove(file_path)
        except OSError as e:
            return e

    
def main():
    root = Tk()
    root.title("PyFlora")
    root.geometry("1280x720")

    
    
    app = App(root)
    app.configure("#c8d6e5")
    

    root.mainloop()


os.makedirs(DATABASES_FOLDER,exist_ok=True) 
os.makedirs(IMAGES_FOLDER,exist_ok=True)


main()
