import numpy as np
from simulator import Simulator


class BackSolve:
    def __init__(self, debug=False):
        self.debug = debug
        self.sim = Simulator()
        self.active_phenotype = "GNAS"
        self.methylated_phenotype = "RWQB"
        self.num_genes = 10
        # Values correspond to true positions of genes in the following order: C, S, A, T, W_M, W_A, R_M, R_A, E_M, E_A
        self.order = np.full(self.num_genes, -1)

    def phase_zero(self):
        if self.debug:
            print("---------Phase Zero----------")
        genes_found = 0
        for i in range(10):
            genome = np.full(self.num_genes, -1)
            genome[i] = 1
            phenotype = np.where(genome == -1, 0, genome)
            self.sim.reset(genome, phenotype)
            self.sim.step()
            # phenotype at t=1
            p_1 = self.sim.print_state(False)
            if self.debug:
                print("t=1 P:", p_1)
            if p_1 == "RWQB":
                self.order[6] = i
                genes_found += 1
                if self.debug:
                    print("found RM", i)
            v, x = self.sim.step()
            p_2 = self.sim.print_state(False)
            if self.debug:
                print("p_2", p_2)
            if p_2 == self.methylated_phenotype:
                if self.debug:
                    print("skipped")
                continue
            for idx, gene in enumerate(p_2):
                if gene == self.active_phenotype[idx]:
                    if self.debug:
                        print("COMP", gene, i, idx)
                    self.order[idx] = i
                    genes_found += 1
                    continue
            if genes_found == 5:
                print("found all genes, ending early")
                break

    def phase_one(self):
        '''Find E_M'''
        genome = np.full(self.num_genes, -1)
        print(self.order, self.order[6])
        genome[self.order[6]] = 1
        print("genome", genome)
        for i in range(self.num_genes):
            if i not in self.order:
                # print(i)
                genome[i] = 1
                print("2", genome)
                phenotype = np.where(genome == -1, 0, genome)
                self.sim.reset(genome, phenotype)
                print("v,x", self.sim.v, self.sim.x)
                v, x = self.sim.step()
                print(x)
                print(np.all(x == 1))
                if np.all(x == 1):

                    self.order[8] = i
                    break
                # if x == np.ones((1, self.num_genes)):
                #     self.order[8] = i
                #     break

    def phase_two():
        pass


x = BackSolve()
# x.order = np.array([2, 8, 3, 6, -1, -1, 5, -1, -1, -1])
x.phase_zero()
print(x.order)
# x.phase_one()
