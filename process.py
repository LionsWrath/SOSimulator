from random import randint, random

BLOCKED     = 2
EXECUTING   = 1
READY       = 0

class Process:
    def __init__(self, type):
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

    # Maybe modify this later
    def begin(self):
        if self.state == READY:
            self.state = EXECUTING
            return True

        if self.state == EXECUTING:
            return True

        return False

    #Can only preempt if is already executing
    #Will give an error state otherwise
    def preempt(self):
        self.state = READY

    def update(self):
        
        if self.state == EXECUTING:
            # Presents a chance to change to I/O
            if self.draw():
                self.state == BLOCKED
            else:
                # Continue processing
                self.pwait += 1

                if self.pwait == self.ptime:
                    self.pwait = 0
                    self.state = READY

        if self.state == BLOCKED:
            self.iwait += 1

            if self.iwait == self.itime:
                self.iwait = 0
                self.state = READY

class ControlBlock:

    def __init__(self, process, PID, priority, quantum):
        self.process            = process
        self.PID                = PID
        self.quantum            = quantum
        self.priority           = priority

        self.default_priority   = priority
        self.default_quantum    = quantum

    def decrease_priority(self):
        self.priority -= 1 

    def decrease_quantum(self):
        self.quantum -= 1

    def init(self):
        self.process.begin()

    def reset(self):
        self.priority = self.default_priority
        self.quantum = self.default_quantum
    
    def get_status(self):
        return self.process.get_status()

    def update(self):
        self.process.update()

class ProcessManager:

    def __init__(self, psize, scheduling_type):
        self.psize = psize
        self.scheduling_type = scheduling_type

        self.pslot = False
        self.islot = False

        self.pbuffer = []
        self.ibuffer = []

    def add_process(self, type, priority, quantum):
        p = Process(self, type)
        c = ControlBlock(p, priority, quantum)

        self.pbuffer.append(c)

# Data Structure functions (CHANGE THIS)
    def pop_first_process(self):
        if self.pbuffer:
            next = self.pbuffer[0]
            self.pbuffer.pop(0)
            
            return next
        return False


#---------------------------------------------------------------------------------------------------
# They have to analyze if the pslot will change at all, so they can return the same pslot

    def round_robin(self):
        if self.pslot:
            self.pslot.decrease_quantum()

            if self.pslot.quantum == 0:             # Check if the quantum ended
                return self.pop_first_process()

        elif self.pbuffer:

        return self.pslot

    def round_robin_priority(self):
        pass

    def priority(self):
        pass

    def dynamic_priority(self):
        pass

    def lottery(self):
        pass

    def schedule(self):
        sched = { 
                'ROUND ROBIN'               : self.round_robin,
                'ROUND ROBIN (PRIORITY)'    : self.round_robin_priority,
                'PRIORITY'                  : self.priority,
                'DYNAMIC PRIORITY'          : self.dynamic_priority,
                'LOTTERY'                   : self.lottery
                }[self.scheduling_type]

        self.pslot = sched()
        self.pslot.init()

#---------------------------------------------------------------------------------------------------

    def resolve_executing(self):
        s = self.pslot.get_status() 
        
        if s == BLOCKED:
            self.pslot.reset()
            self.ibuffer.append(self.pslot)
            self.pslot = False

        if s == READY:
            self.pslot.reset()
            self.pbuffer.append(self.pslot)
            self.pslot = False

    def resolve_blocked(self):
        s = self.islot.get_status()

        if s == READY:
            self.pbuffer.append(self.islot)
            self.islot = False

    def update(self):
        # Update the main processes
        if self.pslot:
            self.pslot.update()
            self.resolve_executing()

        if self.islot:
            self.islot.update()
            self.resolve_blocked()

        schedule()

