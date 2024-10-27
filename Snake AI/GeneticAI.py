import random
import math
import csv
import json


class Controller:
    def get_direction(self):
        """Cette méthode doit être implémentée par les sous-classes pour retourner la direction."""
        raise NotImplementedError("Must be implemented in subclasses")

class Genome:
    def __init__(self, genes, bias):
        self.genes = genes
        self.fitness = 0
        self.bias = bias

    def copy(self):
        # Crée un nouvel objet Genome avec une copie profonde des gènes
        new_genes = {k: v[:] for k, v in self.genes.items()}  # Copie des gènes
        bias = self.bias[:]  # Crée une copie de la liste bias
        new_genome = Genome(new_genes,bias)
        new_genome.fitness = self.fitness  # Copie la valeur du fitness
        return new_genome

class AIController(Controller):
    def __init__(self,nbGenomes):
        self.genomes = []
        self.Best3Genome = []
        for i in range(0,nbGenomes):
            self.genomes.append(createGenome())
        with open('fitness_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["best_fitness", "average_fitness"])
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
            self.Best3Genome.append(self.genomes[0].copy())
            self.Best3Genome.append(self.genomes[1].copy())
            self.Best3Genome.append(self.genomes[2].copy())
        elif(self.Best3Genome[0].fitness < best_fitness):
            print("New best genome found fitness : " + str(best_fitness))
            self.Best3Genome[0] = self.genomes[0].copy()  # Remplace la valeur si elle existe
        elif(self.Best3Genome[1].fitness < best_fitness):
            self.Best3Genome[1] = self.genomes[0].copy()
        elif(self.Best3Genome[2].fitness < best_fitness):
            self.Best3Genome[2] = self.genomes[0].copy()



        with open('fitness_data.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([best_fitness, average_fitness])
        newGenomes = []
        for i in range(0, 4):
            newGenomes.append(self.genomes[i])
        for i in range(4, 7):
            newGenomes.append(self.Best3Genome[6-i].copy())
        for i in range(7, 50):
            newGenomes.append(crossMute(self.genomes[:7],numGeneration))
        for i in range(50, 100):
            newGenomes.append(mutate(self.genomes[random.randint(0, 6)],numGeneration))
        self.genomes = newGenomes


    def saveBestGenome(self):
        try:
            with open('bestGenome.json', mode='r') as file:
                data = json.load(file)
                best_fitness = data.get('fitness', 0)
        except (FileNotFoundError, json.JSONDecodeError):
            best_fitness = 0

        if self.Best3Genome[0].fitness > best_fitness:
            with open('bestGenome.json', mode='w') as file:
                data = {
                    'genes': {k: v for k, v in self.Best3Genome[0].genes.items()},
                    'bias': self.Best3Genome[0].bias,
                    'fitness': self.Best3Genome[0].fitness
                }
                json.dump(data, file)
    def saveTrainingState(self):        #TODO
        with open('training_state.json', mode='w') as file:
            json.dump(self.genomes, file)
    
def createGenome():
    genes = {}
    bias = [0]*85
    for i in range(0, 16):
        if i not in genes:
            genes[i] = []
        for j in range(16, 48):  
            genes[i].append((j, random.uniform(-1, 1)))
    for i in range(16, 48):
        bias[i] = random.uniform(-1, 1)  
        if i not in genes:
            genes[i] = []
        for j in range(48, 80):  
            genes[i].append((j, random.uniform(-1, 1)))
    for i in range(48, 80):
        bias[i] = random.uniform(-1, 1)  
        if i not in genes:
            genes[i] = []
        for j in range(80, 85):  
            genes[i].append((j, random.uniform(-1, 1)))
    
    return Genome(genes,bias)

def ComputeForward(genome, inputs):
    outputs = {}
    for i in range(0, 16):
        outputs[i] = inputs[i]
    for i in range(16, 85):
        outputs[i] = 0

    for i in range(0, 16):
        for j in range(16, 48):
            outputs[j] += genome.genes[i][j-16][1] * inputs[i]
    for h in range (16,48):
        outputs[h] = math.tanh(outputs[h]+genome.bias[h])
    for i in range(16, 48):
        for j in range(48, 80):
            if not isinstance(genome.genes[i][j-48][1], float) or not isinstance(outputs[i], float):
                print(f"i: {i}")
                print(f"j: {j}")
                print(f"genome.genes[i][j-48][1] type: {type(genome.genes[i][j-48][1])}")
                print(f"outputs[i] type: {type(outputs[i])}")
                print(f"genome.genes[i][j-48][1]: {genome.genes[i][j-48][1]}")
            outputs[j] += genome.genes[i][j-48][1] * outputs[i]
    for h in range (48,80):
        outputs[h] = math.tanh(outputs[h]+genome.bias[h])
    for i in range(48, 80):
        for j in range(80, 85):
            outputs[j] += genome.genes[i][j-80][1] * outputs[i]
    for h in range (80,85):
        outputs[h] = math.tanh(outputs[h]+genome.bias[h])
    return {k: outputs[k] for k in range(80, 85)}

def crossMute(genomes,numGeneration):
    genome1 = genomes[random.randint(0, 6)]
    genome2 = genomes[random.randint(0, 6)]

    mute_rate = 0.2-math.log(3*numGeneration+1)/50
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
                newGenes[i].append((j+16, random.uniform(-1, 1)))
    for i in range(16, 48):
        if i not in newGenes:
            newGenes[i] = []
        for j in range(0, 32):
            choice = random.uniform(0, 1)
            if choice <= 0.45:
                newGenes[i].append(genome1.genes[i][j])
            elif choice <= 1.0-mute_rate:
                newGenes[i].append(genome2.genes[i][j])
            else:
                newGenes[i].append((j+48, random.uniform(-1, 1)))
    for i in range(48, 80):
        if i not in newGenes:
            newGenes[i] = []
        for j in range(0, 5):
            choice = random.uniform(0, 1)
            if choice <= 0.45:
                newGenes[i].append(genome1.genes[i][j])
            elif choice <= 1.0-mute_rate:
                newGenes[i].append(genome2.genes[i][j])
            else:
                newGenes[i].append((j+80, random.uniform(-1, 1)))
    bias = [0]*85
    for i in range (16,85):
        choice = random.uniform(0, 1)
        if choice <= 0.4:
            bias[i] = genome1.bias[i]
        elif choice <= 0.8:
            bias[i] = genome2.bias[i]
        elif choice <= 0.9:
            bias[i] = genome1.bias[i] + random.gauss(0, 0.3-mute_rate)
        else:
            bias[i] = genome2.bias[i] + random.gauss(0, 0.3-mute_rate)


    
    return Genome(newGenes,bias)

def mutate(genome,numGeneration):

    mute_rate = math.log(3*numGeneration+1)/120
    newGenes= {}
    bias = [0]*85
    for i in range(0, 16):
        if i not in newGenes:
            newGenes[i] = []
        for j in range(0, 32):
            choice = random.uniform(0, 1)
            if choice <= 0.8:
                newGenes[i].append(genome.genes[i][j])
            elif choice <= 0.95+mute_rate:
                newGenes[i].append((j+16, genome.genes[i][j][1] + random.gauss(0, 0.3-mute_rate)))
            else:
                newGenes[i].append((j+16, random.uniform(-1, 1)))
    for i in range(16, 48):
        bias[i] = genome.bias[i] + random.gauss(0, 0.3-mute_rate)
        if i not in newGenes:
            newGenes[i] = []
        for j in range(0, 32):
            choice = random.uniform(0, 1)
            if choice <= 0.8:
                newGenes[i].append(genome.genes[i][j])
            elif choice <= 0.95+mute_rate:
                newGenes[i].append((j+16, genome.genes[i][j][1] + random.gauss(0, 0.3-mute_rate)))
            else:
                newGenes[i].append((j+48, random.uniform(-1, 1)))
    for i in range(48, 80):
        bias[i] = genome.bias[i] + random.gauss(0, 0.3-mute_rate)
        if i not in newGenes:
            newGenes[i] = []
        for j in range(0, 5):
            choice = random.uniform(0, 1)
            if choice <= 0.8:
                newGenes[i].append(genome.genes[i][j])
            elif choice <= 0.95+mute_rate:
                newGenes[i].append((j+80, genome.genes[i][j][1] + random.gauss(0, 0.3-mute_rate)))
            else:
                newGenes[i].append((j+80, random.uniform(-1, 1)))
    for i in range(80,85):
        bias[i] = genome.bias[i] + random.gauss(0, 0.3-mute_rate)
    return Genome(newGenes,bias)



class AITrainedControler(Controller):
    genome = {}
    def __init__(self):
        with open('bestGenome.json', mode='r') as file:
            data = json.load(file)
            self.genome = Genome({int(k): v for k, v in data['genes'].items()}, data['bias'])
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