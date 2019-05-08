import numpy as np
from simulator import Simulator


class BackSolve:
    def __init__(self):
        self.sim = Simulator()

        self.num_genes = 10
        # Values correspond to true positions of genes in the following order: C, S, A, T, W_M, W_A, R_M, R_A, E_M, E_A
        self.order = np.full(self.num_genes, -1)

    def phase_one(self):
        pass

    def phase_two(self):
        '''Find E_M'''
        genome = np.full(self.num_genes, -1)
        genome[self.order[6]] = 1

        for i in range(self.num_genes):
            if i not in self.order:
                genome[i] = 1
                phenotype = np.where(genome == -1, 0, genome)
                self.sim.reset(genome, phenotype)
                v, x = self.sim.step()
                print(x)
                print(np.all(x == 1))
                if np.all(x == 1):

                    self.order[8] = i
                    break
                # if x == np.ones((1, self.num_genes)):
                #     self.order[8] = i
                #     break

    def phase_three():
        ass


x = BackSolve()
x.order = np.array([2, 8, 3, 6, -1, -1, 5, -1, -1, -1])
x.phase_two()
print(x.order)
