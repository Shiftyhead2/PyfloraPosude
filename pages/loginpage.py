from tkinter import Frame,Label,Entry,Button


class LoginPage(Frame):
    def __init__(self,root,controller_class):
        super().__init__(root) 
        self.root_window = root 
        self.controller_class = controller_class 

        

        self.login_header = Label(self,text = "Prijava", font = ('Arial', 15), bg = "#c8d6e5")
        self.login_header.grid(row=0,column=1,sticky="N",pady = 10)

        self.username_label = Label(self,text = "Korisničko ime",font = ('Arial'), bg = "#c8d6e5")
        self.username_label.grid(row=1,column=1,sticky="N")

        self.username_input = Entry(self, width= 25, font = ('Arial'), bg = "#ffffff" ,relief="flat")
        self.username_input.grid(row=2,column=1, sticky="N",pady= 5)

        self.password_label = Label(self,text = "Lozinka" , font = ('Arial'), bg = "#c8d6e5")
        self.password_label.grid(row=3,column=1,sticky="N")
        
        self.password_input = Entry(self,show = "*", width = 25 , font = ('Arial'), bg = "#ffffff", relief="flat")
        self.password_input.grid(row=4,column=1, sticky="N",pady= 5)

        self.login_button = Button(self,text = "Prijavite se", command=self.login, relief= "solid", bg = "#ffffff", font = ('Arial'), width=25,  borderwidth= 1)
        self.login_button.grid(row=5,column=1, sticky="N", pady = 10)

        self.register_button = Button(self,text = "Regristracija",command=self.controller_class.switch_to_register_page, relief= "solid", bg = "#ffffff", font = ('Arial'), width=25,  borderwidth= 1)
        self.register_button.grid(row=6,column=1, sticky="N", pady = 5)

        

    def show_page(self,plant_id = 0, pot_id = 0):
        self.place(relx=0.5, rely=0.5, anchor="center")


    def hide_page(self):
        self.place_forget()
    
    
    def login(self):
        self.current_username = self.username_input.get()
        self.current_password = self.password_input.get()

        self.controller_class.login_user(self.current_username,self.current_password)
        self.username_input.delete(0,'end')
        self.password_input.delete(0,'end')

        

        