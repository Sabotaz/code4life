import sys
import time
def millis():
    return int(round(time.time() * 1000))

# Bring data on patient samples from the diagnosis machine to the laboratory with enough molecules to produce medicine!
_=int
def err(*x):print(x, file=sys.stderr)

class GameState:
    def __init__(self):
        self.samples = []

project_count = _(input())
for i in range(project_count):
    a, b, c, d, e = [_(j) for j in input().split()]
    
mol = []
samples = []

class Sample:
    def __init__(self, sid, uid, rank, exp, pts, a, b, c, d, e):
        self.sid = _(sid)
        self.uid = _(uid)
        self.rank = _(rank)
        self.exp = exp
        self.pts = _(pts)
        self.a = _(a)
        self.b = _(b)
        self.c = _(c)
        self.d = _(d)
        self.e = _(e)
    def print_state(self):
        err(self.a, self.b, self.c, self.d, self.e)
    
    def can_reduce_cost(self, player, sample):
        molecule = self.exp.lower()
        price = getattr(sample,molecule)
        expertise = getattr(player, "e"+molecule)
        return expertise < price
        
class Player:
    def __init__(self, target, eta, score, a, b, c, d, e, ea, eb, ec, ed, ee):
        self.target = target
        self.eta = _(eta)
        self.score = _(score)
        self.a, self.b, self.c, self.d, self.e = _(a), _(b), _(c), _(d), _(e)
        self.ea, self.eb, self.ec, self.ed, self.ee = _(ea), _(eb), _(ec), _(ed), _(ee)
        samples = []
        
    def getAction(self):
        if self.target == "START_POS":
            return "GOTO SAMPLES"
        if self.target == "SAMPLES":
            if len(self.samples) < 3:
                return self.take_sample()
            else:
                return "GOTO DIAGNOSIS"
        if self.target == "DIAGNOSIS":
            if self.have_undiagnosed_samples():
                return self.diagnose_sample()
            else:
                if len(self.samples) < 2:
                    return "GOTO SAMPLES"
                else:
                    return "GOTO MOLECULES"
        if self.target == "MOLECULES":
            s = self.a + self.b + self.c + self.d + self.e
            if s < 10:
                return self.take_molecule()
            else:
                if any(self.can_validate(s) for s in self.samples):
                    return "GOTO LABORATORY"
                elif len(self.samples) == 3:
                    return "GOTO DIAGNOSIS"
                else:
                    return "GOTO SAMPLES"
        if self.target == "LABORATORY":
            if any(self.can_validate(s) for s in self.samples):
                return self.validate_sample()
            if len(self.samples) > 0:
                return "GOTO MOLECULES"
            else:
                return "GOTO SAMPLES"
        
    def print_state(self):
        err("I AM IN " + self.target)
        err("I HAVE ", self.a, self.b, self.c, self.d, self.e)
        err("I OWN :")
        for s in self.samples:
            s.print_state()
        
    def take_sample(self):
        x = self.ea + self.eb + self.ec + self.ed + self.ee
        # 1,1,1 - 1,1,2 - 1,2,2, - 2,2,2 - 2,2,3 - 2,3,3 - 3,3,3
        choices = [[1,1,1], [1,1,2], [1,2,2], [2,2,2], [2,2,3], [2,3,3], [3,3,3]]
        n = min(len(choices)-1,max(0, x-4))
        if self.rooms() == 0:
            n = 3
        return "CONNECT " + str(choices[n][len(self.samples)])
        
    def have_undiagnosed_samples(self):
        for s in self.samples:
            if s.a == -1:
                return True
            elif self.price(s) > self.rooms():
                return True
        return False
        
    def rooms(self):
        return 10 - (self.a + self.b + self.c + self.d + self.e)
        
    def diagnose_sample(self):
        #if len(self.samples) < 3:
        #    for s in samples:
        #        if self.can_validate(s):
        #            return "CONNECT " + str(s.sid)
        for s in self.samples:
            if s.a == -1:
                return "CONNECT " + str(s.sid)
            elif self.price(s) > self.rooms():
                return "CONNECT " + str(s.sid)

    def price(self, s):
        a = max(0, s.a - self.a - self.ea)
        b = max(0, s.b - self.b - self.eb)
        c = max(0, s.c - self.c - self.ec)
        d = max(0, s.d - self.d - self.ed)
        e = max(0, s.e - self.e - self.ee)
        return a+b+c+d+e
        
    def take_molecule(self):
        a = self.a
        b = self.b
        c = self.c
        d = self.d
        e = self.e
        ordered_samples = sorted(self.samples, key=lambda x: self.price(x))
        for s in self.samples:
            a -= max(0, s.a - self.ea)
            b -= max(0, s.b - self.eb)
            c -= max(0, s.c - self.ec)
            d -= max(0, s.d - self.ed)
            e -= max(0, s.e - self.ee)
            needs = [mol[i] if x < 0 and mol[i] else 0 for i, x in enumerate([a, b, c, d, e])]
            if (any(needs)):
                return "CONNECT " + "ABCDE"[needs.index(min(filter(lambda x:x, needs)))]
        if any(self.can_validate(s) for s in self.samples):
            return "GOTO LABORATORY"
        elif len(self.samples) == 3:
            return "GOTO DIAGNOSIS"
        else:
            return "GOTO SAMPLES"
        m = min("abcde", key = lambda l: getattr(self,l) + getattr(self,"e"+l)).upper()
        return "CONNECT " + m
            
    def can_validate(self, sample):
        return self.a + self.ea >= sample.a and self.b + self.eb >= sample.b and self.c + self.ec >= sample.c and self.d + self.ed >= sample.d and self.e + self.ee >= sample.e

    def validate_sample(self):
        s = max(filter(lambda t: self.can_validate(t), self.samples), key = lambda s: sum(s.can_reduce_cost(self,x) for x in self.samples if x != s))
        err("x:")
        s.print_state()
        return "CONNECT " + str(s.sid)
        
# game loop
while True:
    moi = Player(*input().split())
    t1 = millis()
    lui = Player(*input().split())
    
    mol = [int(i) for i in input().split()]
    
    sample_count = int(input())
    
    samples = [Sample(*input().split()) for i in range(sample_count)]
    
    moi.samples = list(filter(lambda sample: sample.uid == 0, samples))
    lui.samples = list(filter(lambda sample: sample.uid == 1, samples))
    samples = list(filter(lambda sample: sample.uid == -1, samples))
    
    err("moi")
    moi.print_state()
    err("lui")
    lui.print_state()
    
    action = moi.getAction()
    t2 = millis()
    err(t2-t1)
    print(action)