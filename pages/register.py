from tkinter import Frame,Label,Entry,Button

class RegisterPage(Frame):
    def __init__(self,master,controller):
        super().__init__(master)
        self.master = master
        self.controller = controller

        

        self.register_label = Label(self,text = "Regristracija", font = (45))
        self.name_label = Label(self,text = "Ime:", font = (20))
        self.name_entry = Entry(self, width= 20 , font = (15))
        self.surname_label = Label(self,text = "Prezime:", font = (20))
        self.surname_entry = Entry(self,width= 20, font = (15))
        self.username_label = Label(self,text = "Korisničko ime:", font = (20))
        self.username_entry = Entry(self,width= 20,font = (15))
        self.password_label = Label(self,text = "Lozinka:", font = (20))
        self.password_entry = Entry(self,show = "*",width= 20,font = (15))
        self.register_button = Button(self,text = "Registriraj se",width=25, font = (20),command=self.register)
        self.back_to_login_button = Button(self,text = "Natrag na prijavu",width=25, font = (20),command= self.controller.switch_to_login)

        self.register_label.grid(row=0,column=1,sticky="N" , pady = 10)
        self.name_label.grid(row=1,column=0,sticky="E")
        self.name_entry.grid(row=1,column=1,pady= 5)
        self.surname_label.grid(row=2,column=0,sticky="E")
        self.surname_entry.grid(row=2,column=1,pady= 5)
        self.username_label.grid(row=3,column=0,sticky="E")
        self.username_entry.grid(row=3,column=1,pady= 5)
        self.password_label.grid(row=4,column=0,sticky="E")
        self.password_entry.grid(row=4,column=1,pady= 5)
        self.register_button.grid(row=5,column=1,pady = 5)
        self.back_to_login_button.grid(row=6,column=1,pady=5)

    def show(self, plant_id = None, pot_id = None):
        self.master.update_idletasks()  # Ensure the window size is updated
        self.place(relx=0.5, rely=0.5, anchor="center")
    
    def hide(self):
        self.place_forget()
    
    def register(self):
        self.name = self.name_entry.get()
        self.surname = self.surname_entry.get()
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()

        self.controller.register_user(self.name,self.surname,self.username,self.password)
        self.name_entry.delete(0,'end')
        self.surname_entry.delete(0,'end')
        self.username_entry.delete(0,'end')
        self.password_entry.delete(0,'end')
