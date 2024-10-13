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
        if  max(output, key=output.get) == 80:
            return "UP"
        elif max(output, key=output.get) == 81:
            return "DOWN"
        elif max(output, key=output.get) == 82:
            return "LEFT"
        elif max(output, key=output.get) == 83:
            return "RIGHT"
        elif max(output, key=output.get) == 84:
            return "NONE"
    
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
        for j in range(80, 85):
            genes[i].append((j, random.uniform(-1, 1)))
    return Genome(genes)

def ComputeForward(genome, inputs):
    outputs = {}
    for i in range(0, 16):
        outputs[i] = inputs[i]
    for i in range(16, 85):
        outputs[i] = 0

    for i in range(0, 16):
        for j in range(16, 48):
            outputs[j] += genome.genes[i][j-16][1] * inputs[i]
    for i in range(16, 48):
        for j in range(48, 80):
            outputs[j] += genome.genes[i][j-48][1] * outputs[i]
    for i in range(48, 80):
        for j in range(80, 85):
            outputs[j] += genome.genes[i][j-80][1] * outputs[i]
    return {k: outputs[k] for k in range(80, 85)}

# controller = AIController(4)
# print(AIController.get_direction(controller, [1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1], 0))