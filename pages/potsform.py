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
            plant_options.insert(0, "0 - Prazna")
            self.plant_dropdown['values'] = plant_options


            if self.pot is None:
                self.add_button.config(text= "Dodaj Posudu") 
            else:
                self.location_label_entry.insert(0,self.pot[1])

                self.add_button.config(text = "Ažurijaj Posudu")
        finally:
            conn.close()
            conn2.close()
          

  
    def create_or_update_pot(self):
        self.location = self.location_label_entry.get()
        self.plant_selection = self.plant_dropdown.get()
        self.plant_id = self.plant_selection.split()[0]

        print(self.location,self.plant_id)

        self.location_label_entry.delete(0,'end')
        self.plant_dropdown.delete(0, 'end')

        return
        
            

        
    def show(self,plant_id = None, pot_id = None):
        self.master.update_idletasks()  # Ensure the window size is updated

        self.pots_id = pot_id

        print(self.pots_id)

        self.update_UI_accordingly()


        self.place(relx=0.5, rely=0.5,anchor="center")

    def hide(self):
        self.place_forget()
