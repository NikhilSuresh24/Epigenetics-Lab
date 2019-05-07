import random
import numpy as np

class Simulator:
    def __init__(self):
        self.permutation = ['gr', 'nw', 'aq', 'sb', 'wm', 'rm', 'em', 'wa', 'ra', 'ea']
        self.v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        random.shuffle(self.permutation)

    def reset(self, startv, startx):
        if len(startv) != 10 or len(startx) != 10:
            print("startv and startx must be length 10")
            return;

        self.x = startx
        self.v = startv

    def step(self):
        nextv = []
        nextx = []
        for i in self.v:
            if i == -1:
                rm = self.permutation.index('rm')
                em = self.permutation.index('em')
                nextv.append(self.x[rm]*self.x[em]-1) 
                nextx.append(1-self.x[rm])
            elif i == 1:
                ra = self.permutation.index('ra')
                ea = self.permutation.index('ea')
                nextv.append(1-self.x[ra]*self.x[ea])
                nextx.append(1)
            elif i == 0:
                wm = self.permutation.index('wm')
                wa = self.permutation.index('wa')
                h = 2*np.random.binomial(1, 0.5) - 1
                nextv.append(-self.x[wm] + self.x[wa] + h*self.x[wm]*self.x[wa])
                nextx.append(1)
        self.v = nextv
        self.x = nextx

        return (nextv, nextx)

    def print_state(self):
        print('p: ', end='')
        print(' '.join(self.permutation))

        print('v: ', end='')
        for i in self.v:
            if i == -1:
                print(i, end=' ')
            else:
                print(i, end='  ')

        print('\nx: ', end='')
        for i in self.x:
            if i == -1:
                print(i, end=' ')
            else:
                print(i, end='  ')
        
        print('\n')

        gr = self.permutation.index('gr')
        nw = self.permutation.index('nw')
        aq = self.permutation.index('aq')
        sb = self.permutation.index('sb')

        phenotype = []
        phenotype.append('R' if self.x[gr] == 0 else 'G')
        phenotype.append('W' if self.x[nw] == 0 else 'N')
        phenotype.append('Q' if self.x[aq] == 0 else 'A')
        phenotype.append('B' if self.x[sb] == 0 else 'S')
        print(''.join(phenotype))


test = Simulator()
test.reset([1,-1,1,0,1,1,1,-1,-1,0], [1, 0, 1, 1, 1, 1, 1, 0, 0, 1])
test.print_state()
test.step()
test.print_state()
