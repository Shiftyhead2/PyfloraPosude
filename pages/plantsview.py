from tkinter import Frame,Label,Button,messagebox
import sqlite3

class PlantsView(Frame):
    def __init__(self,master,controller):
        super().__init__(master)
        self.master = master
        self.controller = controller

      

        self.plant_buttons = []

        self.plants_label = Label(self,text = "Evidencija biljka", font = (45))

        self.plants_label.grid(row=0, column= 1, sticky= "N")
        self.add_plant_button = Button(self, text="Dodaj novu biljku", command = self.controller.switch_to_plant_form)

        

        self.load_and_create_plant_buttons()

       
    
    def load_and_create_plant_buttons(self):
       conn = sqlite3.connect(self.controller.db_plant_path)
       cursor = conn.cursor()


       cursor.execute("SELECT id,name,picture FROM plants")
       plants = cursor.fetchall()

       conn.close()

       for index, plant in enumerate(plants):
            button = Button(self, text=plant[1], command=lambda p=plant: self.show_plant_details(p[0],p[1],p[2]))
            button.grid(row=index + 1, column=1, pady=5)
            self.plant_buttons.append(button)
      
       
       self.add_plant_button.grid(row=len(self.plant_buttons) + 1, column=1, pady=10)
    
    def show_plant_details(self, plant_id, plant_name, plant_picture_location):

        messagebox.showinfo("Plant Details", f"Plant ID: {plant_id}, Plant name: {plant_name}, Plant picture location: {plant_picture_location}")
        self.controller.plant_id = plant_id
    
  

    

    def show(self,plant_id = None):
      self.master.update_idletasks()  # Ensure the window size is updated

      self.place(relx=0.5, rely=0.5, anchor="center")

      self.load_and_create_plant_buttons()
    
    def hide(self):
       self.place_forget()