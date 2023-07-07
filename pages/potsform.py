from tkinter import Frame,Label,Entry,Button, ttk, StringVar, messagebox
import sqlite3


class PotsForm(Frame):
    def __init__(self,master,controller,pots = None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.pot = pots

        self.pots_id = None

        self.status = None

        self.pots_form_label = Label(self,text = "Posude forma", font = (45),pady= 15)
        self.pots_form_label.grid(row=0, column=0 , sticky="N")
      
        self.location_label = Label(self,text= "Najbolja lokacija:", font = (25))
        self.location_label.grid(row=1,column=0, sticky="N")
        self.location_label_entry = Entry(self, width= 25, font = (15))
        self.location_label_entry.grid(row = 2 , column = 0, sticky= "N")

        self.plant_label = Label(self, text="Biljka:", font=(25))
        self.plant_label.grid(row=3, column=0, sticky="N")

        self.plant_var = StringVar()
        self.plant_dropdown = ttk.Combobox(self, textvariable=self.plant_var, width=25, font=(15))
        self.plant_dropdown.grid(row=4, column=0, sticky="N",pady= 5)
       

       

        self.add_button = Button(self, command= self.create_or_update_pot, font= (25))
        self.add_button.grid(row = 6, column=0 , sticky= "N")

        

        self.back_button = Button(self, text="Natrag", command = self.controller.switch_to_pot_view, font = (25))
        self.back_button.grid(row = 7, column=0 , sticky= "N", pady= 5)

        


    def update_UI_accordingly(self):
        conn = sqlite3.connect(self.controller.db_pot_path)
        conn2 = sqlite3.connect(self.controller.db_plant_path)
        cursor = conn.cursor()
        cursor2 = conn2.cursor()

        try:
            cursor.execute("SELECT * FROM pots WHERE id=?", (self.pots_id,))    
            cursor2.execute("SELECT id, name FROM plants")
        except sqlite3.Error as e:
            messagebox.showerror("Greška!",f"Nešto je otišlo po zlu: {e}")
        else:
            self.pot = cursor.fetchone()
            self.location_label_entry.delete(0,'end')

            plants = cursor2.fetchall()
            plant_options = [f"{id} - {name}" for id, name in plants]

            if "0 - Prazna" not in plant_options:
                plant_options.insert(0, "0 - Prazna")

            self.plant_dropdown['values'] = plant_options

            if self.pot is not None:
                selected_option = f"{self.pot[2]} - {self.pot[3]}" 
                if selected_option in plant_options:
                    self.plant_dropdown.current(plant_options.index(selected_option))
                else:
                    # Handle case when the selected plant_id is not found in the dropdown options
                    self.plant_dropdown.current(0)
            else:
                self.plant_dropdown.current(0)


            if self.pot is None:
                self.pots_form_label.config(text = "Posuda forma")
                self.add_button.config(text= "Dodaj Posudu") 
            else:
                self.pots_form_label.config(text= f"Posuda forma: Posuda #{self.pot[0]}")
                self.location_label_entry.insert(0,self.pot[1])

                self.add_button.config(text = "Ažuriraj Posudu")
        finally:
            conn.close()
            conn2.close()
          

  
    def create_or_update_pot(self):
        self.location = self.location_label_entry.get()
        self.plant_selection = self.plant_dropdown.get()
        self.plant_id = self.plant_selection.split()[0]

        self.plant_name = ""

        self.plant_picture_location = ""

        #print(self.location,self.plant_id)

        conn_plants = sqlite3.connect(self.controller.db_plant_path)
        cursor_plants = conn_plants.cursor()

        cursor_plants.execute('SELECT * FROM plants WHERE id = ?', (self.plant_id,))
        plant_details = cursor_plants.fetchone()

        if plant_details and self.plant_id != 0:
            self.plant_name = plant_details[1]
            self.plant_picture_location = plant_details[2]
            min_soil_pH = plant_details[3]
            max_soil_pH = plant_details[4]
            required_ground_moisture = plant_details[5]
            ideal_min_temperature = plant_details[6]
            ideal_max_temperature = plant_details[7]
            ideal_light = plant_details[8]

            conn_sensors = sqlite3.connect(self.controller.db_sensor_path)
            cursor_sensors = conn_sensors.cursor()
            cursor_sensors.execute('SELECT * FROM sensors ORDER BY id DESC LIMIT 1')
            last_measurement = cursor_sensors.fetchone()

            if last_measurement:
                ground_moisture = last_measurement[1]
                pH_ground = last_measurement[2]
                light_lux = last_measurement[3]
                temperature = last_measurement[4]
            
                # Compare values with the plant requirements
                if min_soil_pH <= pH_ground <= max_soil_pH:
                    soil_pH_status = "Optimalna"
                else:
                    soil_pH_status = "Suboptimalna"
            
                if ground_moisture >= required_ground_moisture:
                    moisture_status = "Dovoljno vode"
                else:
                    moisture_status = "Treba vode"
            
                if ideal_min_temperature <= temperature <= ideal_max_temperature:
                    temperature_status = "Idealna"
                else:
                    temperature_status = "Suboptimalna"
            
                if light_lux >= ideal_light:
                    light_status = "Dovoljno"
                else:
                    light_status = "Ne dovoljno"
            
                self.status_text = f"Status: \n pH tla: {soil_pH_status}\nMokrost tla: {moisture_status}\nTemperatura: {temperature_status}\nSvjetlost: {light_status}"
            else:
                #print("No measurements found in the sensors database")
                self.status_text = f"Status: \n Nema podataka"
            conn_sensors.close()
        else:
            #print("Plant details not found in the plants database")
            self.status_text = f"Status: \nPrazna posuda"
        conn_plants.close()

        #print(self.status_text)

        if self.pots_id is not None or self.pots_id != 0:
            self.controller.add_pot(self.location,self.plant_id, self.plant_name, self.plant_picture_location,self.status_text,self.pots_id)
        else:
            self.controller.add_pot(self.location,self.plant_id,self.plant_name, self.plant_picture_location, self.status_text)
            
        self.location_label_entry.delete(0,'end')
        self.plant_dropdown.delete(0, 'end')

        self.status_text = None

        


        

        
            

        
    def show(self,plant_id = None, pot_id = None):
        self.master.update_idletasks()  # Ensure the window size is updated

        self.pots_id = pot_id

        print(self.pots_id)

        self.update_UI_accordingly()


        self.place(relx=0.5, rely=0.5,anchor="center")

    def hide(self):
        self.place_forget()
