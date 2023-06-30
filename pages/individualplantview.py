from tkinter import Frame

class IndividualPlantView(Frame):
    def __init__(self,master,controller,plant = None):
        self.master = master
        self.controller = controller
        self.plant = plant
    

    def show(self,plant_id = None):
        self.master.update_idletasks()  # Ensure the window size is updated

        self.place(relx=0.5, rely=0,anchor="n")

    def hide(self):
        self.place_forget()

        
