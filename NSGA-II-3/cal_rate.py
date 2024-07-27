import numpy as np


import random


class Rate_indi():
    def __init__(self):
        k1 = round(random.uniform(0, 1),2)
        k2 = round(random.uniform(0, 1 - k1),2)
        self.chromosomes= [k1, k2]
        self.fitness=999
        self.ans=[]

def decode(rate,indi:Rate_indi,time):

    A = np.array([
        [1.5, 1.65],
        [-0.5, -0.65],
    ])
    # 常数向量b
    b = np.array([rate/833.3, 1 - (rate/833.3)])
    # 求解方程组
    ans = np.linalg.solve(A, b)
    especial_solu=[0,0,ans[0],ans[1]]

    generals_solu_1=np.array([1,0,-11,10])
    generals_solu_2=np.array([0,1,-4.33,3.33])
    ans=indi.chromosomes[0]*generals_solu_1+indi.chromosomes[1]*generals_solu_2+especial_solu
    if(ans[0]>=0 and ans[1]>=0 and ans[2]>=0 and ans[3]>=0):
        indi.ans=ans
        indi.fitness=time*ans[1]*1+time*ans[2]*2+time*ans[3]*3
    return

def cal_rate(rate,time):
    rate_dict={0:[0,0,0,0],
               1375:[0,0,0,1]}
    if(rate==0 or rate==1375):
        indi=Rate_indi()
        indi.ans=[0,0,0,rate/1375]
        indi.fitness=(rate/1375)*time*3
        return indi

    for i in range(10000):
        # 遗传算法参数
        population_size = 30
        # 初始化种群
        P = []
        for i in range(population_size):
            indi = Rate_indi()
            decode(rate, indi, time)
            P.append(indi)
        P = sorted(P, key=lambda x: x.fitness)
        if(P[0].fitness!=999):
            return P[0]

