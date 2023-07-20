from tkinter import Frame,Button
from PIL import Image, ImageTk
import sqlite3

class PlantsViewPage(Frame):
    def __init__(self,root,controller_class):
        super().__init__(root)
        self.root_window = root
        self.controller_class = controller_class

      

        self.current_plant_buttons = []

        
        self.add_plant_button = Button(self, text="Dodaj novu biljku", font= ('Arial'),  bg = "#ffffff", command = self.controller_class.switch_to_plants_form, relief= "solid",  borderwidth= 1)

        self.load_and_create_plant_buttons()
        

       
    def load_and_create_plant_buttons(self):
         try:
            with sqlite3.connect(self.controller_class.plant_database_location) as conn_plants:
               cursor_plants = conn_plants.cursor()
               cursor_plants.execute("SELECT id, name, picture FROM plants")
               plants = cursor_plants.fetchall()

               for button in self.current_plant_buttons:
                  button.destroy()
               self.current_plant_buttons = []

               max_buttons_per_row = 4
               num_buttons = len(plants)
               num_rows = (num_buttons + max_buttons_per_row - 1) // max_buttons_per_row

               for index, plant in enumerate(plants):
                  row = index // max_buttons_per_row + 1
                  column = index % max_buttons_per_row + 1

                  image_path = plant[2]
                  image = Image.open(image_path)
                  image = image.resize((100, 100))
                  photo = ImageTk.PhotoImage(image)

                  button = Button(self, text=plant[1], image=photo, bg="#ffffff", command=lambda p=plant: self.show_plant_details(p[0]), relief="solid", border=0)
                  button.image = photo
                  button.config(compound="left", padx=10, font=('Arial', 15))
                  button.grid(row=row, column=column, padx=5, sticky="WE", pady=5)

                  self.current_plant_buttons.append(button)

            self.add_plant_button.grid(row=num_rows + 1, columnspan=max_buttons_per_row, column=1, sticky="WE", pady=10)
         except sqlite3.Error as e:
            print(f"Something went wrong: {e}")
       
    
    def show_plant_details(self, plant_id):
        self.controller_class.plant_id = plant_id
        self.controller_class.switch_to_individual_plant_page()

    
    def show_page(self,plant_id = 0, pot_id = 0):

      self.place(relx=0.5, rely=0.5, anchor="center")


      self.load_and_create_plant_buttons()
    
    def hide_page(self):
       self.place_forget()