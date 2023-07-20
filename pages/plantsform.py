from tkinter import Frame,Label,Entry,Button, filedialog, messagebox
import sqlite3


class PlantsForm(Frame):
    def __init__(self,root,controller_class,current_plant = None):
        super().__init__(root)
        self.root_window = root
        self.controller_class = controller_class
        self.current_plant = current_plant

        self.current_plant_id = 0

      

        self.plants_form_label = Label(self,font = ('Arial', 15),pady= 15 , bg = "#c8d6e5")
        self.plants_form_label.grid(row=0, column=0 , sticky="N")

        self.plants_form_name_label = Label(self,text = "Ime", font = ('Arial'), bg = "#c8d6e5")
        self.plants_form_name_label.grid(row=1, column=0 , sticky="N")

        self.plants_form_name_input = Entry(self, width= 25, font = ('Arial'), bg = "#ffffff", relief="flat")
        self.plants_form_name_input.grid(row=2, column=0 , sticky="N", pady= 5)

        self.plants_form_picture_label = Label(self,text = "Slika",font = ('Arial') , bg = "#c8d6e5" )
        self.plants_form_picture_label.grid(row=3, column=0 , sticky="n")

        self.plants_form_picture_input = Entry(self, width= 25, font = ('Arial'), bg = "#ffffff", relief="flat")
        self.plants_form_picture_input.grid(row=4, column=0 , sticky="n", padx= 5,  pady= 5)

        self.browse_button = Button(self, text="Odaberi sliku", command=self.browse_picture, font= ('Arial'), bg = "#ffffff", relief="solid",  borderwidth= 1)
        self.browse_button.grid(row=4, column=1, sticky="N")

        self.plants_form_soil_label = Label(self,text = "Minimalna pH vrijednost tla", font = ('Arial') , bg = "#c8d6e5")
        self.plants_form_soil_label.grid(row=5, column=0 , sticky="n")

        self.plants_form_soil_input = Entry(self, width= 25, font = (15), bg = "#ffffff", relief="flat")
        self.plants_form_soil_input.grid(row=6, column=0 , sticky="N", pady= 5)

        self.plants_form_max_soil_label = Label(self,text = "Maximalna pH vrijednost tla", font = ('Arial') , bg = "#c8d6e5")
        self.plants_form_max_soil_label.grid(row=7, column=0 , sticky="N")

        self.plants_form_max_soil_input = Entry(self, width= 25, font = (15), bg = "#ffffff" , relief="flat")
        self.plants_form_max_soil_input.grid(row=8, column=0 , sticky="N", pady= 5)

        self.plants_form_required_moisture_label = Label(self,text = "Potrebna vlažnost tla u mm", font = ('Arial') , bg = "#c8d6e5")
        self.plants_form_required_moisture_label.grid(row=9, column=0 , sticky="N")

        self.plants_form_required_moisture_input = Entry(self, width= 25, font = ('Arial'), bg = "#ffffff" , relief="flat")
        self.plants_form_required_moisture_input.grid(row=10, column=0 , sticky="N", pady= 5)

    
        self.plants_form_minimum_temperature_label = Label(self,text = "Minimalna temperatura", font = ('Arial') , bg = "#c8d6e5")
        self.plants_form_minimum_temperature_label.grid(row=11, column=0 , sticky="N")
        
        self.plants_form_minimum_temperature_input = Entry(self, width= 25, font = ('Arial'), bg = "#ffffff", relief="flat")
        self.plants_form_minimum_temperature_input.grid(row=12, column=0 , sticky="N",pady= 5)

        self.plants_form_maximum_temperature_label = Label(self,text = "Maximalna temperatura", font = ('Arial') , bg = "#c8d6e5")
        self.plants_form_maximum_temperature_label.grid(row=13, column=0 , sticky="N")

        self.plants_form_maximum_temperature_input = Entry(self, width= 25, font = ('Arial'), bg = "#ffffff", relief="flat")
        self.plants_form_maximum_temperature_input.grid(row=14, column=0 , sticky="N",pady= 5)

        self.plants_form_light_label = Label(self,text = "Potrebna svjetlost u satima", font = ('Arial') , bg = "#c8d6e5")
        self.plants_form_light_label.grid(row = 15, column=0 , sticky="N")

        self.plants_form_light_input = Entry(self, width= 25, font = ('Arial'), bg = "#ffffff", relief="flat")
        self.plants_form_light_input.grid(row=16, column=0 , sticky="N", pady= 5)

        self.plants_form_substrate_label = Label(self,text = "Preporuka za dodavanje suprata", font = ('Arial') , bg = "#c8d6e5")
        self.plants_form_substrate_label.grid(row=17, column=0 , sticky="N")

        self.plants_form_substrate_input = Entry(self, width= 25, font = ('Arial'), bg = "#ffffff" , relief="flat")
        self.plants_form_substrate_input.grid(row=18, column=0 , sticky="N",pady= 5)

       

        self.add_button = Button(self, command= self.create_or_update_plant, font= ('Arial'), bg = "#ffffff" , relief= "solid",  borderwidth= 1)
        self.add_button.grid(row = 19, column=0 , sticky= "N")

        

        self.back_button = Button(self, text="Natrag", command = self.switch_to_correct_page, font = ('Arial'), bg = "#ffffff", relief= "solid",  borderwidth= 1)
        self.back_button.grid(row = 20, column=0 , sticky= "N", pady= 5)

        


    def update_UI(self):
        try:
            with sqlite3.connect(self.controller_class.plant_database_location) as conn_plants:
                cursor_plants = conn_plants.cursor()
                cursor_plants.execute("SELECT * FROM plants WHERE id=?", (self.current_plant_id,))
                self.current_plant = cursor_plants.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror("Greška!", f"Nešto je otišlo po zlu: {e}")
        else:
            self.plants_form_name_input.delete(0, 'end')
            self.plants_form_picture_input.delete(0, 'end')
            self.plants_form_soil_input.delete(0, 'end')
            self.plants_form_max_soil_input.delete(0, 'end')
            self.plants_form_minimum_temperature_input.delete(0, 'end')
            self.plants_form_maximum_temperature_input.delete(0, 'end')
            self.plants_form_light_input.delete(0, 'end')
            self.plants_form_substrate_input.delete(0, 'end')
            self.plants_form_required_moisture_input.delete(0, 'end')

            if self.current_plant is None or self.current_plant == 0:
                self.add_button.config(text="Dodaj biljku")
                self.plants_form_label.config(text="Biljke forma")
            else:
                self.plants_form_label.config(text=f"Biljke forma: {self.current_plant[1]}")
                self.plants_form_name_input.insert(0, self.current_plant[1])
                self.plants_form_picture_input.insert(0, self.current_plant[2])
                self.plants_form_soil_input.insert(0, self.current_plant[3])
                self.plants_form_max_soil_input.insert(0, self.current_plant[4])
                self.plants_form_required_moisture_input.insert(0, self.current_plant[5])
                self.plants_form_minimum_temperature_input.insert(0, self.current_plant[6])
                self.plants_form_maximum_temperature_input.insert(0, self.current_plant[7])
                self.plants_form_light_input.insert(0, self.current_plant[8])
                self.plants_form_substrate_input.insert(0, self.current_plant[9])
                self.add_button.config(text="Ažuriraj biljku")
          

    def browse_picture(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        self.plants_form_picture_input.delete(0, "end")
        self.plants_form_picture_input.insert(0, file_path)

  
    def create_or_update_plant(self):
        self.name = self.plants_form_name_input.get()
        self.picture_path = self.plants_form_picture_input.get()
        self.soil = self.plants_form_soil_input.get()
        self.max_soil = self.plants_form_max_soil_input.get()
        self.min_temperature = self.plants_form_minimum_temperature_input.get()
        self.max_temperature = self.plants_form_maximum_temperature_input.get()
        self.light = self.plants_form_light_input.get()
        self.substrate = self.plants_form_substrate_input.get()
        self.required_moisture = self.plants_form_required_moisture_input.get()

        if self.current_plant is None or self.current_plant == 0:
            self.controller_class.add_or_update_plants(self.name,self.picture_path,self.soil,self.max_soil,self.required_moisture,self.min_temperature,self.max_temperature,self.light,self.substrate)
            self.plants_form_name_input.delete(0,'end')

            self.plants_form_picture_input.delete(0,'end')


            self.plants_form_soil_input.delete(0,'end')

            self.plants_form_max_soil_input.delete(0,'end')



            self.plants_form_minimum_temperature_input.delete(0,'end')

            self.plants_form_maximum_temperature_input.delete(0,'end')


            self.plants_form_light_input.delete(0,'end')


            self.plants_form_substrate_input.delete(0,'end')

            self.plants_form_required_moisture_input.delete(0,'end')
        else:
            self.controller_class.add_or_update_plants(self.name,self.picture_path,self.soil,self.max_soil,self.required_moisture,self.min_temperature,self.max_temperature,self.light,self.substrate, self.current_plant[0])

        
    def show_page(self,plant_id = 0, pot_id = 0):

        self.current_plant_id = plant_id

        self.place(relx=0.5, rely=0.5,anchor="center")

        self.update_UI()

    def hide_page(self):
        self.place_forget()
    

    def switch_to_correct_page(self):
        if self.current_plant_id != 0:
            self.controller_class.plant_id = self.current_plant_id
            self.controller_class.switch_to_individual_plant_page()
        else:
            self.controller_class.plant_id = 0
            self.controller_class.switch_to_plants_page()