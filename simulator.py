import numpy as np
import random


class Simulator:
    def __init__(self):
        self.permutation = ['gr', 'nw', 'aq', 'sb',
                            'wm', 'rm', 'em', 'wa', 'ra', 'ea']
        self.num_genes = 10
        self.v = np.zeros(self.num_genes)
        self.x = np.zeros(self.num_genes)
        # self.v = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        # self.x = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        random.shuffle(self.permutation)

    def reset(self, startv, startx):
        if len(startv) != self.num_genes or len(startx) != self.num_genes:
            print("startv and startx must be length {}".format(self.num_genes))
            return

        self.x = startx
        self.v = startv

    def step(self):
        nextv = np.empty(self.num_genes)
        nextx = np.empty(self.num_genes)
        # nextv = []
        # nextx = []
        for idx, val in np.ndenumerate(self.v):
            if val == -1:
                rm = self.permutation.index('rm')
                em = self.permutation.index('em')
                nextv[idx] = self.x[rm]*self.x[em]-1
                nextx[idx] = 1-self.x[rm]
                # nextv.append(self.x[rm]*self.x[em]-1)
                # nextx.append(1-self.x[rm])
            elif val == 1:
                ra = self.permutation.index('ra')
                ea = self.permutation.index('ea')
                nextv[idx] = 1-self.x[ra]*self.x[ea]
                nextx[idx] = 1
                # nextv.append(1-self.x[ra]*self.x[ea])
                # nextx.append(1)
            elif val == 0:
                wm = self.permutation.index('wm')
                wa = self.permutation.index('wa')
                h = 2*np.random.binomial(1, 0.5) - 1
                nextv[idx] = -self.x[wm] + self.x[wa] + h*self.x[wm]*self.x[wa]
                nextx[idx] = 1
                # nextv.append(-self.x[wm] + self.x[wa] +
                #              h*self.x[wm]*self.x[wa])
                # nextx.append(1)
        self.v = nextv
        self.x = nextx

        return (nextv, nextx)

    def print_state(self, debug=True):
        if debug:
            print('p: ', end='')
            print(' '.join(self.permutation))

            print('v: ', end='')
        for i in self.v:
            if i == -1:
                if debug:
                    print(i, end=' ')
            else:
                if debug:
                    print(i, end='  ')

        if debug:
            print('\nx: ', end='')
        for i in self.x:
            if i == -1:
                if debug:
                    print(i, end=' ')
            else:
                if debug:
                    print(i, end='  ')

        if debug:
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
        if debug:
            print(''.join(phenotype))
        return ''.join(phenotype)
