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
        self.create_user_table()
        self.create_plant_table()

        # This is to keep track of the current plant ID for use in individual plant view and in the plant form
        self.plant_id = None

        # This is a dictionary of all the pages for the application. All the pages are actually initialized when this app starts. 
        # The key is the name of the page and the value is the class itself
        self.pages = {
            # When creating a page class like this there are a couple of parametres. The first one is the master which is the root window of the GUI application and the second one
            # is the controller which is the AppController class
            "login": LoginPage(self.root,self),
            "register":RegisterPage(self.root,self),
            "plant_view_header": PlantViewHeader(self.root,self),
            "plants_view": PlantsView(self.root,self),
            "plants_form": PlantsForm(self.root,self),
            "plant_view": IndividualPlantView(self.root,self)
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

            print(self.current_pages)

            # Loops throught all the new assigned pages in the current pages list and shows them passing the plant_id variable
            for page in self.current_pages:
                page.show(self.plant_id)
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

    def switch_to_individual_plant_view(self):
        self.switch_to_page("plant_view_header","plant_view")
        
    
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
                ideal_min_temperature REAL,
                ideal_max_temperature REAL,
                ideal_light REAL,
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
    def add_or_update_plants(self,name,picture,min_soil,max_soil,min_temperature,max_temperature,light,substrate,plant_id):

        # If any of the parameters are empty or None then show an error and return(exit) out of the function
        if not name or not picture or not min_soil or not max_soil or not min_temperature or not light or not substrate or not max_temperature:
            messagebox.showerror("Dodavanje ili ažuriranje biljke nije uspjelo!", "Molimo vas da unesete sve podatke!")
            return
        
        # Try to convert the parametres that should be floating numbers in the database to a floating number if possible. If they cannot be converted 
        # then show an error and return(exit) out of the function
        try:
            min_temperature = float(min_temperature)
            max_temperature = float(max_temperature)
            light = float(light)
            min_soil = float(min_soil)
            max_soil = float(max_soil)
        except ValueError:
            messagebox.showerror("Dodavanje ili ažuriranje biljke nije uspjelo!", "Unesite ispravne vrijednosti za tlo,  temperaturu i svjetlost!")
            return
    
        # Assigns the AppController's plant_id to the passed plant_id    
        self.plant_id = plant_id

        # Connects to the plants database and creates a cursor for executing SQL commands in the database
        conn = sqlite3.connect(self.db_plant_path)
        cursor = conn.cursor()

        # Checks if the AppControllers's plant_id is not None
        if self.plant_id is not None:
            # If it isn't None then the cursor the function tries to execute the SQL command for updating the correct plant in the plants database
            try:
                cursor.execute('''
                    UPDATE plants SET name=?, picture=?, min_soil_pH=?, max_soil_pH = ?, ideal_min_temperature=?,ideal_max_temperature=?, ideal_light=?, substrate_recommendation=?
                    WHERE id=?
                ''', (name, self.save_image_locally(picture,name), float(min_soil),float(max_soil), float(min_temperature),float(max_temperature), float(light), substrate, self.plant_id))
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
                    INSERT INTO plants (name, picture, min_soil_pH,max_soil_ph, ideal_min_temperature,ideal_max_temperature, ideal_light, substrate_recommendation)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (name, self.save_image_locally(picture,name), float(min_soil),float(max_soil), float(min_temperature),float(max_temperature), float(light), substrate))
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
    
    def delete_the_plant(self):
        conn = sqlite3.connect(self.db_plant_path)
        cursor = conn.cursor()

        try:
            cursor.execute('DELETE FROM plants WHERE id= ?' ,(self.plant_id,))
            conn.commit()
            messagebox.showinfo("Biljka izbrisana!" , "Uspješno ste izbrisali biljku!")
            self.switch_to_plant_view()
        except sqlite3.Error as e:
            messagebox.showerror("Greška!",f"Nešto je pošlo po zlu pri brisanju biljke: {e}")
            self.switch_to_individual_plant_view()
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