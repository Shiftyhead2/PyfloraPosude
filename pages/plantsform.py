from tkinter import Frame,Label,Entry,Button, filedialog, messagebox
import sqlite3


class PlantsForm(Frame):
    def __init__(self,master,controller,plant = None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.plant = plant

        self.plant_id = None

      

        self.plants_form_label = Label(self,text = "Biljke forma", font = (45),pady= 15)
        self.plants_form_label.grid(row=0, column=0 , sticky="N")

        self.plants_form_name_label = Label(self,text = "Ime", font = (25))
        self.plants_form_name_label.grid(row=1, column=0 , sticky="N")
        self.plants_form_name_entry = Entry(self, width= 25, font = (15))
        self.plants_form_name_entry.grid(row=2, column=0 , sticky="N", pady= 5)

        self.plants_form_picture_label = Label(self,text = "Slika",font = (25))
        self.plants_form_picture_label.grid(row=3, column=0 , sticky="n")
        self.plants_form_picture_entry = Entry(self, width= 25, font = (15))
        self.plants_form_picture_entry.grid(row=4, column=0 , sticky="n", padx= 5,  pady= 5)
        self.browse_button = Button(self, text="Odaberi sliku", command=self.browse_picture, font= (25))
        self.browse_button.grid(row=4, column=1, sticky="N")

        self.plants_form_soil_label = Label(self,text = "Minimalna pH vrijednost tla", font = (25))
        self.plants_form_soil_label.grid(row=5, column=0 , sticky="n")
        self.plants_form_soil_entry = Entry(self, width= 25, font = (15))
        self.plants_form_soil_entry.grid(row=6, column=0 , sticky="N", pady= 5)

        self.plants_form_max_soil_label = Label(self,text = "Maximalna pH vrijednost tla", font = (25))
        self.plants_form_max_soil_label.grid(row=7, column=0 , sticky="N")
        self.plants_form_max_soil_entry = Entry(self, width= 25, font = (15))
        self.plants_form_max_soil_entry.grid(row=8, column=0 , sticky="N", pady= 5)

        self.plants_form_required_moisture_label = Label(self,text = "Potrebna vlažnost tla(u mm)", font = (25))
        self.plants_form_required_moisture_label.grid(row=9, column=0 , sticky="N")
        self.plants_form_required_moisture_entry = Entry(self, width= 25, font = (15))
        self.plants_form_required_moisture_entry.grid(row=10, column=0 , sticky="N", pady= 5)

    
        self.plants_form_minimum_temperature_label = Label(self,text = "Minimalna idealna temperatura", font = (25))
        self.plants_form_minimum_temperature_label.grid(row=11, column=0 , sticky="N")
        self.plants_form_minimum_temperature_entry = Entry(self, width= 25, font = (15))
        self.plants_form_minimum_temperature_entry.grid(row=12, column=0 , sticky="N",pady= 5)

        self.plants_form_maximum_temperature_label = Label(self,text = "Maximalna idealna temperatura", font = (25))
        self.plants_form_maximum_temperature_label.grid(row=13, column=0 , sticky="N")
        self.plants_form_maximum_temperature_entry = Entry(self, width= 25, font = (15))
        self.plants_form_maximum_temperature_entry.grid(row=14, column=0 , sticky="N",pady= 5)

        self.plants_form_light_label = Label(self,text = "Potrebna svjetlost u satima", font = (25))
        self.plants_form_light_label.grid(row = 15, column=0 , sticky="N")
        self.plants_form_light_entry = Entry(self, width= 25, font = (15))
        self.plants_form_light_entry.grid(row=16, column=0 , sticky="N", pady= 5)

        self.plants_form_substrate_label = Label(self,text = "Preporuka za dodavanje suprata", font = (25))
        self.plants_form_substrate_label.grid(row=17, column=0 , sticky="N")
        self.plants_form_substrate_entry = Entry(self, width= 25, font = (15))
        self.plants_form_substrate_entry.grid(row=18, column=0 , sticky="N",pady= 5)

       

        self.add_button = Button(self, command= self.create_or_update_plant, font= (25))
        self.add_button.grid(row = 19, column=0 , sticky= "N")

        

        self.back_button = Button(self, text="Natrag", command = self.controller.switch_to_plant_view, font = (25))
        self.back_button.grid(row = 20, column=0 , sticky= "N", pady= 5)

        


    def update_UI_accordingly(self):
        conn = sqlite3.connect(self.controller.db_plant_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM plants WHERE id=?", (self.plant_id,))    
        except sqlite3.Error as e:
            messagebox.showerror("Greška!",f"Nešto je otišlo po zlu: {e}")
        else:
            self.plant = cursor.fetchone()

            self.plants_form_name_entry.delete(0,'end')

            self.plants_form_picture_entry.delete(0,'end')


            self.plants_form_soil_entry.delete(0,'end')

            self.plants_form_max_soil_entry.delete(0,'end')



            self.plants_form_minimum_temperature_entry.delete(0,'end')

            self.plants_form_maximum_temperature_entry.delete(0,'end')


            self.plants_form_light_entry.delete(0,'end')


            self.plants_form_substrate_entry.delete(0,'end')

            self.plants_form_required_moisture_entry.delete(0,'end')


            if self.plant is None:
                self.add_button.config(text= "Dodaj biljku") 
            else:
                self.plants_form_name_entry.insert(0,self.plant[1])

                self.plants_form_picture_entry.insert(0,self.plant[2])


                self.plants_form_soil_entry.insert(0,self.plant[3])

                self.plants_form_max_soil_entry.insert(0,self.plant[4])

                self.plants_form_required_moisture_entry.insert(0,self.plant[5])



                self.plants_form_minimum_temperature_entry.insert(0,self.plant[6])

                self.plants_form_maximum_temperature_entry.insert(0,self.plant[7])


                self.plants_form_light_entry.insert(0,self.plant[8])


                self.plants_form_substrate_entry.insert(0,self.plant[9])

                self.add_button.config(text = "Ažuriraj biljku")
        finally:
            conn.close()
          

    def browse_picture(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        self.plants_form_picture_entry.delete(0, "end")
        self.plants_form_picture_entry.insert(0, file_path)

  
    def create_or_update_plant(self):
        self.name = self.plants_form_name_entry.get()
        self.picture_path = self.plants_form_picture_entry.get()
        self.soil = self.plants_form_soil_entry.get()
        self.max_soil = self.plants_form_max_soil_entry.get()
        self.min_temperature = self.plants_form_minimum_temperature_entry.get()
        self.max_temperature = self.plants_form_maximum_temperature_entry.get()
        self.light = self.plants_form_light_entry.get()
        self.substrate = self.plants_form_substrate_entry.get()
        self.required_moisture = self.plants_form_required_moisture_entry.get()

        if self.plant is None or self.plant == 0:
            self.controller.add_or_update_plants(self.name,self.picture_path,self.soil,self.max_soil,self.required_moisture,self.min_temperature,self.max_temperature,self.light,self.substrate,self.plant)
            self.plants_form_name_entry.delete(0,'end')

            self.plants_form_picture_entry.delete(0,'end')


            self.plants_form_soil_entry.delete(0,'end')

            self.plants_form_max_soil_entry.delete(0,'end')



            self.plants_form_minimum_temperature_entry.delete(0,'end')

            self.plants_form_maximum_temperature_entry.delete(0,'end')


            self.plants_form_light_entry.delete(0,'end')


            self.plants_form_substrate_entry.delete(0,'end')

            self.plants_form_required_moisture_entry.delete(0,'end')
        else:
            self.controller.add_or_update_plants(self.name,self.picture_path,self.soil,self.max_soil,self.required_moisture,self.min_temperature,self.max_temperature,self.light,self.substrate, self.plant[0])

        
    def show(self,plant_id = None, pot_id = None):
        self.master.update_idletasks()  # Ensure the window size is updated

        self.plant_id = plant_id

        print(self.plant_id)

        self.update_UI_accordingly()


        self.place(relx=0.5, rely=0.5,anchor="center")

    def hide(self):
        self.place_forget()
