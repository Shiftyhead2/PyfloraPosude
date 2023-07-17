from tkinter import Frame,Label,Button

class PlantViewHeader(Frame):
    def __init__(self,master,controller):
        super().__init__(master)
        self.master = master
        self.controller = controller

       

        self.header_label = Label(self, bg="lightgray",height= 2)
        self.middle_label = Label(self, text="Evidencija biljka",font = ('Arial',20),bg= "lightgray")
        self.right_button = Button(self, text="Posude", font = ('Arial',15), command= self.controller.switch_to_pot_view)
        self.logout_button = Button(self, text = "Logout", font = ('Arial',15),command = self.controller.switch_to_login)

        self.pack_widgets()

    def pack_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.header_label.grid(row=0, column=0, columnspan=5, sticky="NSEW")
        self.middle_label.grid(row=0, column=1)
        self.right_button.grid(row=0, column=2, sticky="E" , padx=10)
        self.logout_button.grid(row = 0, column= 3 , sticky= "E" , padx=10)


    

    def show(self,plant_id = None, pot_id = None):
        self.grid(sticky="nsew")
        
    
    def hide(self):
        self.grid_remove()