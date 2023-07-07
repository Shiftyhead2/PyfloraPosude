from tkinter import Frame,Button
from PIL import Image, ImageTk
import sqlite3

class PotsView(Frame):
    def __init__(self,master,controller):
        super().__init__(master)
        self.master = master
        self.controller = controller

      

        self.pot_buttons = []

        
        self.add_pot_button = Button(self, text="Dodaj novu posudu", font= (25), command = self.controller.switch_to_pot_form)
        

       
    
    def load_and_create_pot_buttons(self):
       conn = sqlite3.connect(self.controller.db_pot_path)
       cursor = conn.cursor()

       try:
          cursor.execute("SELECT id,location,plant_name, plant_id, plant_picture_location,status FROM pots")
       except sqlite3.Error as e:
          print(f"Something went wrong: {e}")
       else: 
          pots = cursor.fetchall()

          # Clear existing plant buttons
          for button in self.pot_buttons:
                button.destroy()
          self.pot_buttons = []

          max_buttons_per_row = 3
          num_buttons = len(pots)
          num_rows = (num_buttons + max_buttons_per_row - 1) // max_buttons_per_row

          

          for index, pot in enumerate(pots):
                row = index // max_buttons_per_row + 1
                column = index % max_buttons_per_row + 1
                
                if pot[3] > 0:
                    image_path = pot[4]
                    if image_path:
                     image = Image.open(image_path)
                     image = image.resize((95, 95))
                     photo = ImageTk.PhotoImage(image)
                     button = Button(self, text=f"Posuda #{pot[0]}", command=lambda p=pot: self.show_pot_details(p[0]))
                     button.image = photo
                     button.config(compound="left", image=photo, padx=10, font=(25))
                     button.grid(row=row, column=column, padx=5, sticky="WE", pady=5)
                    else:
                       button = Button(self, text=f"Posuda #{pot[0]}", command=lambda p=pot: self.show_pot_details(p[0]))
                       button.config(compound="left", padx=10, font=(25))
                       button.grid(row=row, column=column, padx=5, sticky="WE", pady=5)
                else:
                     button = Button(self, text=f"Posuda #{pot[0]} \n {pot[5]}", command=lambda p=pot: self.show_pot_details(p[0]))
                     button.config(compound="left", padx=10, font=(25))
                     button.grid(row=row, column=column, padx=5, sticky="WE", pady=5)
                
                self.pot_buttons.append(button)

          self.add_pot_button.grid(row=num_rows + 1,columnspan=max_buttons_per_row, column=1, sticky= "WE", pady=10)
       finally:
          conn.close()    
       
    
    def show_pot_details(self, pot_id):
        self.controller.pot_id = pot_id

        self.controller.switch_to_individual_pot_view()

    
    def show(self,plant_id = None, pot_id = None):
      self.master.update_idletasks()  # Ensure the window size is updated

      self.place(relx=0.5, rely=0.5, anchor="center")

      self.load_and_create_pot_buttons()
    
    def hide(self):
       self.place_forget()