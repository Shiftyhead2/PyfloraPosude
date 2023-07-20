import tkinter as tk
from tkinter import Frame,Label,Button, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import sqlite3

class PotViewPage(Frame):
    def __init__(self,root,controller_class,current_pot_id = 0):
        super().__init__(root)
        self.root_window = root
        self.controller_class = controller_class
        self.current_pot_id = current_pot_id
        self.current_pot = None
        self.current_measurements = None


        self.pot_label = Label(self, font = ('Arial',15) , bg = "#c8d6e5")
        self.pot_label.grid(row = 0, column=1, sticky= "W", pady= 10)

        self.pot_location_label = Label(self, font = ('Arial') , bg = "#c8d6e5")
        self.pot_location_label.grid(row = 1, column= 1,sticky= "W")


        self.plant_status_label = Label(self, font = ('Arial') , bg = "#c8d6e5")
        self.plant_status_label.grid(row = 3 , column= 1, sticky= "W", pady= 10)

        self.measurements_frame = Frame(self , bg = "#c8d6e5")
        self.measurements_frame.grid(row=4, column=1, sticky="W", pady=10)
        self.measurements_labels = []


        self.back_button = Button(self,text= "Natrag", font = ('Arial'),  bg = "#ffffff", command= self.controller_class.switch_to_pots_page, relief= "solid",  borderwidth= 1)
        

        self.update_button = Button(self,text= "Ažuriraj", font = ('Arial'), bg = "#ffffff", command= self.update_pot, relief= "solid",  borderwidth= 1)
        

        self.delete_button = Button(self,text= "Izbriši posudu", font = ('Arial') , bg = "#ffffff", command= self.delete_pot, relief= "solid",  borderwidth= 1)


        self.show_line_chart_button = Button(self, text="Prikaži graf", font = ('Arial'), bg = "#ffffff", command=self.show_line_chart, relief= "solid",  borderwidth= 1)
        self.show_line_chart_button.grid(row=6, column=1, sticky="WE")

        self.show_pie_button = Button(self, text="Prikaži pie chart", bg = "#ffffff", command=self.show_pie_chart, font = ('Arial') ,relief= "solid",  borderwidth= 1)
        self.show_pie_button.grid(row=5, column=2, sticky="WE")

        self.show_histogram_button = Button(self, text="Prikaži histogram", bg = "#ffffff", command=self.show_histogram_chart, font = ('Arial'), relief= "solid",  borderwidth= 1)
        self.show_histogram_button.grid(row=7, column=3, sticky="WE")

       
        
        
    def get_plant_status_text(self):
        status = self.current_pot[4]
        return f"{status}"

    
    def update_labels(self):
        self.pot_location_label.config(text=f"Lokacija: {self.current_pot[1]}")
        self.pot_label.config(text=f"Posuda #{self.current_pot[0]}")
        self.plant_status_label.config(text=f"Posuđena biljka: {self.current_pot[2]}\n\n{self.get_plant_status_text()}")


    def show_page(self,plant_id = 0, pot_id = 0):

        self.place(relx=0.3, rely=0.5,anchor="w")

        self.current_pot_id = pot_id

       

        self.get_plant()

        self.show_measurements()

        self.update_labels()

        

    def hide_page(self):
        self.place_forget()
    
    def get_plant(self):
        try:
            with sqlite3.connect(self.controller_class.pot_database_location) as conn_pots:
                cursor_pots = conn_pots.cursor()
                cursor_pots.execute("SELECT id, location, plant_name, plant_id, status FROM pots WHERE id=?", (self.current_pot_id,))
                self.current_pot = cursor_pots.fetchone()
        except sqlite3.Error as e:
            messagebox.showerror(f"Greška!", f"Nešto je otišlo po zlu: {e}")
        
    
    def show_measurements(self):
        # Clear the existing measurement labels
        for label in self.measurements_labels:
            label.destroy()
        self.measurements_labels = []
        try:
            with sqlite3.connect(self.controller_class.sensor_database_location) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM sensors")
                self.current_measurements = cursor.fetchall()
                # Create labels to display the measurements
                if len(self.current_measurements) > 0:
                    for i, measurement in enumerate(self.current_measurements):
                        sensor_id, ground_moisture, self.pH_ground, light_hours, temperature = measurement

                        # Create and grid the labels
                        label_text = f"Sensor #{sensor_id}:  Mokrost tla= {ground_moisture}, pH = {self.pH_ground}, Sunčevih sati = {light_hours}, Temperatura = {temperature}"
                        label = Label(self.measurements_frame, text=label_text, bg="#c8d6e5")
                        label.grid(row=i, column=0, sticky="N")
                        self.measurements_labels.append(label)
                        self.back_button.grid(row=6 + i, column=1, sticky="WE", pady=5)
                        self.update_button.grid(row=5 + i, column=1, sticky="WE", pady=5)
                        self.delete_button.grid(row=7 + i, column=1, sticky="WE", pady=5)
                        self.show_line_chart_button.grid(row=8 + i, column=1, padx=5)
                        self.show_pie_button.grid(row=8 + i, column=2, padx=5)
                        self.show_histogram_button.grid(row=8 + i, column=3, padx=5)
                        status_text = self.get_plant_status_text()
                        self.plant_status_label.config(text=status_text)
                else:
                    self.back_button.grid(row=6, column=1, sticky="WE", pady=5)
                    self.update_button.grid(row=5, column=1, sticky="WE", pady=5)
                    self.delete_button.grid(row=7, column=1, sticky="WE", pady=5)
                    self.show_line_chart_button.grid(row=8, column=1, padx=5)
                    self.show_pie_button.grid(row=8, column=2, padx=5)
                    self.show_histogram_button.grid(row=8, column=3, padx=5)
            
                    # Get and display the status text
                    status_text = self.get_plant_status_text()
                    self.plant_status_label.config(text=status_text)
        except sqlite3.Error as e:
             messagebox.showerror(f"Greška!", f"Nešto je otišlo po zlu: {e}")
    
    def show_line_chart(self):

        if len(self.current_measurements) == 0:
            return

        chart_window = tk.Toplevel(self)
        chart_window.title("Line Chart")

        chart_window.configure(bg = "#ffffff")

        figure = Figure(figsize=(8, 4))
        chart = figure.add_subplot(1, 1, 1)
        canvas = FigureCanvasTkAgg(figure, master=chart_window)


        # Create the line chart
        chart.clear()
        x_values = range(1, len(self.current_measurements) + 1)
        ground_moisture_values = [measurement[1] for measurement in self.current_measurements]
        pH_ground_values = [measurement[2] for measurement in self.current_measurements]
        light_values = [measurement[3] for measurement in self.current_measurements]
        temperature_values = [measurement[4] for measurement in self.current_measurements]

        chart.plot(x_values, ground_moisture_values, label='Mokrost tla')
        chart.plot(x_values, pH_ground_values, label='pH tla')
        chart.plot(x_values, light_values, label='Sunčevi sati')
        chart.plot(x_values, temperature_values, label='Temperatura')

        chart.set_xlabel('Mjerenja')
        chart.set_ylabel('Vrijednost')
        chart.set_title('Mjerenja sa sensora')

        chart.legend()
        figure.tight_layout()

        # Update the canvas
        canvas.draw()

        # Add the canvas to the new window
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

        # Show the new window
        chart_window.mainloop()
    
    def show_pie_chart(self):

        if len(self.current_measurements) == 0:
            return

        chart_window = tk.Toplevel(self)
        chart_window.title("Pie Chart")

        chart_window.configure(bg = "#ffffff")

        figure = Figure(figsize=(8, 4))
        chart = figure.add_subplot(1, 1, 1)
        canvas = FigureCanvasTkAgg(figure, master=chart_window)

        # Calculate the total values for each category
        ground_moisture_total = sum(max(0, measurement[1]) for measurement in self.current_measurements)
        pH_ground_total = sum(max(0, measurement[2]) for measurement in self.current_measurements)
        light_total = sum(max(0, measurement[3]) for measurement in self.current_measurements)
        temperature_total = sum(max(0, measurement[4]) for measurement in self.current_measurements)

        # Create a list of labels and values for the pie chart
        labels = ['Mokrost tla', 'pH tla', 'Sunčevi sati', 'Temperatura']
        values = [ground_moisture_total, pH_ground_total, light_total, temperature_total]

        # Create the pie chart
        chart.pie(values, labels=labels, autopct='%1.1f%%')
        chart.set_title('Mjerenja sa sensora')


        # Update the canvas
        canvas.draw()

        # Add the canvas to the new window
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

        # Show the new window
        chart_window.mainloop()

    def show_histogram_chart(self):

        if len(self.current_measurements) == 0:
            return

        chart_window = tk.Toplevel(self)
        chart_window.title("Histogram")

        chart_window.configure(bg = "#ffffff")


        figure = Figure(figsize=(8, 4))
        chart = figure.add_subplot(1, 1, 1)
        canvas = FigureCanvasTkAgg(figure, master=chart_window)

        # Calculate the total values for each category
        ground_moisture_values = [measurement[1] for measurement in self.current_measurements]
        pH_ground_values = [measurement[2] for measurement in self.current_measurements]
        light_values = [measurement[3] for measurement in self.current_measurements]
        temperature_values = [measurement[4] for measurement in self.current_measurements]

        # Create the histogram bins
        bins = 10  

        # Plot the histograms
        chart.hist(ground_moisture_values, bins=bins, alpha=0.5, label='Mokrost tla', color='green')
        chart.hist(pH_ground_values, bins=bins, alpha=0.5, label='pH tla', color='yellow')
        chart.hist(light_values, bins=bins, alpha=0.5, label='Sunčevi sati', color='orange')
        chart.hist(temperature_values, bins=bins, alpha=0.5, label='Temperatura', color='red')
        
        #Set labels and title
        chart.set_xlabel('Vrijednost')
        chart.set_ylabel('Broj mjerenja')
        chart.set_title('Mjerenja sa sensora')

        chart.legend()

        # Update the canvas
        canvas.draw()

        # Add the canvas to the new window
        canvas.get_tk_widget().grid(row=0, column=0, padx=10, pady=10)

        # Show the new window
        chart_window.mainloop()
     
     
    
    def update_pot(self):
        self.controller_class.pot_id = self.current_pot_id
        self.controller_class.switch_to_pots_form()
    

    def delete_pot(self):
        confirmed = messagebox.askyesno("PAŽNJA!", "Da li stvarno želite izbrisati ovu posudu?")


        if confirmed:
            self.controller_class.pot_id = self.current_pot_id
            self.controller_class.delete_the_pot()