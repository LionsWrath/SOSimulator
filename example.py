from tkinter import *
from tkinter import ttk

class ProcessManagement:
    def __init__(self, master):
        self.master = master
        self.master.title("Process Management")

        self.tframe = Frame(master)
        self.tframe.pack(side=TOP, fill=BOTH, expand=True)

        self.lframe = Frame(master)
        self.lframe.pack(side=LEFT, fill=BOTH, expand=True)

        self.rframe = Frame(master)
        self.rframe.pack(side=RIGHT)

        self.label = Label(master, text="This is our first GUI!")
        self.label.pack(in_=self.tframe)

        self.table = ttk.Treeview(master, columns=['PID', 'Priority', 'State'])
        self.table.heading('#0', text='PID')
        self.table.heading('#1', text='Priority')
        self.table.heading('#2', text='State')
        self.table.heading('#3', text='Frames')
        self.table.column('#0', stretch=YES)
        self.table.column('#1', stretch=YES)
        self.table.column('#2', stretch=YES)
        self.table.column('#3', stretch=YES)
        self.table.pack(in_=self.lframe, fill=BOTH, expand=True)

        self.insert_button = Button(master, text="Insert", command=self.create_window)
        self.insert_button.pack(in_=self.rframe, side=TOP)

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack(in_=self.rframe, side=TOP)

    def create_window(self):
        window = AddWindow(self.master)

    def insert_process(self):
        pass

class AddWindow(Toplevel):
    def __init__(self, master):
        Toplevel.__init__(self, master)
        self.title("Create Process")

        self.master = master
        self.master.withdraw()
        self.bind("<Destroy>", self.on_destroy)

        # Number of Processes
        self.number_label = Label(self, text="Number of Processes")
        self.number_spin = Spinbox(self, from_=0, to_=10)

        self.number_label.pack()
        self.number_spin.pack()
        self.number_label.grid(row=0, column=0, sticky=W)
        self.number_spin.grid(row=0, column=1, sticky=W)

        # Priority
        self.priority_label = Label(self, text="Priority")
        self.priority_spin = Spinbox(self, from_=0, to_=10)

        self.priority_label.pack()
        self.priority_spin.pack()
        self.priority_label.grid(row=1, column=0, sticky=W)
        self.priority_spin.grid(row=1, column=1, sticky=W)

        # Type of Process
        self.type = StringVar()
        self.type_label = Label(self, text="Type of Proccess")
        self.type_option = OptionMenu(self, self.type, 
                'CPU-BOUND',
                'IO-BOUND')

        self.type_label.pack()
        self.type_option.pack()
        self.type_label.grid(row=2, column=0, sticky=W)
        self.type_option.grid(row=2, column=1, sticky=W)

        self.ok_button = Button(self, text="Ok", command=self.quit)
        self.ok_button.pack()

        self.close_button = Button(self, text="Close", command=self.quit)
        self.close_button.pack()

    def on_destroy(self, event):
        if event.widget == self:
            self.master.deiconify()

root = Tk()
my_gui = ProcessManagement(root)
root.mainloop()
