from random import randint, random

BLOCKED     = 2
EXECUTING   = 1
READY       = 0

class Process:
    def __init__(self, manager, priority, type):
        self.manager = manager
        self.priority = priority
        self.type = type

        self.generate_times()

        # Variables to control processing and io
        self.state = READY
        self.pwait = 0
        self.iwait = 0

    def get_status(self):
        return self.state

    def draw(self):
        return random() < self.chance

    def generate_times(self):
        if self.type == 'CPU BOUND':
            self.ptime = randint(1, 3) * 3 
            self.itime = randint(1, 3) * 1
            self.chance = 0.3

        if self.type == 'IO BOUND':
            self.ptime = randint(1, 3) * 1
            self.itime = randint(1, 3) * 3
            self.chance = 0.7

        if self.type == 'CPU&IO BOUND':
            self.ptime = randint(1, 3) * 3
            self.itime = randint(1, 3) * 3
            self.chance = 0.5

    def update(self):
        
        if self.state == EXECUTING:
            # Presents a chance to change to I/O
            if self.draw():
                self.state == BLOCKED
            else:
                # Continue processing
                self.pwait = self.pwait + 1

                if self.pwait == self.ptime:
                    self.pwait = 0
                    self.state = READY

        if self.state == BLOCKED:
            self.iwait = self.iwait + 1

            if self.iwait == self.itime:
                self.iwait = 0
                self.state = READY

class ProcessManager:

    def __init__(self, psize, schedule):
        self.psize = psize

        self.pslot = False
        self.islot = False
        self.pbuffer = []
        self.ibuffer = []

    def resolve_executing(self):
        s = self.pslot.get_status() 
        
        if s == BLOCKED:
            self.ibuffer.append(self.pslot)
            self.pslot = False

        if s == READY:
            self.pbuffer.append(self.pslot)
            self.pslot = False

    def resolve_blocked(self):
        s = self.islot.get_status()

        if s == READY:
            self.pbuffer.append(self.islot)
            self.islot = False

    def update(self):
        # Begin updating the main processes
        if self.pslot:
            self.pslot.update()
            self.resolve_executing()

        if self.islot:
            self.islot.update()
            self.resolve_blocked()

         
