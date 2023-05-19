from tkinter import Frame,Label,Button

class PlantViewHeader(Frame):
    def __init__(self,master,controller):
        super().__init__(master)
        self.master = master
        self.controller = controller

        self.header_label = Label(self, bg="lightgray",height= 2)
        self.middle_label = Label(self, text="Plants",font = ('Arial',15),bg= "lightgray")
        self.right_button = Button(self, text="Posude", font = ('Arial',10))

        self.pack_widgets()

    def pack_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(2, weight=1)

        self.header_label.grid(row=0, column=0, columnspan=3, sticky="nsew")
        self.middle_label.grid(row=0, column=1)
        self.right_button.grid(row=0, column=2, sticky="e" , padx=10)


    

    def show(self):
        self.grid(sticky="nsew")
        
    
    def hide(self):
        self.grid_remove()