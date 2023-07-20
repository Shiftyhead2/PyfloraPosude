from tkinter import Frame,Label,Button

class PotViewHeader(Frame):
    def __init__(self,root,controller_class):
        super().__init__(root)
        self.root_window = root
        self.controller_class = controller_class

       

        self.header_label = Label(self, bg="#8395a7",height= 2)
        self.middle_label = Label(self, text="Evidencija posuda",font = ('Arial',15),bg= "#8395a7")
        self.right_button = Button(self, text="Biljke", font = ('Arial',15),  bg = "#ffffff", command= self.controller_class.switch_to_plants_page, relief="solid",  borderwidth= 1)
        self.logout_button = Button(self, text = "Logout", font = ('Arial',15),  bg = "#ffffff", command = self.controller_class.switch_to_login_page, relief="solid",  borderwidth= 1)

        self.configure_grid()

    def configure_grid(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.header_label.grid(row=0, column=0, columnspan=5, sticky="NSEW")
        self.middle_label.grid(row=0, column=1, sticky= "E")
        self.right_button.grid(row=0, column=2, sticky="E" , padx=10)
        self.logout_button.grid(row = 0, column= 3 , sticky= "E" , padx=10)


    

    def show_page(self,plant_id = 0, pot_id = 0):
        self.grid(sticky="nsew")
        
    
    def hide_page(self):
        self.grid_remove()