"""vrpga.py"""

import sys
import math
import random
from pip._vendor.distlib.compat import raw_input


vrp = {}
population = []
populationSize = int(sys.argv[1])
epochsNumber = int(sys.argv[2])
tournamentSize = int(sys.argv[3])
crossoverProbability = float(sys.argv[4])
mutateProbability = float(sys.argv[5])


def readinput():
    try:
        thisLine = raw_input().strip()
        while thisLine == '' or thisLine.startswith('#'):
            thisLine = raw_input().strip()
        return thisLine
    except EOFError:
        return None


def evaluateDistance(n1, n2):
    dx = n2['X'] - n1['X']
    dy = n2['Y'] - n1['Y']
    return math.sqrt(dx * dx + dy * dy)


def evaluateFitness(chromosome):
    s = evaluateDistance(vrp['customers'][0], vrp['customers'][chromosome[0]])
    for z in range(len(chromosome) - 1):
        prev = vrp['customers'][chromosome[z]]
        nextt = vrp['customers'][chromosome[z + 1]]
        s += evaluateDistance(prev, nextt)
    s += evaluateDistance(vrp['customers'][chromosome[len(chromosome) - 1]], vrp['customers'][0])
    return s


def repairChromosome(chromosome):
    z = 0
    s = 0.0
    cap = vrp['capacity']
    while z < len(chromosome):
        s += vrp['customers'][chromosome[z]]['demand']
        if s > cap:
            chromosome.insert(z, 0)
            s = 0.0
        z += 1
    z = len(chromosome) - 2
    while z >= 0:
        if chromosome[z] == 0 and chromosome[z + 1] == 0:
            del chromosome[z]
        z -= 1
    if chromosome[0] == 0:
        del chromosome[0]
    if chromosome[len(chromosome) - 1] == 0:
        del chromosome[len(chromosome) - 1]


def tournamentSelection():
    parentIds = set()
    while len(parentIds) < tournamentSize:
        parentIds |= {random.randint(0, len(population) - 1)}
    parentIds = list(parentIds)

    participants = []
    for z in parentIds:
        participants.append(population[z])

    for x in range(int(math.log(tournamentSize, 2)) - 1):
        winners = []
        z = 0
        while z < len(participants):
            if evaluateFitness(participants[z]) < evaluateFitness(participants[z + 1]):
                winners.append(participants[z])
            else:
                winners.append(participants[z + 1])
            z = z + 2
        participants = winners
    return winners[0], winners[1]


def crossover(chromosome1, chromosome2):
    cutIdx1, cutIdx2 = random.randint(1, min(len(chromosome1), len(chromosome2)) - 1), \
                       random.randint(1, min(len(chromosome1), len(chromosome2)) - 1)
    cutIdx1, cutIdx2 = min(cutIdx1, cutIdx2), max(cutIdx1, cutIdx2)

    n_parent1 = chromosome1[cutIdx1:cutIdx2]
    n_parent2 = chromosome2[cutIdx1:cutIdx2]

    new_parent1 = []
    new_parent2 = []

    for z in range(len(chromosome2)):
        for x in n_parent1:
            if chromosome2[z] == x:
                new_parent1.append(chromosome2[z])
                n_parent1.remove(x)
                break

    for z in range(len(chromosome1)):
        for x in n_parent2:
            if chromosome1[z] == x:
                new_parent2.append(chromosome1[z])
                n_parent2.remove(x)
                break

    new_chromosome1 = chromosome1[:cutIdx1] + new_parent1 + chromosome1[cutIdx2:]
    new_chromosome2 = chromosome2[:cutIdx1] + new_parent2 + chromosome2[cutIdx2:]

    return new_chromosome1, new_chromosome2


def mutation(chromod_vsome):
    for z in range(len(chromosome)):
        if random.random() < mutateProbability:
            i1_2 = random.randint(0, len(chromosome) - 1)
            temp = chromosome[z]

            chromosome[z] = chromosome[i1_2]
            chromosome[i1_2] = temp
    return chromosome


def generateInitialPopulation():
    for x in range(populationSize):
        chromosome = list(range(1, len(vrp['customers'])))
        random.shuffle(chromosome)
        repairChromosome(chromosome)
        population.append(chromosome)


line = readinput()
while line.lower() != 'customers:':
    inputs = line.split()
    if inputs[0].lower() == 'capacity':
        vrp['capacity'] = int(inputs[1])
    line = readinput()


line = readinput()
vrp['customers'] = [{'N': 0, 'X': 0, 'Y': 0, 'demand': 0}]
while line is not None:
    inputs = line.split()
    customer = {'N': inputs[0], 'X': int(inputs[1]), 'Y': int(inputs[2]), 'demand': int(inputs[3])}
    vrp['customers'].append(customer)
    line = readinput()


generateInitialPopulation()
for i in range(epochsNumber):
    newPopulation = []

    for j in range(int(len(population) / 2)):

        parent1, parent2 = tournamentSelection()
        if random.random() < crossoverProbability:
            child1, child2 = crossover(parent1, parent2)
        else:
            child1, child2 = parent1, parent2

        child1 = mutation(child1)
        repairChromosome(child1)
        child2 = mutation(child2)
        repairChromosome(child2)
        newPopulation += [child1, child2]

    population = newPopulation


better = None
bf = float('inf')
for p in population:
    f = evaluateFitness(p)
    if f < bf:
        bf = f
        better = p


file1 = open("output.txt", "a")
file1.write('%f' % bf)
file1.write("\n")
file1.close()
