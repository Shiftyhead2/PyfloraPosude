from tkinter import *

class RegisterPage(Frame):
    def __init__(self,master,controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.grid(sticky="nsew") 


        self.name_label = Label(self,text = "Name:")
        self.name_entry = Entry(self)
        self.surname_label = Label(self,text = "Surname:")
        self.surname_entry = Entry(self)
        self.username_label = Label(self,text = "Username:")
        self.username_entry = Entry(self)
        self.password_label = Label(self,text = "Password:")
        self.password_entry = Entry(self,show = "*")
        self.register_button = Button(self,text = "Register",width=15,command=self.register)
        self.back_to_login_button = Button(self,text = "Back to login",width=15,command= self.controller.switch_to_login)

        self.name_label.grid(row=0,column=0,sticky="e")
        self.name_entry.grid(row=0,column=1,pady= 5)
        self.surname_label.grid(row=1,column=0,sticky="e")
        self.surname_entry.grid(row=1,column=1,pady= 5)
        self.username_label.grid(row=2,column=0,sticky="e")
        self.username_entry.grid(row=2,column=1,pady= 5)
        self.password_label.grid(row=3,column=0,sticky="e")
        self.password_entry.grid(row=3,column=1,pady= 5)
        self.register_button.grid(row=4,column=0,columnspan=2,pady = 5)
        self.back_to_login_button.grid(row=5,column=0,columnspan=2,pady=5)

    def show(self):
        self.grid(sticky="nsew")
    
    def hide(self):
        self.grid_remove()
    
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
