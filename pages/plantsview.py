from tkinter import Frame,Button
from PIL import Image, ImageTk
import sqlite3

class PlantsView(Frame):
    def __init__(self,master,controller):
        super().__init__(master)
        self.master = master
        self.controller = controller

      

        self.plant_buttons = []

        
        self.add_plant_button = Button(self, text="Dodaj novu biljku", font= (25), command = self.controller.switch_to_plant_form)
        

       
    
    def load_and_create_plant_buttons(self):
       conn = sqlite3.connect(self.controller.db_plant_path)
       cursor = conn.cursor()

       try:
          cursor.execute("SELECT id,name,picture FROM plants")
       except sqlite3.Error as e:
          print(f"Something went wrong: {e}")
       else: 
          plants = cursor.fetchall()

          # Clear existing plant buttons
          for button in self.plant_buttons:
                button.destroy()
          self.plant_buttons = []

          max_buttons_per_row = 3
          num_buttons = len(plants)
          num_rows = (num_buttons + max_buttons_per_row - 1) // max_buttons_per_row

          for index, plant in enumerate(plants):
                row = index // max_buttons_per_row + 1
                column = index % max_buttons_per_row + 1

                image_path = plant[2]
                image = Image.open(image_path)
                image = image.resize((95, 95))
                photo = ImageTk.PhotoImage(image)

                button = Button(self, text=plant[1], image=photo, command=lambda p=plant: self.show_plant_details(p[0]))
                button.image = photo
                button.config(compound="left", padx=10, font=(25))
                button.grid(row=row, column=column, padx=5, sticky="WE", pady=5)

                self.plant_buttons.append(button)

          self.add_plant_button.grid(row=num_rows + 1,columnspan=max_buttons_per_row, column=1, sticky= "WE", pady=10)
       finally:
          conn.close()    
       
    
    def show_plant_details(self, plant_id):

        self.controller.plant_id = plant_id
        self.controller.switch_to_individual_plant_view()

    
  

    

    def show(self,plant_id = None):
      self.master.update_idletasks()  # Ensure the window size is updated

      self.place(relx=0.5, rely=0.5, anchor="center")

      self.load_and_create_plant_buttons()
    
    def hide(self):
       self.place_forget()