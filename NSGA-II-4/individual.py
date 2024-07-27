#实体类
import random
from constant import Constant

class Individual():

    def __init__(self):
        self.chromosome=[random.randint(0,len(Constant.TK)-1) if i%3==0
                         else (random.randint(0, len(Constant.RT)-1) if i%3==1
                               else random.uniform(0.3, 1))for i in range(42)]#三个一对
        # self.chromosome = [8, 0, 2, 2, 2, 3, 6, 0, 1, 0, 0, 3, 4, 1, 3, 3, 0, 3, 9, 1, 3, 4, 0, 1, 3, 0, 2, 5, 1, 2, 6, 1, 1, 2, 0, 1]
        self.schedules_distiller = []#二维数组，存放各个蒸馏塔的炼油信息，一维数组[TANK,COT,V,START,END,RATE]
        self.schedules_pipe=[]#二维数组，存放管道调度信息：一维数组[TANK,COT,V,START,END,RATE_1,RATE_2]
        self.fitness=[99,99,99,99,5000,5000]#管道，罐底，换罐，用罐,能耗，波动/100
        self.distance = 0  #拥挤度距离
        self.rank=0#pareto等级
        self.S=[]# 解p支配哪些解，
        self.n=0# 解p被几个解所支配
        self.feasible=False#可行性
        self.rate_list=[]#管道泵速求解结果


    def __lt__(self, other):
        #判断v1是否支配v2，支配返回1
        v1 = self.fitness
        v2 = other.fitness
        if(v1==v2):
            return 0
        i=0
        while(i<len(v1)):

            if(v1[i]<=v2[i]):
                i+=1
            else:
                return 0
        return 1

