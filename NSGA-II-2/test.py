#测试
import math
import random

from individual import Individual
from decode import decode
count=0
indi=Individual()
indi.chromosome=[8, 0, 2, 2, 2, 3, 6, 0, 1, 0, 0, 3, 4, 1, 3, 3, 0, 3, 9, 1, 3, 4, 0, 1, 3, 0, 2, 5, 1, 2, 6, 1, 1, 2, 0, 1]
decode(indi)
print(indi.schedules_pipe)
for i in range(len(indi.schedules_pipe)):
    start=indi.schedules_pipe[i][3]
    end=indi.schedules_pipe[i][4]
    print(end-start)

print(indi.fitness)