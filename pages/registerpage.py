from tkinter import Frame,Label,Entry,Button

class RegisterPage(Frame):
    def __init__(self,root,controller_class):
        super().__init__(root)
        self.root_window = root
        self.controller_class = controller_class

        

        self.register_label = Label(self,text = "Regristracija", font = ('Arial',15), bg = "#c8d6e5")
        self.register_label.grid(row=0,column=0,sticky="N" , pady = 10)

        self.name_label = Label(self,text = "Ime", font = ('Arial'), bg = "#c8d6e5")
        self.name_label.grid(row=1,column=0,sticky="N")

        self.name_input = Entry(self, width= 25 , font = ('Arial'), bg = "#ffffff", relief="flat")
        self.name_input.grid(row=2,column=0, sticky="N" ,pady= 5)

        self.surname_label = Label(self,text = "Prezime", font = ('Arial'), bg = "#c8d6e5")
        self.surname_label.grid(row=3,column=0,sticky="N")

        self.surname_input = Entry(self,width= 25, font = ('Arial'),  bg = "#ffffff", relief="flat")
        self.surname_input.grid(row=4,column=0, sticky="N", pady= 5)

        self.username_label = Label(self,text = "Korisničko ime", font = ('Arial'), bg = "#c8d6e5")
        self.username_label.grid(row=5,column=0,sticky="N")
        
        self.username_input = Entry(self,width= 25,font = ('Arial'),  bg = "#ffffff", relief="flat")
        self.username_input.grid(row=6,column=0, sticky="N", pady= 5)

        self.password_label = Label(self,text = "Lozinka", font = ('Arial'), bg = "#c8d6e5")
        self.password_label.grid(row=7,column=0,sticky="N")

        self.password_input = Entry(self,show = "*",width= 25,font = ('Arial'), bg = "#ffffff", relief="flat")
        self.password_input.grid(row=8,column=0, sticky="N", pady= 5)

        self.register_button = Button(self,text = "Registriraj se",width=25, font = ('Arial'),  bg = "#ffffff",command=self.register, relief= "solid",  borderwidth= 1)
        self.register_button.grid(row=9,column=0, sticky="N", pady = 5)

        self.back_to_login_button = Button(self,text = "Natrag na prijavu",width=25, font = ('Arial'),  bg = "#ffffff",command= self.controller_class.switch_to_login_page, relief= "solid" ,  borderwidth= 1 )
        self.back_to_login_button.grid(row=10,column=0, sticky="N", pady=5)
     
        

    def show_page(self, plant_id = 0, pot_id = 0):
        self.place(relx=0.5, rely=0.5, anchor="center")

    
    def hide_page(self):
        self.place_forget()
    
    def register(self):
        self.name = self.name_input.get()
        self.surname = self.surname_input.get()
        self.username = self.username_input.get()
        self.password = self.password_input.get()

        self.controller_class.register_user(self.name,self.surname,self.username,self.password)
        self.name_input.delete(0,'end')
        self.surname_input.delete(0,'end')
        self.username_input.delete(0,'end')
        self.password_input.delete(0,'end')
