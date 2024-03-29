from tkinter import Frame,Label,Entry,Button

class LoginPage(Frame):
    # Initialization function for classes. Many classes follow the same rules of creation
    def __init__(self,master,controller):
        super().__init__(master) # Intializes the base parent class from which this class inherits the functions from
        self.master = master # refers to the root window from the app.py file
        self.controller = controller # refers to the AppController class from the app.py file

        

        self.login_label = Label(self,text = "Prijava", font = (45))
        self.username_label = Label(self,text = "Korisničko ime:",font = (20))
        self.username_entry = Entry(self, width= 22, font = (15))
        self.password_label = Label(self,text = "Lozinka:" , font = (20))
        self.password_entry = Entry(self,show = "*", width = 22 , font = (15))
        self.login_button = Button(self,text = "Prijavite se",width=25, font = (20) , command=self.login)
        self.register_button = Button(self,text = "Regristracija",width=25, font = (20) ,command=self.controller.switch_to_register)

        self.login_label.grid(row=0,column=1,sticky="N",pady = 10)
        self.username_label.grid(row=1,column=0,sticky="E")
        self.username_entry.grid(row=1,column=1,pady= 5)
        self.password_label.grid(row=2,column=0,sticky="E")
        self.password_entry.grid(row=2,column=1,pady= 5)
        self.login_button.grid(row=3,column=1,pady = 10)
        self.register_button.grid(row=4,column=1,pady = 5)

    # Used for showing the pages. The parameters like plant_id and pot_id are optional because not all pages require them to work
    def show(self,plant_id = None, pot_id = None):
        self.master.update_idletasks()  # Ensure the window size is updated

        self.place(relx=0.5, rely=0.5, anchor="center") # Uses the tkinter place method to place the page on the relative x and y values of the window. This places the window on the center
                                                        # of the screen


    # Used for hiding the view when the page switching occurs
    def hide(self):
        self.place_forget()
    
    
    def login(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()

        self.controller.login_user(self.username,self.password)
        self.username_entry.delete(0,'end')
        self.password_entry.delete(0,'end')

        

        