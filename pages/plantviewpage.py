from tkinter import Frame,Label,Button, messagebox
from PIL import Image, ImageTk
import sqlite3

class PlantViewPage(Frame):
    def __init__(self,root,controller_class,current_plant_id = 0):
        super().__init__(root)
        self.root_window = root
        self.controller_class = controller_class
        self.current_plant_id = current_plant_id
        self.current_plant = None

        self.plant_name_label = Label(self , font= ('Arial',15) , bg = "#c8d6e5")
        self.plant_name_label.grid(row = 0, column= 1,sticky= "N",  pady = 10)

        self.plant_care_label = Label(self,text= "Njega:" , font= ('Arial',10) , bg = "#c8d6e5")
        self.plant_care_label.grid(row = 1, column= 1,sticky= "N")

        self.plant_soil_ph_label = Label(self , font= ('Arial',10) , bg = "#c8d6e5")
        self.plant_soil_ph_label.grid(row = 2 , column= 1, sticky= "N")

        self.plant_moisture_label = Label(self , font= ('Arial',10) , bg = "#c8d6e5")
        self.plant_moisture_label.grid(row=3,column = 1,  sticky= "N")

        self.plant_temperature_label = Label(self , font= ('Arial',10) , bg = "#c8d6e5")
        self.plant_temperature_label.grid(row = 4 , column= 1, sticky= "N")

        self.plant_light_label = Label(self , font= ('Arial',10) , bg = "#c8d6e5")
        self.plant_light_label.grid(row = 5 , column= 1, sticky= "N")

        self.plant_substrate_label = Label(self , font= ('Arial',10) , bg = "#c8d6e5")
        self.plant_substrate_label.grid(row = 6, column= 1 , sticky= "N")

        self.plant_image = Label(self , font= ('Arial',10) , bg = "#c8d6e5")
        self.plant_image.grid(row= 7,column= 1 , sticky= "N",pady= 5)

        self.back_button = Button(self,text= "Natrag", bg = "#ffffff", command= self.controller_class.switch_to_plants_page, font = ('Arial',10) , relief= "solid" ,  borderwidth= 1)
        self.back_button.grid(row = 10, column= 1, sticky= "WE" , pady= 5)

        self.update_button = Button(self,text= "Ažuriraj", bg = "#ffffff", command= self.update_plant, font = ('Arial',10), relief= "solid" , borderwidth= 1)
        self.update_button.grid(row = 9, column= 1, sticky= "WE")

        self.delete_button = Button(self,text= "Izbriši biljku", bg = "#ffffff", command= self.delete_plant, font = ('Arial',10), relief= "solid" , borderwidth= 1)
        self.delete_button.grid(row = 11, column= 1, sticky= "WE")
        
        


    

    def show_page(self,plant_id = 0, pot_id = 0):

        self.place(relx=0.5, rely=0.2,anchor="n")

        self.current_plant_id = plant_id

        self.get_plant()

    def hide_page(self):
        self.place_forget()
    
    def get_plant(self):
        try:
            with sqlite3.connect(self.controller_class.plant_database_location) as conn_plants:
                cursor_plants = conn_plants.cursor()
                cursor_plants.execute("SELECT name, picture, min_soil_pH, max_soil_pH, required_ground_moisture, ideal_min_temperature, ideal_max_temperature, ideal_light_hours, substrate_recommendation FROM plants WHERE id=?", (self.current_plant_id,))
                self.current_plant = cursor_plants.fetchone()
                self.plant_name_label.config(text=self.current_plant[0], font=65)
                self.plant_soil_ph_label.config(text=f"pH tla: {self.current_plant[2]} - {self.current_plant[3]} pH")
                self.plant_moisture_label.config(text=f"Potrebna vlažnost: {self.current_plant[4]} mm")
                self.plant_temperature_label.config(text=f"temperatura: {self.current_plant[5]} - {self.current_plant[6]}°C")
                self.plant_light_label.config(text=f"Potrebna svjetlost: {self.current_plant[7]} sati dnevno")
                self.plant_substrate_label.config(text=f"Preporuka substrata: {self.current_plant[8]}")

                image_path = self.current_plant[1]
                image = Image.open(image_path)
                image = image.resize((250, 250))
                photo = ImageTk.PhotoImage(image)

                self.plant_image.config(image=photo)
                self.plant_image.image = photo
        except sqlite3.Error as e:
            messagebox.showerror("Greška!", f"Nešto je otišlo po zlu: {e}")
    
    def update_plant(self):
        self.controller_class.plant_id = self.current_plant_id
        self.controller_class.switch_to_plants_form()
    

    def delete_plant(self):
        confirmed = messagebox.askyesno("PAŽNJA!", "Da li stvarno želite izbrisati ovu biljku?")


        if confirmed:
            self.controller_class.plant_id = self.current_plant_id
            self.controller_class.delete_the_plant(self.current_plant[0])
        
       
        

        
