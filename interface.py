from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
import process as p

class ProcessManagement:
    def __init__(self, master, manager):
        self.manager = manager
        
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
        self.time = StringVar()
        self.time_label = Label(master, textvariable= self.time)
        self.time_label.pack(in_=self.tframe)

        # Table
        self.table = Treeview(master, columns=['PID', 
            'Priority', 
            'Quantum',
            'Tickets',
            'State', 
            'Type'])
        self.table.heading('#0', text='PID')
        self.table.heading('#1', text='Priority')
        self.table.heading('#2', text='Quantum')
        self.table.heading('#3', text='Tickets')
        self.table.heading('#4', text='State')
        self.table.heading('#5', text='Type')
        self.table.heading('#6', text='Frames')
        self.table.column('#0', stretch=YES, width=50)
        self.table.column('#1', stretch=YES, width=100)
        self.table.column('#2', stretch=YES, width=100)
        self.table.column('#3', stretch=YES, width=100)
        self.table.column('#4', stretch=YES, width=130)
        self.table.column('#5', stretch=YES, width=130)
        self.table.column('#6', stretch=YES, width=100)
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
        window = AddWindow(self.master, self)

    def clear_table(self):
        self.table.delete(*self.table.get_children())

    def select_item(self):
        cur_item = self.table.focus()
        return self.table.item(cur_item)

    def add_to_table(self, control):
        if control.process.state == p.READY:
            state = 'READY'
        if control.process.state == p.EXECUTING:
            state = 'EXECUTING'
        if control.process.state == p.BLOCKED:
            state = 'BLOCKED'

        self.table.insert("", control.PID, text=str(control.PID), 
                values=(
                    control.priority,
                    control.quantum,
                    control.tickets,
                    state,
                    control.process.type,
                    5)) 

    def add_to_table_s(self, control):

        self.table.insert("", control.PID, text=str(control.PID), 
                values=(
                    control.priority,
                    'SUSPENDED',
                    control.process.type,
                    5)) 

    def create_process(self, priority, quantum, type, tickets):
        self.manager.add_process(type, priority, quantum, tickets)

    def delete_process(self):
        p = self.select_item()
        if p['text']:
            self.manager.remove_process(int(p['text']))

    def suspend_process(self):
        p = self.select_item()
        if p['text']:
            res = self.manager.suspend_process(int(p['text']))
            if res:
                return
        messagebox.showinfo("Alert", "Not possible SUSPEND that process.")
    
    def resume_process(self):
        p = self.select_item()
        if p['text']:
            res = self.manager.resume_process(int(p['text']))
            if res:
                return
        messagebox.showinfo("Alert", "Not possible RESUME that process.")

    def configure(self):
        window = ConfigWindow(self.master, self)

    # Update Routines
    def update_console(self):
        self.time.set('Tempo: ' + str(self.manager.time))

    def update_table(self):
        p = self.select_item()

        self.clear_table()
        ps = self.manager.get_processes()
        ss = self.manager.sbuffer

        for cb in ps:
            self.add_to_table(cb)

        for cb in ss:
            self.add_to_table_s(cb)

        if p['text']:
            for child in self.table.get_children():
                item = self.table.item(child)
                if item['text'] == p['text']:
                    self.table.focus_set()
                    self.table.selection_set((child,child))
                    self.table.focus(child)

    def update_all(self):
        self.manager.update()
        self.update_console()
        self.update_table()
        self.master.after(1000, self.update_all)

class AddWindow(Toplevel):
    def __init__(self, master, window):
        Toplevel.__init__(self, master)
        self.title("Create Process")

        self.master = master
        self.master.withdraw()
        self.bind("<Destroy>", self.on_destroy)

        self.window = window

        # Number of Processes
        self.number_label = Label(self, text="Number of Processes")
        self.number_spin = Spinbox(self, from_=1, to_=10)

        self.number_label.pack()
        self.number_spin.pack()
        self.number_label.grid(row=0, column=0, sticky=W)
        self.number_spin.grid(row=0, column=1, sticky=W)

        # Priority
        self.priority_label = Label(self, text="Priority")
        self.priority_spin = Spinbox(self, from_=1, to_=10)

        self.priority_label.pack()
        self.priority_spin.pack()
        self.priority_label.grid(row=1, column=0, sticky=W)
        self.priority_spin.grid(row=1, column=1, sticky=W)

        # Quantum
        self.quantum_label = Label(self, text="Quantum")
        self.quantum_spin = Spinbox(self, from_=1, to_=10)

        self.quantum_label.pack()
        self.quantum_spin.pack()
        self.quantum_label.grid(row=2, column=0, sticky=W)
        self.quantum_spin.grid(row=2, column=1, sticky=W)

        # Tickets
        self.tickets_label = Label(self, text="Tickets")
        self.tickets_spin = Spinbox(self, from_=10, to_=100)

        self.tickets_label.pack()
        self.tickets_spin.pack()
        self.tickets_label.grid(row=3, column=0, sticky=W)
        self.tickets_spin.grid(row=3, column=1, sticky=W)

        # Type of Process
        self.choices = ['CPU BOUND', 'IO BOUND', 'CPU&IO BOUND']
        self.type = StringVar(master)
        self.type_label = Label(self, text="Type of Proccess")
        self.type_option = OptionMenu(self, self.type, self.choices[0], *self.choices)

        self.type_label.pack()
        self.type_option.pack()
        self.type_label.grid(row=4, column=0, sticky=W)
        self.type_option.grid(row=4, column=1, sticky=W)

        # Buttons
        self.ok_button = Button(self, text="Ok", command=self.applyWindow)
        self.ok_button.pack()
        self.ok_button.grid(row=5, column=1, sticky=E)

        self.close_button = Button(self, text="Close", command=self.destroy)
        self.close_button.pack()
        self.close_button.grid(row=5, column=2, sticky=E)
        
        for child in self.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    def applyWindow(self):
        n_processes     = int(self.number_spin.get())
        priority        = int(self.priority_spin.get())
        quantum         = int(self.quantum_spin.get())
        tickets         = int(self.tickets_spin.get())

        for i in range(n_processes):
            self.window.create_process(priority,
                    quantum,
                    self.type.get(),
                    tickets)

        self.destroy()

    def on_destroy(self, event):
        if event.widget == self:
            self.master.deiconify()

class ConfigWindow(Toplevel):
    def __init__(self, master, window):
        Toplevel.__init__(self, master)
        self.title("Configuration")

        self.master = master
        self.master.withdraw()
        self.bind("<Destroy>", self.on_destroy)

        self.window = window

        # Type of Process
        self.choices = [
                'ROUND ROBIN', 
                'ROUND ROBIN (PRIORITY)', 
                'PRIORITY',
                'DYNAMIC PRIORITY',
                'LOTTERY']
        self.sched = StringVar(master)
        self.sched.set(self.window.manager.scheduling_type)
        self.sched_label = Label(self, text="Type of Scheduling")
        self.sched_option = OptionMenu(self, self.sched, 
                self.window.manager.scheduling_type, *self.choices)

        self.sched_label.pack()
        self.sched_option.pack()
        self.sched_label.grid(row=0, column=0, sticky=W)
        self.sched_option.grid(row=0, column=1, sticky=W)

        # Buttons
        self.ok_button = Button(self, text="Ok", command=self.applyWindow)
        self.ok_button.pack()
        self.ok_button.grid(row=1, column=1, sticky=E)

        self.close_button = Button(self, text="Close", command=self.destroy)
        self.close_button.pack()
        self.close_button.grid(row=1, column=2, sticky=E)
        
        for child in self.winfo_children(): 
            child.grid_configure(padx=5, pady=5)

    def applyWindow(self):
        self.window.manager.change_scheduling(self.sched.get())
        self.destroy()

    def on_destroy(self, event):
        if event.widget == self:
            self.master.deiconify()

m = p.ProcessManager(15, 'ROUND ROBIN')
root = Tk()
my_gui = ProcessManagement(root, m)
my_gui.update_all()
root.mainloop()
