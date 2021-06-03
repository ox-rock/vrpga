import numpy as np

file1 = open("output.txt", "r")
file2 = open("mean.txt", "a")
file3 = open("std.txt", "a")

for x in range(575):

    file1.readline()
    file1.readline()
    i = 0
    temp = []
    while i < 100:
        line = float(file1.readline().strip())
        temp.append(line)
        i = i + 1

    mean = np.average(temp)
    std = np.std(temp)
    file2.write('%f' % mean)
    file3.write('%f' % std)

    file2.write('\n')
    file3.write('\n')

file1.close()
file2.close()
file3.close()
