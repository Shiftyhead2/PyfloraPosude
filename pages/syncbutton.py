from tkinter import Frame,Button

class SyncButton(Frame):
    def __init__(self,root,controller_class):
        super().__init__(root)

        self.root_window = root
        self.controller_class = controller_class

        self.sync_button = Button(self,text = "Sync", font = ('Arial',15), bg = "#ffffff",command= self.controller_class.sync_sensor, relief= "solid", width= 10,  borderwidth= 1)
        self.sync_button.grid(row=0,column=0,sticky= "N")

    
        
    def show_page(self,plant_id = 0, pot_id = 0):

        self.place(relx=0.1, rely=0.1,anchor="center")

    def hide_page(self):
        self.place_forget()