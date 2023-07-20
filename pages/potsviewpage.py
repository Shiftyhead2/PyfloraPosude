from tkinter import Frame,Button
from PIL import Image, ImageTk
import sqlite3

class PotsViewPage(Frame):
    def __init__(self,root,controller_class):
        super().__init__(root)
        self.root_window = root
        self.controller_class = controller_class

      

        self.current_pot_buttons = []

        
        self.add_pot_button = Button(self, text="Dodaj novu posudu", font= ('Arial'), bg = "#ffffff", command = self.controller_class.switch_to_pots_form, relief= "solid",  borderwidth= 1)

        self.load_and_create_pot_buttons()
        

       
    def load_and_create_pot_buttons(self):
      try:
            with sqlite3.connect(self.controller_class.pot_database_location) as conn_pots:
               cursor_pots = conn_pots.cursor()
               cursor_pots.execute("SELECT id, location, plant_name, plant_id, plant_picture_location, status FROM pots")
               pots = cursor_pots.fetchall()

               for button in self.current_pot_buttons:
                  button.destroy()
               self.current_pot_buttons = []

               max_buttons_per_row = 4
               num_buttons = len(pots)
               num_rows = (num_buttons + max_buttons_per_row - 1) // max_buttons_per_row

               for index, pot in enumerate(pots):
                     row = index // max_buttons_per_row + 1
                     column = index % max_buttons_per_row + 1
                     button = Button(self, text=f"Posuda #{pot[0]}", bg="#ffffff", command=lambda p=pot: self.show_pot_details(p[0]), relief="solid", border=0)

                     if pot[3] > 0 and pot[4]:
                        image = Image.open(pot[4])
                        image = image.resize((100, 100))
                        photo = ImageTk.PhotoImage(image)
                        button.image = photo
                        button.config(compound="left", image=photo, padx=10, font=('Arial', 15))
                     else:
                        button.config(compound="left", padx=10, font=('Arial', 15), text=f"Posuda #{pot[0]} \n Status:Prazna posuda")

                     button.grid(row=row, column=column, padx=5, pady=5, sticky="news")
                     self.current_pot_buttons.append(button)

               self.add_pot_button.grid(row=num_rows + 1, columnspan=max_buttons_per_row, column=1, sticky="WE", pady=10)
      except sqlite3.Error as e:
            print(f"Something went wrong: {e}")
       
    
    def show_pot_details(self, pot_id):
        self.controller_class.pot_id = pot_id

        self.controller_class.switch_to_individual_pot_page()

    
    def show_page(self,plant_id = 0, pot_id = 0): 
      self.place(relx=0.5, rely=0.5, anchor="center")

      self.load_and_create_pot_buttons()
    
    def hide_page(self):
        self.place_forget()