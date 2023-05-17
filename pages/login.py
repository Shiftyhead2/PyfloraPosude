from tkinter import *

class LoginPage(Frame):
    def __init__(self,master,controller):
        super().__init__(master)
        self.master = master
        self.controller = controller
        self.grid(sticky="NSEW") 

        self.username_label = Label(self,text = "Username:")
        self.username_entry = Entry(self)
        self.password_label = Label(self,text = "Password:")
        self.password_entry = Entry(self,show = "*")
        self.login_button = Button(self,text = "Login",width=15,command=self.login)
        self.register_button = Button(self,text = "Register",width=15,command=self.controller.switch_to_register)

        self.username_label.grid(row=0,column=0,sticky="E")
        self.username_entry.grid(row=0,column=1,columnspan=2,pady= 5)
        self.password_label.grid(row=1,column=0,sticky="E")
        self.password_entry.grid(row=1,column=1,columnspan=2,pady= 5)
        self.login_button.grid(row=2,column=1,columnspan=2,pady = 10)
        self.register_button.grid(row=3,column=1,columnspan=2,pady = 5)
    
    def show(self):
        self.grid(sticky="NSEW")
    
    def hide(self):
        self.grid_remove()
    
    def login(self):
        self.username = self.username_entry.get()
        self.password = self.password_entry.get()

        self.controller.login_user(self.username,self.password)
        self.username_entry.delete(0,'end')
        self.password_entry.delete(0,'end')

        

        