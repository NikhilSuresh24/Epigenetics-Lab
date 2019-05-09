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
        '''FIND C, S, A, T, R_M'''
        if self.debug:
            print("---------Phase Zero----------")
        genes_found = 0
        for i in range(self.num_genes):
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
        R_m_pos = 6
        E_m_pos = 8

        for i in range(self.num_genes):
            genome = np.full(self.num_genes, -1)
            genome[self.order[R_m_pos]] = 1

            if i not in self.order:
                genome[i] = 1
                phenotype = np.where(genome == -1, 0, genome)
                self.sim.reset(genome, phenotype)
                self.sim.step()
                self.sim.step()
                p_2 = self.sim.print_state(False)
                if self.debug:
                    print("P_2", p_2)
                if p_2 == self.active_phenotype:
                    self.order[E_m_pos] = i
                    print("found E_M", i)
                    break

    def phase_two(self):
        '''find W_A, W_M'''
        C_pos = 0
        W_m_pos = 4
        W_a_pos = 5
        genes_found = 0
        for i in range(self.num_genes):
            genome = np.full(self.num_genes, -1)
            genome[self.order[C_pos]] = 0
            if i not in self.order:
                genome[i] = 1
                phenotype = np.where(genome == -1, 0, genome)
                print("0", genome, genome[self.order[C_pos]])
                self.sim.reset(genome, phenotype)
                v, x = self.sim.step()
                print(v, v[C_pos])
                if v[C_pos] == 0:
                    continue
                elif v[C_pos] == -1:
                    self.order[W_m_pos] = i
                    print("found W_M", i)
                    genes_found += 1
                elif v[C_pos] == 1:
                    self.order[W_a_pos] = i
                    print("found W_A", i)
                    genes_found += 1
            if genes_found == 2:
                print("found genes, done early")
                break


x = BackSolve()
# x.order = np.array([2, 8, 3, 6, -1, -1, 5, -1, -1, -1])
x.phase_zero()
# print(x.order)
x.phase_one()
x.phase_two()
print(x.order)
