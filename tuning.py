"""tuning.py"""
import os

populationSize = [50, 100, 150, 200]
epochsNumber = [50, 100, 150, 200]
tournamentSize = [4, 8, 16, 32]
crossoverProbability = [1, 0.8, 0.6]
mutationProbability = [0.005, 0.01, 0.1]

permutationNumber = 0
for x in populationSize:
    for y in epochsNumber:
        for z in tournamentSize:
            for j in crossoverProbability:
                for k in mutationProbability:
                    file1 = open("output.txt", "a")
                    file1.write("\n")
                    file1.write('%i' % permutationNumber)
                    file1.write(": ")
                    file1.write("Population size: {} Epochs number: {} Tournament size: {} Crossover probability: "
                                "{} Mutation Probability: {}".format(x, y, z, j, k))
                    file1.write("\n")
                    file1.close()
                    i = 0
                    while i < 100:
                        os.system("vrpga.py {} {} {} {} {} < C101.txt".format(x, y, z, j, k))
                        i += 1
                    permutationNumber += 1
