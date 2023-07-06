from tkinter import Frame,Button

class SyncButton(Frame):
    def __init__(self,master,controller):
        super().__init__(master)

        self.master = master
        self.controller = controller

        self.sync_button = Button(self,text = "Sync", font = (25),command= self.controller.sync_sensor)
        self.sync_button.grid(row=0,column=0,sticky= "N")

    
        
    def show(self,plant_id = None, pot_id = None):
        self.master.update_idletasks()  # Ensure the window size is updated

        self.place(relx=0.8, rely=0.2,anchor="center")

    def hide(self):
        self.place_forget()