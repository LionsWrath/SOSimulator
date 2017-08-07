from random import randint, random
from gerenciadorMemoria import GerenciadorMemoriaVirtual

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

        self.mem_pos = -1

    def get_status(self):
        return self.state

    def draw(self):
        return random() < self.chance

    def generate_times(self):
        if self.type == 'CPU BOUND':
            self.ptime = randint(1, 3) * 3
            self.itime = randint(1, 3) * 1
            self.chance = 0.1

        if self.type == 'IO BOUND':
            self.ptime = randint(1, 3) * 1
            self.itime = randint(1, 3) * 3
            self.chance = 0.3

        if self.type == 'CPU&IO BOUND':
            self.ptime = randint(1, 3) * 3
            self.itime = randint(1, 3) * 3
            self.chance = 0.2

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
        print('\tSTATE: ', self.state)

        print('\tPTIME: ', self.ptime)
        print('\tITIME: ', self.itime)

        print('\tB PWAIT: ', self.pwait)
        print('\tB IWAIT: ', self.iwait)

        if self.state == BLOCKED:
            self.iwait += 1

            if self.iwait == self.itime:
                self.iwait = 0
                self.state = READY

        if self.state == EXECUTING:
            # Presents a chance to change to I/O
            if self.draw():
                print('\tBLOCKING. . .')
                self.state = BLOCKED
            else:
                print('\tUPDATING PWAIT')

                self.mem_pos = randint(0, 4)

                # Continue processing
                self.pwait += 1

                if self.pwait == self.ptime:
                    self.pwait = 0
                    self.state = READY

        print('\tSTATE: ', self.state)

        print('\tA PWAIT: ', self.pwait)
        print('\tA IWAIT: ', self.iwait)

class ControlBlock:

    def __init__(self, process, PID, priority, quantum, tickets, mem_pos):
        self.process            = process
        self.PID                = PID
        self.priority           = priority
        self.quantum            = quantum
        self.tickets            = tickets

        self.default_priority   = priority
        self.default_quantum    = quantum
        self.default_tickets    = tickets

        self.mem_pos            = mem_pos

    def decrease_priority(self):
        self.priority -= 1

    def decrease_quantum(self):
        self.quantum -= 1

    def decrease_tickets(self):
        self.tickets -= 1

    def calculate_dynamic(self):
        if self.quantum == 0:
            return 0

        return self.priority/self.quantum

    def init(self):
        self.process.begin()

    def preempt(self):
        self.process.preempt()

    def reset(self):
        self.priority = self.default_priority
        self.quantum = self.default_quantum
        self.tickets = self.default_tickets

    def get_status(self):
        return self.process.get_status()

    def update(self):
        print('PROCESS UPDATE: ', self.PID)

        self.process.update()

        self.mem_translate_pos = self.mem_pos * self.process.mem_pos

class ProcessManager:

    def __init__(self, psize, scheduling_type):
        self.psize = psize
        self.scheduling_type = scheduling_type

        self.pslot = False
        self.islot = False

        self.pbuffer = []
        self.ibuffer = []
        self.sbuffer = []

        self.last_mem = 0
        self.free_pos = []

        self.time = 0
        self.pid_count = 0

        self.mem = GerenciadorMemoriaVirtual()

    def generate_pid(self):
        self.pid_count += 1
        return self.pid_count

    def add_process(self, type, priority, quantum, tickets):
        PID = self.generate_pid()

        if (len(self.free_pos) > 0):
            mem = self.free_pos.pop()
        else:
            mem = self.last_mem
            self.last_mem += 1

        p = Process(type)
        c = ControlBlock(p, PID, priority, quantum, tickets, mem)

        self.pbuffer.append(c)

    def remove_process(self, PID):
        if self.pslot and self.pslot.PID == PID:
            deleted_process = self.pslot
            self.pslot = False

        if self.islot and self.islot.PID == PID:
            deleted_process = self.islot
            self.islot = False

        for cb in self.pbuffer:
            if cb.PID == PID:
                deleted_process = cb
                self.pbuffer.remove(cb)

        for cb in self.ibuffer:
            if cb.PID == PID:
                deleted_process = cb
                self.ibuffer.remove(cb)

        for i in range(deleted_process.mem_pos, deleted_process.mem_pos + 5):
            self.mem.free_mem(i)

        self.free_pos.append(deleted_process.mem_pos)

    def suspend_process(self, PID):
        if self.pslot:
            if self.pslot.PID == PID:
                self.pslot.preempt()
                self.sbuffer.append(self.pslot)
                self.pslot = False
                return True

        for cb in self.pbuffer:
            if cb.PID == PID:
                self.pbuffer.remove(cb)
                self.sbuffer.append(cb)
                return True

        for cb in self.ibuffer:
            if cb.PID == PID:
                self.ibuffer.remove(cb)
                self.sbuffer.append(cb)
                return True

        return False

    def resume_process(self, PID):

        for cb in self.sbuffer:
            if cb.PID == PID:
                s = cb.get_status()

                if s == READY:
                    self.pbuffer.append(cb)
                    self.sbuffer.remove(cb)
                    return True

                if s == BLOCKED:
                    self.ibuffer.append(cb)
                    self.sbuffer.remove(cb)
                    return True
        return False

    def change_scheduling(self, scheduling_type):
        self.scheduling_type = scheduling_type

# Interface Helper Function ------------------------------------------------------------------------

    def get_processes(self):
        processes = []

        if self.pslot:
            processes.append(self.pslot)

        if self.islot:
            processes.append(self.islot)

        if self.pbuffer:
            for cb in self.pbuffer:
                processes.append(cb)

        if self.ibuffer:
            for cb in self.ibuffer:
                processes.append(cb)

        return processes

# Data Structure Functions (CHANGE THIS) -----------------------------------------------------------

    def pop_first_process(self):
        if self.pbuffer:
            next = self.pbuffer[0]
            self.pbuffer.pop(0)

            return next
        return self.pslot

    def pop_first_io(self):
        if self.ibuffer:
            next = self.ibuffer[0]
            self.ibuffer.pop(0)

            return next
        return self.islot

    def get_highest_priority(self):
        if not self.pbuffer:
            return False

        mx = max(self.pbuffer, key=lambda x: x.priority)

        return mx

    def get_highest_dynamic(self):
        if not self.pbuffer:
            return False

        mx = max(self.pbuffer,
                key=lambda x: x.calculate_dynamic())

        return mx

#---------------------------------------------------------------------------------------------------
# They have to analyze if the pslot will change at all, so they can return the same pslot

    def round_robin(self):
        print('ROUND ROBIN')

        if self.pslot:
            self.pslot.decrease_quantum()

            if self.pslot.quantum == 0:             # Check if the quantum ended
                print('QUANTUM CHANGE')
                return self.pop_first_process()
            return self.pslot                       # Quantum not ended, continue
        return self.pop_first_process()             # Not processing, get next

    def round_robin_priority(self):
        print('ROUND ROBIN (PRIORITY)')

        mx = self.get_highest_priority()
        if self.pslot:
            self.pslot.decrease_quantum()

            if self.pslot.quantum == 0:
                print('QUANTUM CHANGE')
                self.pbuffer.remove(mx)
                return mx

            return self.pslot

        self.pbuffer.remove(mx)
        return mx

    def priority(self):
        print('PRIORITY')

        mx = self.get_highest_priority()
        if self.pslot and mx:
            if mx.priority > self.pslot.priority:
                self.pbuffer.remove(mx)
                return mx

            self.pslot.decrease_priority()
            return self.pslot

        if not self.pslot and mx:
            self.pbuffer.remove(mx)
            return mx

        return self.pslot

    def dynamic_priority(self):
        print('DYNAMIC PRIORITY')

        mx = self.get_highest_dynamic()
        if self.pslot and mx:
            if mx.calculate_dynamic() > self.pslot.calculate_dynamic():
                self.pbuffer.remove(mx)
                return mx

            self.pslot.decrease_quantum()
            return self.pslot

        if not self.pslot and mx:
            self.pbuffer.remove(mx)
            return mx

        return self.pslot

    def lottery(self):
        # End one before to give the chance to the last one
        if self.pbuffer:
            cumsum = sum((cb.tickets for cb in self.pbuffer))
            if cumsum <= 1:
                return self.pslot

            d = randint(1, cumsum)

            s = 0
            for cb in self.pbuffer:
                s += cb.tickets

                if s >= d:
                    cb.decrease_tickets()
                    self.pbuffer.remove(cb)
                    return cb
        return self.pslot

    def schedule(self):
        sched = {
                'ROUND ROBIN'               : self.round_robin,
                'ROUND ROBIN (PRIORITY)'    : self.round_robin_priority,
                'PRIORITY'                  : self.priority,
                'DYNAMIC PRIORITY'          : self.dynamic_priority,
                'LOTTERY'                   : self.lottery
                }[self.scheduling_type]

        next = sched()
        if not next:
            self.pslot = next
            return

        if next != self.pslot:
            if self.pslot:
                self.pslot.preempt()
                self.pbuffer.append(self.pslot)

            self.pslot = next
            self.pslot.init()

    def io_set(self):
        print('SETTING THE IO')

        if not self.islot:
            self.islot = self.pop_first_io()

#---------------------------------------------------------------------------------------------------

    def resolve_executing(self):
        print('RESOLVE EXECUTING')

        s = self.pslot.get_status()

        if s == BLOCKED:
            print('\tFOUND BLOCK')
            self.pslot.reset()
            self.ibuffer.append(self.pslot)
            self.pslot = False

        if s == READY:
            print('\tFOUND READY')
            self.pslot.reset()
            self.pbuffer.append(self.pslot)
            self.pslot = False

        if s == EXECUTING:
            self.mem.requestMem(self.pslot.PID, self.pslot.mem_translate_pos)

    def resolve_blocked(self):
        s = self.islot.get_status()

        if s == READY:
            self.pbuffer.append(self.islot)
            self.islot = False

    def update(self):

        self.time += 1
        # Update the main processes
        if self.pslot:
            # Update pslot

            self.pslot.update()
            self.resolve_executing()


        if self.islot:
            # Update pslot

            self.islot.update()
            self.resolve_blocked()

        self.schedule()
        self.io_set()

