import tkinter as tk
from tkinter import Frame,Label,Button, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3
import random

class IndividualPotView(Frame):
    def __init__(self,master,controller,pot_id = None):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.pot_id = pot_id
        self.pot = None
        self.measurements = None


        self.pot_label = Label(self)
        self.pot_label.grid(row = 0, column=1, sticky= "W", pady= 10)

        self.pot_location_label = Label(self)
        self.pot_location_label.grid(row = 1, column= 1,sticky= "W")

        self.plant_name_label = Label(self,text= "Posuđena biljka:")
        self.plant_name_label.grid(row = 2, column= 1,sticky= "W")

        self.plant_status_label = Label(self)
        self.plant_status_label.grid(row = 3 , column= 1, sticky= "W", pady= 10)

        self.measurements_frame = Frame(self)
        self.measurements_frame.grid(row=4, column=1, sticky="W", pady=10)
        self.measurements_labels = []


        self.back_button = Button(self,text= "Natrag", command= self.controller.switch_to_pot_view, font = (25))
        

        self.update_button = Button(self,text= "Ažuriraj", command= self.update_pot, font = (25))
        

        self.delete_button = Button(self,text= "Izbriši posudu", command= self.delete_pot, font = (25))


        self.show_chart_button = Button(self, text="Prikaži graf", command=self.show_chart, font = (25))
        self.show_chart_button.grid(row=7, column=1, sticky="WE")

        self.show_pie_button = Button(self, text="Prikaži pie chart", command=self.show_pie_chart, font = (25))
        self.show_pie_button.grid(row=7, column=2, sticky="WE")

        self.show_histogram_button = Button(self, text="Prikaži histogram", command=self.show_histogram_chart, font = (25))
        self.show_histogram_button.grid(row=7, column=3, sticky="WE")

       
        
        


    

    def show(self,plant_id = None, pot_id = None):
        self.master.update_idletasks()  # Ensure the window size is updated

        self.place(relx=0.4, rely=0.5,anchor="w")

        self.pot_id = pot_id

        self.get_specific_plant()

        self.show_measurements()

    def hide(self):
        self.place_forget()
    
    def get_specific_plant(self):
        conn = sqlite3.connect(self.controller.db_pot_path)
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT id,location,plant_name, plant_id,status FROM pots WHERE id=?",(self.pot_id,))
        except sqlite3.Error as e:
            messagebox.showerror(f"Greška!", f"Nešto je otišlo po zlu: {e}")
        else:
            self.pot = cursor.fetchone()
            print(self.measurements)
            self.pot_location_label.config(text= f"Lokacija: {self.pot[1]}")
            self.pot_label.config(text = f"Posuda #{self.pot[0]}", font = (65))
            if self.pot[3] > 0:
                self.plant_name_label.config(text = f"Posuđenja biljka: {self.pot[2]}")
            else:
                self.plant_name_label.config(text = f"Posuđenja biljka:")
            self.plant_status_label.config(text = f"{self.pot[4]}")
            
        finally:
            conn.close()
    
    def show_measurements(self):
        # Clear the existing measurement labels
        for label in self.measurements_labels:
            label.destroy()
        self.measurements_labels = []

        # Retrieve measurements from the sensors database
        try:
            conn = sqlite3.connect(self.controller.db_sensor_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sensors")
        except sqlite3.Error as e:
            messagebox.showerror(f"Greška!", f"Nešto je otišlo po zlu: {e}")
        else:
            self.measurements = cursor.fetchall()
            # Create labels to display the measurements
            if len(self.measurements) != 0:
                for i, measurement in enumerate(self.measurements):
                    sensor_id, ground_moisture, pH_ground, light_lux, temperature = measurement

                    # Create and grid the labels
                    label_text = f"Sensor #{sensor_id}: Mokrost tla={ground_moisture}, pH={pH_ground}, Sunčevih sati: {light_lux}, Temp={temperature}"
                    label = Label(self.measurements_frame, text=label_text)
                    label.grid(row=i, column=0, sticky="W")
                    self.measurements_labels.append(label)
                    self.back_button.grid(row = 5 + i, column= 1, sticky= "WE" , pady = 5)
                    self.update_button.grid(row = 4 + i, column= 1, sticky= "WE" , pady = 5)
                    self.delete_button.grid(row = 6 + i, column= 1, sticky= "WE" , pady = 5)
                    self.show_chart_button.grid(row = 7 + i, column = 1 , padx = 5)
                    self.show_pie_button.grid(row = 7 + i , column= 2 , padx = 5)
                    self.show_histogram_button.grid(row = 7 + i, column = 3 , padx = 5)
            else:
                self.back_button.grid(row = 5, column= 1, sticky= "WE" , pady = 5)
                self.update_button.grid(row = 4, column= 1, sticky= "WE" , pady = 5)
                self.delete_button.grid(row = 6, column= 1, sticky= "WE" , pady = 5)
                self.show_chart_button.grid(row = 7, column = 1 , padx = 5)
                self.show_pie_button.grid(row = 7, column= 2 , padx = 5)
                self.show_histogram_button.grid(row = 7, column = 3 , padx = 5)


            
        finally:
            conn.close()
    
    def show_chart(self):

        if len(self.measurements) == 0:
            return

        chart_window = tk.Toplevel(self)
        chart_window.title("Line Chart")

        figure = Figure(figsize=(8, 4))
        chart = figure.add_subplot(1, 1, 1)
        canvas = FigureCanvasTkAgg(figure, master=chart_window)


        # Create the line chart
        chart.clear()
        x_values = range(1, len(self.measurements) + 1)
        ground_moisture_values = [measurement[1] for measurement in self.measurements]
        pH_ground_values = [measurement[2] for measurement in self.measurements]
        light_values = [measurement[3] for measurement in self.measurements]
        temperature_values = [measurement[4] for measurement in self.measurements]

        chart.plot(x_values, ground_moisture_values, label='Mokrost tla')
        chart.plot(x_values, pH_ground_values, label='pH tla')
        chart.plot(x_values, light_values, label='Sunčevi sati')
        chart.plot(x_values, temperature_values, label='Temperatura')

        chart.set_xlabel('Mjerenja')
        chart.set_ylabel('Vrijednost')
        chart.set_title('Sensor Mjerenja')

        chart.legend()
        figure.tight_layout()

        # Update the canvas
        canvas.draw()

        # Add the canvas to the new window
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

        # Show the new window
        chart_window.mainloop()
    
    def show_pie_chart(self):

        if len(self.measurements) == 0:
            return

        chart_window = tk.Toplevel(self)
        chart_window.title("Pie Chart")

        figure = Figure(figsize=(8, 4))
        chart = figure.add_subplot(1, 1, 1)
        canvas = FigureCanvasTkAgg(figure, master=chart_window)

        # Calculate the total values for each category
        ground_moisture_total = sum(max(0, measurement[1]) for measurement in self.measurements)
        pH_ground_total = sum(max(0, measurement[2]) for measurement in self.measurements)
        light_total = sum(max(0, measurement[3]) for measurement in self.measurements)
        temperature_total = sum(max(0, measurement[4]) for measurement in self.measurements)

        # Create a list of labels and values for the pie chart
        labels = ['Mokrost tla', 'pH tla', 'Sunčevi sati', 'Temperatura']
        values = [ground_moisture_total, pH_ground_total, light_total, temperature_total]

        # Create the pie chart
        chart.pie(values, labels=labels, autopct='%1.1f%%')
        chart.set_title('Sensor Mjerenja')


        # Update the canvas
        canvas.draw()

        # Add the canvas to the new window
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

        # Show the new window
        chart_window.mainloop()

    def show_histogram_chart(self):

        if len(self.measurements) == 0:
            return

        chart_window = tk.Toplevel(self)
        chart_window.title("Histogram")

        figure = Figure(figsize=(8, 4))
        chart = figure.add_subplot(1, 1, 1)
        canvas = FigureCanvasTkAgg(figure, master=chart_window)

        # Calculate the total values for each category
        ground_moisture_values = [measurement[1] for measurement in self.measurements]
        pH_ground_values = [measurement[2] for measurement in self.measurements]
        light_values = [measurement[3] for measurement in self.measurements]
        temperature_values = [measurement[4] for measurement in self.measurements]

        # Create the histogram bins
        bins = 10  

        # Plot the histograms
        chart.hist(ground_moisture_values, bins=bins, alpha=0.5, label='Mokrost tla', color='blue')
        chart.hist(pH_ground_values, bins=bins, alpha=0.5, label='pH tla', color='green')
        chart.hist(light_values, bins=bins, alpha=0.5, label='Sunčevi sati', color='orange')
        chart.hist(temperature_values, bins=bins, alpha=0.5, label='Temperatura', color='red')
        
        #Set labels and title
        chart.set_xlabel('Vrijednost')
        chart.set_ylabel('Broj mjerenja')
        chart.set_title('Sensor Mjerenja')

        chart.legend()

        # Update the canvas
        canvas.draw()

        # Add the canvas to the new window
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

        # Show the new window
        chart_window.mainloop()
     
     
    
    def update_pot(self):
        self.controller.pot_id = self.pot_id
        self.controller.switch_to_pot_form()
    

    def delete_pot(self):
        confirmed = messagebox.askyesno("PAŽNJA!", "Da li stvarno želite izbrisati ovu posudu?")


        if confirmed:
            self.controller.pot_id = self.pot_id
            self.controller.delete_the_pot()
        
       
        

        
