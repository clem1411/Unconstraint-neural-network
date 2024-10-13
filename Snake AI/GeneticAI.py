import random
import math
import csv
import json


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
    Best3Genome = []
    def __init__(self,nbGenomes):
        for i in range(0,nbGenomes):
            self.genomes.append(createGenome())
    def get_direction(self,inputData,genomeIndex):
        output = ComputeForward(self.genomes[genomeIndex], inputData)
        #print(output)
        if max(output, key=output.get) == 80:
            return "up"
        elif max(output, key=output.get) == 81:
            return "down"
        elif max(output, key=output.get) == 82:
            return "left"
        elif max(output, key=output.get) == 83:
            return "right"
        elif max(output, key=output.get) == 84:
            return "NONE"
    def setFitness(self,genomeIndex,fitness):
        self.genomes[genomeIndex].fitness = fitness

    def newGeneration(self,numGeneration):
        self.genomes = sorted(self.genomes, key=lambda x: x.fitness, reverse=True)
        best_fitness = self.genomes[0].fitness
        average_fitness = sum([x.fitness for x in self.genomes]) / len(self.genomes)
        if(len(self.Best3Genome) < 3):
            self.Best3Genome.append(self.genomes[0])
            self.Best3Genome.append(self.genomes[1])
            self.Best3Genome.append(self.genomes[2])
        elif(self.Best3Genome[0].fitness < best_fitness):
            self.Best3Genome[0] = self.genomes[0]
        elif(self.Best3Genome[1].fitness < best_fitness):
            self.Best3Genome[1] = self.genomes[0]
        elif(self.Best3Genome[2].fitness < best_fitness):
            self.Best3Genome[2] = self.genomes[0]

        with open('fitness_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([best_fitness, average_fitness])
        newGenomes = []
        for i in range(0, 4):
            newGenomes.append(self.genomes[i])
        for i in range(4, 7):
            newGenomes.append(self.Best3Genome[6-i])
        for i in range(7, 100):
            newGenomes.append(crossMute(self.genomes[:4],numGeneration))
        self.genomes = newGenomes

    def saveBestGenome(self):
        with open('bestGenome.json', mode='w') as file:
            json.dump({k: v for k, v in self.Best3Genome[0].genes.items()}, file)
        
    def saveTrainingState(self):        #TODO
        with open('training_state.json', mode='w') as file:
            json.dump(self.genomes, file)
    
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

def crossMute(genomes,numGeneration):
    genome1 = genomes[random.randint(0, 3)]
    genome2 = genomes[random.randint(0, 3)]

    mute_rate = 0.2-math.log(numGeneration+1)/50
    newGenes= {}
    for i in range(0, 16):
        if i not in newGenes:
            newGenes[i] = []
        for j in range(0, 32):
            choice = random.uniform(0, 1)
            if choice <= 0.45:
                newGenes[i].append(genome1.genes[i][j])
            elif choice <= 1.0-mute_rate:
                newGenes[i].append(genome2.genes[i][j])
            else:
                newGenes[i].append((j+12, random.uniform(-1, 1)))
    for i in range(16, 48):
        if i not in newGenes:
            newGenes[i] = []
        for j in range(0, 32):
            choice = random.uniform(0, 1)
            if choice <= 0.45:
                newGenes[i].append(genome1.genes[i][j])
            elif choice <= 0.9:
                newGenes[i].append(genome2.genes[i][j])
            else:
                newGenes[i].append((j+44, random.uniform(-1, 1)))
    for i in range(48, 80):
        if i not in newGenes:
            newGenes[i] = []
        for j in range(0, 5):
            choice = random.uniform(0, 1)
            if choice <= 0.45:
                newGenes[i].append(genome1.genes[i][j])
            elif choice <= 0.9:
                newGenes[i].append(genome2.genes[i][j])
            else:
                newGenes[i].append((j+80, random.uniform(-1, 1)))
    return Genome(newGenes)



class AITrainedControler(Controller):
    genome = {}
    def __init__(self):
        with open('bestGenome.json', mode='r') as file:
            genes = json.load(file)
            self.genome = Genome({int(k): v for k, v in genes.items()})
    def get_direction(self,inputData):
        output = ComputeForward(self.genome, inputData)
        if max(output, key=output.get) == 80:
            return "up"
        elif max(output, key=output.get) == 81:
            return "down"
        elif max(output, key=output.get) == 82:
            return "left"
        elif max(output, key=output.get) == 83:
            return "right"
        elif max(output, key=output.get) == 84:
            return "NONE"
# controller = AIController(4)
# print(AIController.get_direction(controller, [1,1,1,1,0,1,0,1,0,1,0,1,0,1,0,1], 0))