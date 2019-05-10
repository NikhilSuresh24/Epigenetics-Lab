import numpy as np
from simulator import Simulator


class BackSolve:
    def __init__(self, debug=False, logging=False):
        self.debug = debug
        self.logging = logging
        self.log_string = ""
        self.log_file_path = "backsolve.log"
        self.sim = Simulator()
        self.active_phenotype = "GNAS"
        self.methylated_phenotype = "RWQB"
        self.num_genes = 10

        # Values correspond to true positions of genes in the following order: C, S, A, T, W_M, W_A, R_M, R_A, E_M, E_A
        self.order = np.full(self.num_genes, -1)

    def log_debug_print(self, message):
        if self.debug:
            print(message)
        if self.logging:
            self.log_string += message + "\n"

    def save_file(self):
        log_file = open(self.log_file_path, "w+")
        log_file.write(self.log_string)

    def phase_zero(self):
        '''FIND C, S, A, T, R_M'''
        self.log_debug_print("---------Phase Zero----------")
        genes_found = 0
        for pos in range(self.num_genes):
            self.log_debug_print("\nTrying Position: {}".format(pos))
            genome = np.full(self.num_genes, -1)
            genome[pos] = 1
            phenotype = np.where(genome == -1, 0, genome)
            self.sim.reset(genome, phenotype)
            self.sim.step()
            # phenotype at t=1
            p_1 = self.sim.print_state(False)
            self.log_debug_print("t=1 Phenotype:{}".format(p_1))
            if p_1 == "RWQB":
                self.order[6] = pos
                genes_found += 1
                self.log_debug_print("found RM, position: {}".format(pos))
            v, x = self.sim.step()
            p_2 = self.sim.print_state(False)
            self.log_debug_print("t=2 Phenotype: {}".format(p_2))
            if p_2 == self.methylated_phenotype:
                self.log_debug_print("skipped")
                continue
            for idx, gene in enumerate(p_2):
                if gene == self.active_phenotype[idx]:
                    self.log_debug_print(
                        "Unchanged Gene: {0} Position: {1}".format(gene, pos))
                    self.order[idx] = pos
                    genes_found += 1
                    continue
            if genes_found == 5:
                self.log_debug_print("found C,S,A,T, R_M, quitting early")
                break

    def phase_one(self):
        '''Find E_M'''
        R_m_pos = 6
        E_m_pos = 8
        self.log_debug_print("----------Phase One-------------")
        for pos in range(self.num_genes):
            genome = np.full(self.num_genes, -1)
            genome[self.order[R_m_pos]] = 1

            if pos not in self.order:
                genome[pos] = 1
                phenotype = np.where(genome == -1, 0, genome)
                self.sim.reset(genome, phenotype)
                self.sim.step()
                self.sim.step()
                p_2 = self.sim.print_state(False)
                self.log_debug_print("t=2 Phenotype: {}".format(p_2))
                if p_2 == self.active_phenotype:
                    self.order[E_m_pos] = pos
                    self.log_debug_print("found E_M Position: {}".format(pos))
                    break

    def phase_two(self):
        '''find W_A, W_M'''
        C_pos = 0
        W_m_pos = 4
        W_a_pos = 5
        genes_found = 0

        self.log_debug_print("----------Phase Two-------------")
        for pos in range(self.num_genes):
            genome = np.full(self.num_genes, -1)
            genome[self.order[C_pos]] = 0
            if pos not in self.order:
                genome[pos] = 1
                phenotype = np.where(genome == -1, 0, genome)
                print("t=0 State:", genome, genome[self.order[C_pos]])
                self.sim.reset(genome, phenotype)
                v, x = self.sim.step()
                if v[C_pos] == 0:
                    continue
                elif v[C_pos] == -1:
                    self.order[W_m_pos] = pos
                    self.log_debug_print("found W_M Position: {}".format(pos))
                    genes_found += 1
                elif v[C_pos] == 1:
                    self.order[W_a_pos] = pos
                    self.log_debug_print("found W_A Position: {}".format(pos))
                    genes_found += 1
            if genes_found == 2:
                self.log_debug_print("found W_A, W_M, finishing early")
                break

        self.log_debug_print("Position of Genes: {}".format(
            np.array2string(self.order)))
        self.save_file()


x = BackSolve(True, True)
x.phase_zero()
x.phase_one()
x.phase_two()
# print(x.order)
