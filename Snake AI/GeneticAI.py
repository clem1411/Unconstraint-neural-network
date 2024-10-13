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
    def __init__(self,nbGenomes):
        for i in range(0,nbGenomes):
            self.genomes.append(createGenome())
    def get_direction(self,inputData,genomeIndex):
        output = ComputeForward(self.genomes[genomeIndex], inputData)
        print(output)
        if max(output, key=output.get) == 76:
            return "up"
        elif max(output, key=output.get) == 77:
            return "down"
        elif max(output, key=output.get) == 78:
            return "left"
        elif max(output, key=output.get) == 79:
            return "right"
        elif max(output, key=output.get) == 80:
            return "NONE"
    
def createGenome():
    genes = {}
    for i in range(0, 12):
        if i not in genes:
            genes[i] = []
        for j in range(12, 44):
            genes[i].append((j, random.uniform(-1, 1)))
    for i in range(12, 44):
        if i not in genes:
            genes[i] = []
        for j in range(44, 76):
            genes[i].append((j, random.uniform(-1, 1)))
    for i in range(44, 76):
        if i not in genes:
            genes[i] = []
        for j in range(76, 81):
            genes[i].append((j, random.uniform(-1, 1)))
    return Genome(genes)

def ComputeForward(genome, inputs):
    outputs = {}
    for i in range(0, 12):
        outputs[i] = inputs[i]
    for i in range(12, 81):
        outputs[i] = 0

    for i in range(0, 12):
        for j in range(12, 44):
            outputs[j] += genome.genes[i][j-16][1] * inputs[i]
    for i in range(12, 44):
        for j in range(44, 76):
            outputs[j] += genome.genes[i][j-48][1] * outputs[i]
    for i in range(44, 76):
        for j in range(76, 81):
            outputs[j] += genome.genes[i][j-80][1] * outputs[i]
    return {k: outputs[k] for k in range(76, 81)}

# controller = AIController(4)
# print(AIController.get_direction(controller, [1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1], 0))