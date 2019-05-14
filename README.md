# Simulation and Locating of Randomly Ordered Epigenetic Genes

In this experiment, 10 genes, 4 phenotypic genes, and 6 epigenetic genes, are put in a random order. The simulation takes in as input an initial list of epigenetic markings, and the list of the gene's expression, which will be clarified later.

## Experimental Background

Epigenetic modifications are physical changes to the genome that modify its expression without changing the DNA itself.The best understood of these changes are Methylation and Acetylation, which this lab is based upon. 

Methylation is the addition of a methyl group, CH<sub>3</sub>, to nucleotide, typically cytosines. When a nucleotide is methylated, transcription factors, which are used express DNA, cannot bind to the DNA, thus preventing expression.

Acetylation is the addition of an acetyl group, C<sub>2</sub>H<sub>3</sub>O, to a histone around which DNA is tightly. As a result, the DNA becomes less tightly wrapped around the histone, and transcription factors can bind to the DNA easier. Acetylation promotes gene expression.

In this simulation, we are dealing with 6 epigenetic genes, erasers, writers, and readers, for both acetylation and methylation. Readers are proteins that are needed for methylation or acetylation marks to actually affect gene expression. Without readers, epigenetic marks do not affect the phenotype. Writers are the proteins that actually create and attach the methyl or acetyl groups to the genome. Finally, erasers erase epigenetic markings, making epigenetic modifications inpermanent.

## Experiment Explanation
As mentioned earlier, the simulation randomizes the order of the 10 genes, and when simulates the change in epigenetic markings and gene expression of the genes over timesteps depending on the previous markings and expressions. 

For markings, `0` represents an unmarked gene, which is expressed in this simulation, `1` represents an acetylated gene, which is also expressed, and `-1` represents a methylated gene, which is not expressed. 

On the other hand, gene expression for every gene is either represented as a `0` or a `1` depending on if the gene is not expressed or expressed respectively.

The simulation takes as input an initial set of markings, numpy array of length 10, and a corresponding set of gene expression, another numpy array of length 10. 

An important assumption of this simulation is that the epigenetic markings in time `t=0` will affect the markings and gene expression of `t=1`. 

## Simulation

To run the simulation, a variant of the following code will work in python3:

    from simulator import Simulator
    import numpy as np

    s = Simulator()
    markings_0 = np.array([])
    expression_0 = np.array([])
    s.reset(markings, expression)
    markings_1, expression_1 = s.step()
    phenotype_1 = s.print_state()

## Simulation Visualization

To run a visualization of the simulation, run the following command in Terminal:

    python3 visualize.py

## Backsolve Algorithm

## Backsolve Code

To run the backsolve algorithm to deterimine the randomized order of the genes, run the following command:

    python3 backsolve.py

As its final output, it will print out the position of the genes.
