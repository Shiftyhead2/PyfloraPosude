from tkinter import Frame,Label

class ApplicationHeader(Frame):
    def __init__(self,master,controller):
        super().__init__(master)
        self.master = master
        self.controller = controller

       

        self.header_label = Label(self, bg="#8395a7",height= 2 , relief= "flat")
        self.middle_label = Label(self, text="PyFlora Applikacija",font = ('Arial',15),bg= "#8395a7")

        self.configure_grid()

    def configure_grid(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.header_label.grid(row=0, column=0, columnspan=3, sticky="NSEW")
        self.middle_label.grid(row=0, column=1)


    

    def show_page(self,plant_id = 0, pot_id = 0):
        self.grid(sticky="nsew")
        
    
    def hide_page(self):
        self.grid_remove()