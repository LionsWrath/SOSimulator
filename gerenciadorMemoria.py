from collections import defaultdict

class Frame:
    def __init__(self):
        self.memPos = -1
        self.PID = -1
        self.presente = False
        self.age = -1

class GerenciadorMemoriaVirtual:
    def __init__(self, size=100):
        self.frames = defaultdict(Frame)
        self.mem = [None] * 100

    def susbtitute(self, rankNew, PID):
        substituido = max(filter(lambda x: x is not None and x.presente, self.mem), 
                key=lambda x: x.age)
        substituido.presente = False

        self.frames[rankNew].presente = True
        self.frames[rankNew].memPos = substituido.memPos
        self.frames[rankNew].age = 0
        self.frames[rankNew].PID = PID

        self.mem[self.frames[rankNew].memPos] = self.frames[rankNew]

    def requestMem(self, PID, rank):
        if (rank > 0 and not self.frames[rank].presente):
            print("PAGE FAULT")
            i = 0

            while(i < 100 and self.mem[i] is not None):
                i += 1

            if (i < 100):
                self.mem[i] = self.frames[rank]
                self.mem[i].PID = PID
                self.mem[i].age = 0
                self.mem[i].memPos = i
                self.mem[i].presente = True
            else:
                self.susbtitute(rank, PID)

    def free_mem(self, rank):
        if (self.frames[rank].presente):
            self.mem[self.frames[rank].memPos] = None

        self.frames[rank].presente = False

    def update(self):
        for frame in filter(lambda x: x is not None and x.presente, self.mem):
            frame.age += 1
