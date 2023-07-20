from tkinter import Frame,Label,Entry,Button, ttk, StringVar, messagebox
import sqlite3


class PotsForm(Frame):
    def __init__(self,root,controller_class,pots = None):
        super().__init__(root)
        self.root_window = root
        self.controller_class = controller_class
        self.pot = pots

        self.pots_id = 0


        self.pots_form_label = Label(self,text = "Posude forma", font = ('Arial',15),pady= 15 , bg = "#c8d6e5")
        self.pots_form_label.grid(row=0, column=0 , sticky="N")
      
        self.location_label = Label(self,text= "Najbolja lokacija:", font = ('Arial') , bg = "#c8d6e5")
        self.location_label.grid(row=1,column=0, sticky="N")
        
        self.location_label_input = Entry(self, width= 25, font = ('Arial'), bg = "#ffffff", relief="flat")
        self.location_label_input.grid(row = 2 , column = 0, sticky= "N")

        self.plant_label = Label(self, text="Biljka:", font=('Arial'), bg = "#c8d6e5")
        self.plant_label.grid(row=3, column=0, sticky="N")

        self.plant_var = StringVar()
        self.plant_dropdown_menu = ttk.Combobox(self, textvariable=self.plant_var, width=25, font=('Arial'))
        self.plant_dropdown_menu.grid(row=4, column=0, sticky="N",pady= 5)
       

       

        self.add_button = Button(self, command= self.create_or_update_pot, font= ('Arial'), bg = "#ffffff", relief= "solid",  borderwidth= 1)
        self.add_button.grid(row = 6, column=0 , sticky= "N")

        

        self.back_button = Button(self, text="Natrag", command = self.switch_to_correct_page, font = ('Arial'), bg = "#ffffff", relief= "solid",  borderwidth= 1 )
        self.back_button.grid(row = 7, column=0 , sticky= "N", pady= 5)

        


    def update_UI(self):
        try:
            with sqlite3.connect(self.controller_class.pot_database_location) as conn_pots, sqlite3.connect(self.controller_class.plant_database_location) as conn_plants:
                cursor_pots = conn_pots.cursor()
                cursor_plants = conn_plants.cursor()

                cursor_pots.execute("SELECT * FROM pots WHERE id=?", (self.pots_id,))
                cursor_plants.execute("SELECT id, name FROM plants")

                self.pot = cursor_pots.fetchone()
                self.location_label_input.delete(0, 'end')

                plants = cursor_plants.fetchall()
                plant_options = [f"{id} - {name}" for id, name in plants]

                if "0 - Prazna" not in plant_options:
                    plant_options.insert(0, "0 - Prazna")

                self.plant_dropdown_menu['values'] = plant_options

                if self.pot is not None:
                    selected_option = f"{self.pot[2]} - {self.pot[3]}"
                    if selected_option in plant_options:
                        self.plant_dropdown_menu.current(plant_options.index(selected_option))
                    else:
                        self.plant_dropdown_menu.current(0)
                else:
                    self.plant_dropdown_menu.current(0)

                if self.pot is None:
                    self.pots_form_label.config(text="Posuda forma: Nova Posuda")
                    self.add_button.config(text="Dodaj Posudu")
                else:
                    self.pots_form_label.config(text=f"Posuda forma: Posuda #{self.pot[0]}")
                    self.location_label_input.insert(0, self.pot[1])

                    self.add_button.config(text="Ažuriraj Posudu")
        except sqlite3.Error as e:
            messagebox.showerror("Greška!", f"Nešto je otišlo po zlu: {e}")
          

  
    def create_or_update_pot(self):
        self.location = self.location_label_input.get()
        self.plant_selection = self.plant_dropdown_menu.get()
        self.plant_id = self.plant_selection.split()[0]

        self.plant_name = ""

        self.plant_image_path_location = ""


        with sqlite3.connect(self.controller_class.plant_database_location) as conn_plants:
            cursor_plants = conn_plants.cursor()
            cursor_plants.execute('SELECT * FROM plants WHERE id = ?', (self.plant_id,))
            plant_details = cursor_plants.fetchone()

            if plant_details and self.plant_id != 0:
                self.plant_name = plant_details[1]
                self.plant_image_path_location = plant_details[2]
                min_soil_pH = plant_details[3]
                max_soil_pH = plant_details[4]
                required_moisture = plant_details[5]
                ideal_min_temperature = plant_details[6]
                ideal_max_temperature = plant_details[7]
                ideal_light_hours = plant_details[8]

                with sqlite3.connect(self.controller_class.sensor_database_location) as conn_sensors:
                    cursor_sensors = conn_sensors.cursor()
                    cursor_sensors.execute('SELECT * FROM sensors ORDER BY id DESC LIMIT 1')
                    last_measurement = cursor_sensors.fetchone()

                    if last_measurement:
                        moisture = last_measurement[1]
                        pH_ground = last_measurement[2]
                        light_hours = last_measurement[3]
                        temperature = last_measurement[4]

                        if min_soil_pH <= pH_ground <= max_soil_pH:
                            soil_pH_status = "Optimalna"
                        else:
                            soil_pH_status = "Suboptimalna"

                        if moisture >= required_moisture:
                            moisture_status = "Dovoljno vode"
                        else:
                            moisture_status = "Treba vode"

                        if ideal_min_temperature <= temperature <= ideal_max_temperature:
                            temperature_status = "Idealna"
                        elif ideal_min_temperature > temperature:
                            temperature_status = "Prehladno"
                        elif ideal_max_temperature > temperature:
                            temperature_status = "Pretoplo"
                        else:
                            temperature_status = "Suboptimalno"

                        if light_hours >= ideal_light_hours:
                            light_status = "Dovoljno"
                        else:
                            light_status = "Ne dovoljno"

                        self.status_text = (
                            f"Status:\n"
                            f"pH tla: {soil_pH_status}\n"
                            f"Mokrost tla: {moisture_status}\n"
                            f"Temperatura: {temperature_status}\n"
                            f"Svjetlost: {light_status}"
                        )
                    else:
                        self.status_text = f"Status:\nNema podataka"
            else:
                self.status_text = f"Status:\nPrazna posuda"

        if self.pots_id is not None or self.pots_id != 0:
            self.controller_class.add_or_update_pot(self.location,self.plant_id, self.plant_name, self.plant_image_path_location,self.status_text,self.pots_id)
        else:
            self.controller_class.add_or_update_pot(self.location,self.plant_id,self.plant_name, self.plant_image_path_location, self.status_text)
            
        self.location_label_input.delete(0,'end')
        self.plant_dropdown_menu.delete(0, 'end')

        self.status_text = ""

        
    def show_page(self,plant_id = 0, pot_id = 0):

        self.pots_id = pot_id


        self.update_UI()


        self.place(relx=0.5, rely=0.5,anchor="center")

    def hide_page(self):
        self.place_forget()

    def switch_to_correct_page(self):

        if self.pots_id != 0:
            self.controller_class.pot_id = self.pots_id
            self.controller_class.switch_to_individual_pot_page()
        else:
            self.controller_class.pot_id = 0
            self.controller_class.switch_to_pots_page()

