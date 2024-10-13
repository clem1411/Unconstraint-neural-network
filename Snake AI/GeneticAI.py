import random


class Controller:
    def get_direction(self):
        """Cette méthode doit être implémentée par les sous-classes pour retourner la direction."""
        raise NotImplementedError("Must be implemented in subclasses")

class Genome():
    genes = {}
    fitness = 0
    def __init__(self,genes):
        self.genes = genes

class AIController(Controller):
    genomes = []
    def __init__(self,genomes):
        self.genomes = genomes
    def get_direction(self):
        return random.choice(['left', 'right', 'up', 'down'])
    
def createGenome():
    genes = {}
    for i in range(0, 16):
        if i not in genes:
            genes[i] = []
        for j in range(16, 48):
            genes[i].append((j, random.uniform(-1, 1)))
    for i in range(16, 48):
        if i not in genes:
            genes[i] = []
        for j in range(48, 80):
            genes[i].append((j, random.uniform(-1, 1)))
    for i in range(48, 80):
        if i not in genes:
            genes[i] = []
        for j in range(80, 84):
            genes[i].append((j, random.uniform(-1, 1)))
    return Genome(genes)

controller = AIController([])
genomes = []
# Call create genome and print the result
genomes.append(createGenome())
controller = AIController(genomes)
for gene_key, gene_value in controller.genomes[0].genes.items():
    print(f"Gene {gene_key}: {gene_value}")