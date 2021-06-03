"""permutationTable.py"""

populationSize = [50, 100, 150, 200]
epochsNumber = [50, 100, 150, 200]
tournamentSize = [4, 8, 16, 32]
crossoverProbability = [1, 0.8, 0.6]
mutationProbability = [0.005, 0.01, 0.1]

file1 = open("output.txt", "r")
file2 = open("permutationTable.txt", "a")


for x in populationSize:
    for y in epochsNumber:
        for z in tournamentSize:
            for j in crossoverProbability:
                for k in mutationProbability:

                    file1.readline()
                    b = file1.readline()

                    file2.write(b)

                    i = 0
                    while i < 100:
                        file1.readline()

                        i += 1

