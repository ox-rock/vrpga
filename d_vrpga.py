"""d_vrpga.py"""

import sys
import math
import random
from pip._vendor.distlib.compat import raw_input

# Inizializzazioni #####################################################################################################
vrp = {}
population = []
# Parametri di ingresso
populationSize = int(sys.argv[1])
epochsNumber = int(sys.argv[2])
tournamentSize = int(sys.argv[3])
crossoverProbability = float(sys.argv[4])
mutateProbability = float(sys.argv[5])


# Definizione delle funzioni e procedure ###############################################################################
# Definisce una procedura per leggere da file input txt
def readinput():
    try:
        thisLine = raw_input().strip()
        while thisLine == '' or thisLine.startswith('#'):
            thisLine = raw_input().strip()
        return thisLine
    except EOFError:
        return None


# Valuta la distanza euclidea tra due customer
def evaluateDistance(n1, n2):
    dx = n2['X'] - n1['X']
    dy = n2['Y'] - n1['Y']
    return math.sqrt(dx * dx + dy * dy)


# Valuta la fitness di un cromosoma, ovvero il costo associato al percorso totale rappresentato dal cromosoma
def evaluateFitness(chromosome):
    # Valuta inizialmente la distanza tra il deposito ed il primo customer nel percorso
    s = evaluateDistance(vrp['customers'][0], vrp['customers'][chromosome[0]])
    # Dopo di che calcola la distanza tra i customers
    for z in range(len(chromosome) - 1):
        prev = vrp['customers'][chromosome[z]]
        nextt = vrp['customers'][chromosome[z + 1]]
        s += evaluateDistance(prev, nextt)
    # L'ultima distanza è data dall'ultimo customer dell'ultimo percorso fino al deposito
    s += evaluateDistance(vrp['customers'][chromosome[len(chromosome) - 1]], vrp['customers'][0])
    return s


# Ripara un cromosoma
def repairChromosome(chromosome):
    # Ripara i cromosomi con percorsi che eccedono la capacità massima dei veicoli
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
    # Ripara i cromosomi con due depositi consecutivi
    while z >= 0:
        if chromosome[z] == 0 and chromosome[z + 1] == 0:
            del chromosome[z]
        z -= 1
    if chromosome[0] == 0:
        del chromosome[0]
    if chromosome[len(chromosome) - 1] == 0:
        del chromosome[len(chromosome) - 1]


# Selezione a torneo per selezionare i cromosomi che verranno riprodotti
def tournamentSelection():
    parentIds = set()
    # Seleziona i partecipanti del torneo
    while len(parentIds) < tournamentSize:
        parentIds |= {random.randint(0, len(population) - 1)}
    parentIds = list(parentIds)

    # I partecipanti vengono aggiunti in un array per semplificare le azioni successive
    participants = []
    for z in parentIds:
        participants.append(population[z])

    # Il for viene eseguito per ogni sottofase del torneo (ottavi di finale, quarti di finale ecc)
    for x in range(int(math.log(tournamentSize, 2)) - 1):
        winners = []
        z = 0
        while z < len(participants):
            # Singolo match
            if evaluateFitness(participants[z]) < evaluateFitness(participants[z + 1]):
                winners.append(participants[z])
            else:
                winners.append(participants[z + 1])
            z = z + 2
        participants = winners
    return winners[0], winners[1]


# Operatore di crossover tra i cromosomi vincitori dei tornei
def crossover(chromosome1, chromosome2):
    # Sceglie i due punti di cut-off
    cutIdx1, cutIdx2 = random.randint(1, min(len(chromosome1), len(chromosome2)) - 1), \
                       random.randint(1, min(len(chromosome1), len(chromosome2)) - 1)
    cutIdx1, cutIdx2 = min(cutIdx1, cutIdx2), max(cutIdx1, cutIdx2)

    # Crea due vettori (uno per cromosoma) contenenti la sequenza intermedia tra i due punti di cut-off
    n_parent1 = chromosome1[cutIdx1:cutIdx2]
    n_parent2 = chromosome2[cutIdx1:cutIdx2]

    new_parent1 = []
    new_parent2 = []

    # Definiti i due punti di taglio, il figlio 1 (risp. 2) riporta le parti esterne del genitore 1 (risp. 2);
    # i restanti geni si ottengono copiando i customer mancanti nell’ordine in cui appaiono nel genitore 2 (risp. 1)
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


# Operatore di mutazione
def mutation(chromosome):
    for z in range(len(chromosome)):
        if random.random() < mutateProbability:
            i1_2 = random.randint(0, len(chromosome) - 1)
            temp = chromosome[z]

            chromosome[z] = chromosome[i1_2]
            chromosome[i1_2] = temp
    return chromosome


# Generazione della popolazione iniziale
def generateInitialPopulation():
    # Genera un cromosoma fino al raggiungimento della dimensione scelta per la popolazione
    for x in range(populationSize):
        chromosome = list(range(1, len(vrp['customers'])))
        # Mischia la lista
        random.shuffle(chromosome)
        # Ripara il cromosoma
        repairChromosome(chromosome)
        # Aggiunge il cromosoma alla popolazione iniziale
        population.append(chromosome)


# Funzione per la lettura del file input txt
line = readinput()
while line.lower() != 'customers:':
    inputs = line.split()
    if inputs[0].lower() == 'capacity':
        vrp['capacity'] = int(inputs[1])
    line = readinput()

# Funzione per la lettura del file input txt
line = readinput()
vrp['customers'] = [{'N': 0, 'X': 0, 'Y': 0, 'demand': 0}]
while line is not None:
    inputs = line.split()
    customer = {'N': inputs[0], 'X': int(inputs[1]), 'Y': int(inputs[2]), 'demand': int(inputs[3])}
    vrp['customers'].append(customer)
    line = readinput()


# Main #################################################################################################################
generateInitialPopulation()
# Il ciclo si ripete per il numero di epoche specificato in ingresso
for i in range(epochsNumber):
    newPopulation = []

    print('POPOLAZIONE ', i, '##########################')
    for k in range(len(population)):
        print(population[k], ': ', evaluateFitness(population[k]))

    # Ognuna delle iterazioni genererà due cromosomi. Per garantire che la popolazione rimanga inalterata in numero
    # il numero di iterazioni sarà pari la metà della grandezza della popolazione
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

# Seleziona il miglior cromosoma, ovvero la soluzione finale
better = None
bf = float('inf')
for p in population:
    f = evaluateFitness(p)
    if f < bf:
        bf = f
        better = p

# Stampa la soluzione finale
print("\n")
print('Route 1 : ', end='')
k = 2
for nodeIdx in better:
    if vrp['customers'][nodeIdx]['N'] == 0:
        print('\nRoute', k, ': ', end="")
        k += 1
    else:
        print(vrp['customers'][nodeIdx]['N'], end=' ')

print('\n\nFitness: ', end='')
print('%f' % bf)
