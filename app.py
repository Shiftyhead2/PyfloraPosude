from tkinter import *
from tkinter import messagebox
from pages.login import LoginPage
from pages.register import RegisterPage
from pages.plantviewheader import PlantViewHeader
from pages.plantsview import PlantsView
from pages.plantsform import PlantsForm
from pages.individualplantview import IndividualPlantView
from pages.potviewheader import PotViewHeader
from pages.potsview import PotsView
from pages.potsform import PotsForm
from pages.syncbutton import SyncButton
from pages.individualpotview import IndividualPotView
import sqlite3
import os
import bcrypt
import shutil
import random

IMAGES_FOLDER = "images"
IMAGES_EXTENSION = "jpg"
DATABASES_FOLDER = "database"

#The main app that controls how the application renders diferrent pages. Also creates the required databases and handles CRUD for many of these databases
class AppController:
    def __init__(self,root):
        # The root is the main root window create in the main function that is passed here
        self.root = root

        
        # Creates the correct file paths for various databases and then creates them. The file paths will look like this: database\{database}.db
        self.db_user_path = os.path.join(DATABASES_FOLDER,'users.db') 
        self.db_plant_path = os.path.join(DATABASES_FOLDER,'plants.db')
        self.db_pot_path = os.path.join(DATABASES_FOLDER,"pots.db")
        self.db_sensor_path = os.path.join(DATABASES_FOLDER,"sensors.db")
        self.create_user_table()
        self.create_plant_table()
        self.create_pots_table()
        self.create_sensors_table()

        # This is to keep track of the current plant ID for use in individual plant view and in the plant form
        self.plant_id = None

        # Same thing for pots as plants.
        self.pot_id = None

        # This is a dictionary of all the pages for the application. All the pages are actually initialized when this app starts. 
        # The key is the name of the page and the value is the class itself
        self.pages = {
            # When creating a page class like this there are a couple of parametres. The first one is the master which is the root window of the GUI application and the second one
            # is the controller which is the AppController class, additionally some views may take optional parametres which are required for certain operation ,but not really required
            # for them to work normally as they are assigned a default value by the page class itself
            "login": LoginPage(self.root,self),
            "register":RegisterPage(self.root,self),
            "plant_view_header": PlantViewHeader(self.root,self),
            "plants_view": PlantsView(self.root,self),
            "plants_form": PlantsForm(self.root,self),
            "plant_view": IndividualPlantView(self.root,self),
            "pot_view_header":PotViewHeader(self.root,self),
            "pots_view": PotsView(self.root,self),
            "pot_form": PotsForm(self.root,self),
            "pot_view":IndividualPotView(self.root,self),
            "sync_button":SyncButton(self.root,self),
        }

        # Keeps track of the current shown pages in a list
        self.current_pages = []
        
        # Configures the columns and the rows of the roots grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # Switches to the login page
        self.switch_to_page("login")
    
    # The function for switching pages. Takes in the names of the pages as a parameter
    def switch_to_page(self,*page_names):
        # Finds all the paramater pages in the self.pages dictionary and then assigns them to the pages list 
        pages = [self.pages.get(page_name) for page_name in page_names]
        # Checks if there are any pages in the pages list.
        if all(pages):
            # If there are any pages in the pages list loops throught the current pages list and hides all the current shown pages
            for page in self.current_pages:
                page.hide()
            # Assigns the current pages list to the pages list
            self.current_pages = pages

            # For debugging purposes. Prints the current list of pages
            #print(self.current_pages)

            # Loops throught all the new assigned pages in the current pages list and shows them passing the plant_id and the pot_id variable which are actually optional as 
            # they are assigned by default as None in some pages as not all pages require these variables for them to work. Only plants need the plant_id variable to work correctly 
            # and same goes for the pots.
            for page in self.current_pages:
                page.show(self.plant_id,self.pot_id)
        # Showns an error if a page doesn't exist in the pages dictionary or the pages list is empty
        else:
            messagebox.showerror("Critical Error!",f"One or more pages could not be found: {page_names}")
    
    # Function to switch to the register page
    def switch_to_register(self):
        self.switch_to_page("register")

    # Function to switch to the login page
    def switch_to_login(self):
        self.switch_to_page("login")

    # Function to switch to the plant view. Also assigns the plant_id variable to None
    def switch_to_plant_view(self):
        self.switch_to_page("plant_view_header","plants_view")
        self.plant_id = None
    
    # Function to switch to the plant form.
    def switch_to_plant_form(self):
        self.switch_to_page("plants_form")
    
    # Function to switch to the pot form.
    def switch_to_pot_form(self):
        self.switch_to_page("pot_form")

    # Function to switch to the individual plant view (aka a single plant selected from the plants view)
    def switch_to_individual_plant_view(self):
        self.switch_to_page("plant_view_header","plant_view")
    
    # Function to switch to the view where all the pots are displayed. Also assigns the pot_id variable to None
    def switch_to_pot_view(self):
        self.switch_to_page("pot_view_header","sync_button", "pots_view")
        self.pot_id = None
    
    # Function to switch to an individually selected pot (aka pot selected from the pot view)
    def switch_to_individual_pot_view(self):
        self.switch_to_page("pot_view_header","pot_view")
        
    
    # Function to create the plant table
    def create_plant_table(self):
        # Connects to the plant database
        conn = sqlite3.connect(self.db_plant_path)
        # Creates the cursor used to execute SQL commands in the sqlite3 database
        cursor = conn.cursor()

        # Executes the SQL command for creating a plants table if it doesn't exist
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
                ideal_light INT,
                substrate_recommendation TEXT
            )  
        ''')


        # Commits the changes made to the plants database
        conn.commit()
        # Closes the plants database. It's important to always close a sqlite 3 database when using any programming language to ensure
        # proper handling of resources and data intergrity
        conn.close()

    # Function to create the user table. It's indentical to the function that creates the plants table
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

    # Function to create the pots table. It's indentical to the function that creates the plants table
    def create_pots_table(self):
        conn = sqlite3.connect(self.db_pot_path)
        cursor = conn.cursor()

        cursor.execute('''
          CREATE TABLE IF NOT EXISTS pots (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            plant_id INT,
            plant_name TEXT,
            plant_picture_location TEXT,       
            status TEXT
          )''')
        
        conn.commit()
        conn.close()
    
    # Function to create the sensors table. It's indentical to the function that creates the plants table
    def create_sensors_table(self):
        conn = sqlite3.connect(self.db_sensor_path)
        cursor = conn.cursor()

        cursor.execute('''
          CREATE TABLE IF NOT EXISTS sensors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            ground_moisture INT,
            pH_ground FLOAT,
            light_lux INT,
            temperature FLOAT
          )''')
        
        conn.commit()
        conn.close()
        
    # Function for registering the user. Takes in a name, surname , username and the password
    def register_user(self,name,surname,username,password):
        # Checks if all the parameters are not empty or None. If they are show an error and return (exit) out of the function.
        if not name or not surname or not username or not password:
            messagebox.showerror("Registracija ne uspješna!","Molimo vas unesite sve podatke!")
            return

        # Encrypts and then hashes the encrypted password using the bcrypt python module. It makes sense to encrypt the users password before storing it in a database for added security
        hashed_password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

        # Connects to the users database and creates a cursor for executing SQL commands in the database
        conn = sqlite3.connect(self.db_user_path)
        cursor = conn.cursor()

        
        #Tries to execute the SQL command for inserting the values to the users database. The password is decoded using bcrypt python module.
        try:
            cursor.execute(''' 
                INSERT INTO users(name,surname,username,password)
                VALUES(?,?,?,?)
            ''',(name,surname,username,hashed_password.decode('utf-8')))
        except sqlite3.Error as e:
            messagebox.showerror("Registracija ne uspješna!",f"Nešto je otišlo po zlu: {e}")
            return
        else:
             # Commits the changes to the users database and then closes the connection to the SQL database
            conn.commit()
            # Shows a message when the users has successfully registered to the app and then switches to the login screen
            messagebox.showinfo("Registracija uspješna!","Uspješno ste se registrilali u aplikaciju!")
            self.switch_to_login()
        finally:
            print("Closing connection")
            conn.close()
     
    
    # Function for logging in the user. Takes in a username and a password
    def login_user(self,username,password):
        # Checks if the username and password are not empty or None. If they are show an error and return(exit) out of the function
        if not username or not password:
            messagebox.showerror("Prijava nije uspjela!", "Molimo vas unesite sve podatke!")
            return
        
        

        # Connects to the users database and creates a cursor for executing SQL commands in the database
        conn = sqlite3.connect(self.db_user_path)
        cursor = conn.cursor()

        # Tries to execute an SQL command for selecting the password from the users database with the filter of the username 
        # and then fetches the first result and then caches to the result variable
        try:
            cursor.execute("SELECT password FROM users WHERE username=?",(username,))
        except sqlite3.Error as e:
            messagebox.showerror("Prijava nije uspjela!", f"Nešto je otišlo po zlu: {e}")
            return
        else:
            result = cursor.fetchone()
        finally:
             # Closes the SQL connection. Commiting is not required since we are not updating the users database
            print("Closing connection")
            conn.close()

       

        # If the result is None then show an error
        if result is None:
            messagebox.showerror("Prijava nije uspjela!", "Netočno korisničko ime ili lozinka!")
        else:
            # Encode the password using the bcrypt module and then save it a variable
            hashed_saved_password = result[0].encode('utf-8')

            # Using the bcrypt module we are checking if the function parameter password is the same as the cached passworded
            if bcrypt.checkpw(password.encode('utf-8'),hashed_saved_password):
                messagebox.showinfo("Uspješna prijava!", "Uspješno ste se prijavili u aplikaciju!")
                #Logic for showing the main plant page
                self.switch_to_plant_view()
            else:
                messagebox.showerror("Prijava nije uspjela!", "Netočno korisničko ime ili lozinka")
    
    # Function for creating or updating the plants. Takes in a name, picture location , minimum soil pH, maximum soil pH
    # minimum temperature , maximum temperature , light , substrate and the plant ID for updating the correct plant
    def add_or_update_plants(self,name,picture,min_soil,max_soil, required_moisture,min_temperature,max_temperature,light,substrate,plant_id = None):

        # If any of the parameters are empty or None then show an error and return(exit) out of the function
        if not name or not picture or not min_soil or not max_soil or not min_temperature or not light or not substrate or not max_temperature or not required_moisture:
            messagebox.showerror("Dodavanje ili ažuriranje biljke nije uspjelo!", "Molimo vas da unesete sve podatke!")
            return
        
        # Try to convert the parametres that should be floating numbers in the database to a floating number if possible. If they cannot be converted 
        # then show an error and return(exit) out of the function
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
    
        # Assigns the AppController's plant_id to the passed plant_id    
        self.plant_id = plant_id

        # Connects to the plants database and creates a cursor for executing SQL commands in the database
        conn = sqlite3.connect(self.db_plant_path)
        cursor = conn.cursor()

        # Checks if the AppControllers's plant_id is not None or 0
        if self.plant_id is not None:
            # If it isn't None then the cursor the function tries to execute the SQL command for updating the correct plant in the plants database
            try:
                cursor.execute('''
                    UPDATE plants SET name=?, picture=?, min_soil_pH=?, max_soil_pH = ?, required_ground_moisture=?, ideal_min_temperature=?,ideal_max_temperature=?, ideal_light=?, substrate_recommendation=?
                    WHERE id=?
                ''', (name, self.save_image_locally(picture,name), float(min_soil),float(max_soil),int(required_moisture), float(min_temperature),float(max_temperature), int(light), substrate, self.plant_id))
            except sqlite3.Error as e:
                messagebox.showerror("Greška!", f"Nešto je otišlo po zlu: {e}")
                conn.close()
                return
            else:
                # Shows the message if the update was successfull
                messagebox.showinfo("Uspjeh!", "Uspješno ste ažurirali biljku") 
        else:
            # If it is None then the cursor the function tries executes the SQL command for creating a new plant in the plants database
            try:
                cursor.execute('''
                    INSERT INTO plants (name, picture, min_soil_pH,max_soil_ph, required_ground_moisture, ideal_min_temperature,ideal_max_temperature, ideal_light, substrate_recommendation)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
                ''', (name, self.save_image_locally(picture,name), float(min_soil),float(max_soil), int(required_moisture), float(min_temperature),float(max_temperature), int(light), substrate))
            except sqlite3.Error as e:
                messagebox.showerror("Greška!", f"Nešto je otišlo po zlu: {e}")
                conn.close()
                return
            else:
                # Shows the message if the creation was successfull
                messagebox.showinfo("Uspjeh!", "Uspješno ste dodali biljku")

        
        # Commits the changes to the plants database and then closes the connection to the SQL database
        conn.commit()
        cursor.close()
        
        # Switches to the plant view
        self.switch_to_plant_view()
    

    # Function for deleting the plant
    def delete_the_plant(self,plant_name):
        # Connects to the plants database and creates a cursor for executing SQL commands in the database
        conn = sqlite3.connect(self.db_plant_path)
        cursor = conn.cursor()

        conn2 = sqlite3.connect(self.db_pot_path)
        cursor2 = conn2.cursor()

        
        try:
            # First it tries to delete the local picture file in this app
            self.delete_picture_locally(plant_name)
            #Then tries to delete the actual plant from the database
            cursor.execute('DELETE FROM plants WHERE id= ?' ,(self.plant_id,))
            cursor2.execute('''UPDATE pots SET plant_id = ?, plant_name=?, plant_picture_location= ?,  status = ? WHERE plant_id = ?''',(0,"","","Status:Prazna posuda", self.plant_id))
            # If successfull commits the changes, shows the message box and then switches to the plant view
            conn.commit()
            conn2.commit()
            messagebox.showinfo("Biljka izbrisana!" , "Uspješno ste izbrisali biljku!")
            self.switch_to_plant_view()
        # If there is an error during the deletion of the local picture file in this app then it shows an error  and switches back to the actual plant   
        except OSError as e:
            messagebox.showerror("Greška!",f"Nešto je pošlo po zlu pri brisanju biljke: {e}")
            self.switch_to_individual_plant_view()
        # If there is any errors when doing something with the SQlite 3 database then it shows an error and switches back to the actual plant
        except sqlite3.Error as e:
            messagebox.showerror("Greška!",f"Nešto je pošlo po zlu pri brisanju biljke: {e}")
            self.switch_to_individual_plant_view()
        # Closes the connection regradless if there is an error or not
        finally:
            conn.close()
            conn2.close()

    # Function for randomly generating sensor values and storing them in the sensor database for later use
    def sync_sensor(self):
        conn = sqlite3.connect(self.db_sensor_path)
        cursor = conn.cursor()


        # Create the variables stored randomly making sure they match exactly the same value types in the database
        ground_moisture = random.randint(0, 100)
        pH_ground = round(random.uniform(0.0, 14.0), 2)
        light_day = random.randint(0, 12)
        temperature = round(random.uniform(-20.0, 50.0), 2)
        
        # Again basic principle as creating all the other values and putting them into a database. Try to execute the said SQL command
        # If there is an error throw the user the said error
        # If there are no errors show the user a success message
        # Then finally close the connection
        try:
            cursor.execute('''
            INSERT INTO sensors (ground_moisture, pH_ground, light_lux, temperature)
            VALUES (?, ?, ?, ?)
        ''', (ground_moisture, pH_ground, light_day, temperature))
            
        except sqlite3.Error as e:
            messagebox.showerror("Greška!", f"Nešto je otišlo po zlu: {e}")
        else:
            messagebox.showinfo("Uspjeh!", "Uspješno ste dodali nove podatke sa sensora!")
        finally:
            conn.commit()
    
    # Function to add a pot to the pot database. It takes in the location, plant_id, plant_name , plant_picture_location , status , pot_id for correctly updating the 
    # pot
    def add_pot(self,location,plant_id,plant_name,plant_picture_location,status, pot_id = None):
        # Much of the code is similar and follow the similar logic as the adding or updating plants code expect there are fewer parameters to pass
        # Basically connect to the correct database, try to execute an SQL command based on whatever or not we are creating or updating the pot
        # if there is an error show the user an error message and then close the connection and exit out of the function
        # If there is no errors then show the user a message based on if we are updating or creating a pot
        # And then finally commit the changes and close the connection to the database then switch to the correct page
        if not location or not plant_id:
            messagebox.showerror("Greška!", "Molimo vas da unesete sve podatke!")
            return


        conn = sqlite3.connect(self.db_pot_path)
        cursor = conn.cursor()


        self.pot_id = pot_id

        try:
            if self.pot_id is not None and self.pot_id != 0:
                cursor.execute('''UPDATE pots SET location = ?, plant_id = ?, plant_name=?, plant_picture_location= ?,  status = ? WHERE id = ?''',
                            (location, plant_id, plant_name, plant_picture_location, status, self.pot_id))
            else:
                cursor.execute('''INSERT INTO pots (location, plant_id, plant_name, plant_picture_location, status) VALUES (?,?,?,?,?)''',
                             (location, plant_id, plant_name, plant_picture_location, status))
        except sqlite3.Error as e:
            messagebox.showerror("Greška!", f"Nešto je otišlo po zlu: {e}")
            conn.close()
            return
        else:
            if self.pot_id is not None and self.pot_id != 0:
                messagebox.showinfo("Uspjeh!", "Uspješno ste ažurirali posudu")
            else:
                messagebox.showinfo("Uspjeh!", "Uspješno ste dodali posudu")

        conn.commit()
        conn.close()

        self.switch_to_pot_view()
    

      # Function for deleting the pot
    def delete_the_pot(self):
        # Connects to the pots database and creates a cursor for executing SQL commands in the database
        conn = sqlite3.connect(self.db_pot_path)
        cursor = conn.cursor()
        
        try:
            #Then tries to delete the actual pot from the database
            cursor.execute('DELETE FROM pots WHERE id= ?' ,(self.pot_id,))
            # If successfull commits the changes, shows the message box and then switches to the pot view
            conn.commit()
            messagebox.showinfo("Posuda izbrisana!" , "Uspješno ste izbrisali posudu!")
            self.switch_to_pot_view()
        # If there is any errors when doing something with the SQlite 3 database then it shows an error and switches back to the actual pot
        except sqlite3.Error as e:
            messagebox.showerror("Greška!",f"Nešto je pošlo po zlu pri brisanju posude: {e}")
            self.switch_to_individual_pot_view()
        # Closes the connection regradless if there is an error or not
        finally:
            conn.close()
        
    
    
    # Function for saving the images locally (AKA in this applications folder)
    def save_image_locally(self, picture, plant_name):
        # Generate a unique filename based on the plant name
        filename = f"{plant_name}.{IMAGES_EXTENSION}"  # Change the extension as per the given image format

        # Construct the full file path
        file_path = os.path.join(IMAGES_FOLDER, filename)

        try:
            # Copy the image file to the local folder if it isn't the same
            shutil.copy2(picture, file_path)
        except shutil.SameFileError:
            print("Files are the same")

        return file_path
    
    # Function for deleting the local image
    def delete_picture_locally(self,plant_name):
         # Generate a unique filename based on the plant name
        filename = f"{plant_name}.{IMAGES_EXTENSION}" # Change the extension as per the given image format

         # Construct the full file path
        file_path = os.path.join(IMAGES_FOLDER, filename)

        try:
            # Try deleting the image
            os.remove(file_path)
        # Return an error if there is an error
        except OSError as e:
            return e


        
    
#Create the main root for the GUI application, creates the main app controller app and starts the GUI application
def main():
    root = Tk()
    root.title("PyFlora")
    root.geometry("1280x720")

    app = AppController(root)

    

    root.mainloop()
    
#This checks if this python file has the name __main__ and if it does creates the folders for the databases and images if they do not exist and then executes the main function
if __name__ == "__main__":
    os.makedirs(DATABASES_FOLDER,exist_ok=True) 
    os.makedirs(IMAGES_FOLDER,exist_ok=True)


    main()