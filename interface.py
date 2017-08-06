from tkinter import *
from tkinter.ttk import *

class ProcessManagement:
    def __init__(self, master):
        self.style = Style()
        self.style.theme_use('alt')
        self.master = master
        self.master.title("Process Management")

        self.tframe = Frame(master)
        self.tframe.pack(side=TOP, fill=BOTH, expand=True)

        self.lframe = Frame(master)
        self.lframe.pack(side=LEFT, fill=BOTH, expand=True)

        self.rframe = Frame(master)
        self.rframe.pack(side=RIGHT)

        # Console SOSim
        self.time = Label(master, text="Tempo: 0")
        self.time.pack(in_=self.tframe)

        # Table
        self.table = Treeview(master, columns=['PID', 'Priority', 'State'])
        self.table.heading('#0', text='PID')
        self.table.heading('#1', text='Priority')
        self.table.heading('#2', text='State')
        self.table.heading('#3', text='Frames')
        self.table.column('#0', stretch=YES)
        self.table.column('#1', stretch=YES)
        self.table.column('#2', stretch=YES)
        self.table.column('#3', stretch=YES)
        self.table.pack(in_=self.lframe, fill=BOTH, expand=True)

        # Lateral Buttons
        self.create_button = Button(master, text="Create", command=self.create_window)
        self.create_button.pack(in_=self.rframe, side=TOP)

        self.delete_button = Button(master, text="Delete", command=self.delete_process)
        self.delete_button.pack(in_=self.rframe, side=TOP)

        self.suspend_button = Button(master, text="Suspend", command=self.suspend_process)
        self.suspend_button.pack(in_=self.rframe, side=TOP)

        self.resume_button = Button(master, text="Resume", command=self.resume_process)
        self.resume_button.pack(in_=self.rframe, side=TOP)

        self.config_button = Button(master, text="Configure", command=self.configure)
        self.config_button.pack(in_=self.rframe, side=TOP)

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack(in_=self.rframe, side=TOP)

    # Control routines
    def create_window(self):
        window = AddWindow(self.master)

    def create_process(self):
        pass

    def delete_process(self):
        pass

    def suspend_process(self):
        pass
    
    def resume_process(self):
        pass

    def configure(self):
        pass

    # Update Routines
    def updateConsole(self):
        pass

    def updateAll(self):
        self.master.after(1000, self.update)

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
        self.choices = ['CPU BOUND', 'IO BOUND', 'CPU&IO BOUND']
        self.type = StringVar(master)
        self.type_label = Label(self, text="Type of Proccess")
        self.type_option = OptionMenu(self, self.type, self.choices[0], *self.choices)

        self.type_label.pack()
        self.type_option.pack()
        self.type_label.grid(row=2, column=0, sticky=W)
        self.type_option.grid(row=2, column=1, sticky=W)

        # Buttons
        self.ok_button = Button(self, text="Ok", command=self.applyWindow)
        self.ok_button.pack()
        self.ok_button.grid(row=3, column=1, sticky=E)

        self.close_button = Button(self, text="Close", command=self.destroy)
        self.close_button.pack()
        self.close_button.grid(row=3, column=2, sticky=E)
        
        for child in self.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    def applyWindow(self):
        self.destroy()

    def on_destroy(self, event):
        if event.widget == self:
            self.master.deiconify()

root = Tk()
my_gui = ProcessManagement(root)
root.mainloop()
