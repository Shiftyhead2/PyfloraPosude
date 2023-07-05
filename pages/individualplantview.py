from tkinter import Frame,Label,Button, messagebox
from PIL import Image, ImageTk
import sqlite3

class IndividualPlantView(Frame):
    def __init__(self,master,controller,plant_id = None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.plant_id = plant_id
        self.plant = None

        self.plant_name_label = Label(self)
        self.plant_name_label.grid(row = 0, column= 1,sticky= "W" , pady = 10)

        self.plant_care_label = Label(self,text= "Njega:")
        self.plant_care_label.grid(row = 1, column= 1,sticky= "W")

        self.plant_soil_ph_label = Label(self)
        self.plant_soil_ph_label.grid(row = 2 , column= 2, sticky= "W")

        self.plant_moisture_label = Label(self)
        self.plant_moisture_label.grid(row=3,column = 2,  sticky= "W")

        self.plant_temperature_label = Label(self)
        self.plant_temperature_label.grid(row = 4 , column= 2, sticky= "W")

        self.plant_light_label = Label(self)
        self.plant_light_label.grid(row = 5 , column= 2, sticky= "W")

        self.plant_substrate_label = Label(self)
        self.plant_substrate_label.grid(row = 6, column= 2 , sticky= "W")

        self.plant_image = Label(self)
        self.plant_image.grid(row= 7,column= 2 , sticky= "W",pady= 5)

        self.back_button = Button(self,text= "Natrag", command= self.controller.switch_to_plant_view, font = (25))
        self.back_button.grid(row = 10, column= 2, sticky= "WE" , pady= 5)

        self.update_button = Button(self,text= "Ažuriraj", command= self.update_plant, font = (25))
        self.update_button.grid(row = 9, column= 2, sticky= "WE")

        self.delete_button = Button(self,text= "Izbriši biljku", command= self.delete_plant, font = (25))
        self.delete_button.grid(row = 11, column= 2, sticky= "WE")
        
        


    

    def show(self,plant_id = None, pot_id = None):
        self.master.update_idletasks()  # Ensure the window size is updated

        self.place(relx=0.4, rely=0.5,anchor="w")

        self.plant_id = plant_id

        self.get_specific_plant()

    def hide(self):
        self.place_forget()
    
    def get_specific_plant(self):
        conn = sqlite3.connect(self.controller.db_plant_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT name,picture,min_soil_pH,max_soil_pH,required_ground_moisture,ideal_min_temperature,ideal_max_temperature,ideal_light,substrate_recommendation FROM plants WHERE id=?",(self.plant_id,))
        except sqlite3.Error as e:
            messagebox.showerror(f"Greška!", f"Nešto je otišlo po zlu: {e}")
        else:
            self.plant = cursor.fetchone()
            self.plant_name_label.config(text= self.plant[0], font = 65)
            self.plant_soil_ph_label.config(text = f"pH tla: {self.plant[2]} - {self.plant[3]} pH")
            self.plant_moisture_label.config(text = f"Potrebna vlažnost: {self.plant[4]} mm")
            self.plant_temperature_label.config(text = f"temperatura: {self.plant[5]} - {self.plant[6]}°C")
            self.plant_light_label.config(text = f"Potrebna svjetlost: {self.plant[7]} luxa")
            self.plant_substrate_label.config(text = f"Preporuka substrata: {self.plant[8]}")

            image_path = self.plant[1]
            image = Image.open(image_path)


            image = image.resize((250, 250))

            photo = ImageTk.PhotoImage(image)


            self.plant_image.config(image= photo)
            self.plant_image.image = photo 
        finally:
            conn.close()
    
    def update_plant(self):
        self.controller.plant_id = self.plant_id
        self.controller.switch_to_plant_form()
    

    def delete_plant(self):
        confirmed = messagebox.askyesno("PAŽNJA!", "Da li stvarno želite izbrisati ovu biljku?")


        if confirmed:
            self.controller.plant_id = self.plant_id
            self.controller.delete_the_plant(self.plant[0])
        
       
        

        
