#实体类
import random


class Individual():

    def __init__(self):
        self.chromosome=[random.uniform(0, 1) for _ in range(36)]#三个一对
        # self.chromosome = [0, 0.6, 0.6869065633075293,
        #                    0.1940969132115061, 0.604937241207155, 0.67,
        #                    0.129940703596101, 0.5750842211113684, 0,
        #                    0.3, 0.88049710981939106, 0.6,
        #                    0.8874362894513197, 0.08731020561655056, 0,
        #                    0.0785895657257867, 0.83370005575377728, 0.67,
        #                    0.0713416082651152, 0.0710955519576381, 0.68,
        #                    0.01557359066837738, 0.7134992673341259, 0,
        #                    0.048581162387377, 0.2843841277290986, 0.67,
        #                    0.0542273103579516, 0.35772777807568723, 0.67]
        self.schedules_distiller = []#二维数组，存放各个蒸馏塔的炼油信息，一维数组[TANK,COT,V,START,END,RATE]
        self.schedules_pipe=[]#二维数组，存放管道调度信息：一维数组[TANK,COT,V,START,END]
        self.fitness=[99,99,99,99,50,100,24]#管道，罐底，换罐，用罐,能耗，波动/100，时间/10
        self.distance = 0  #拥挤度距离
        self.rank=0#pareto等级
        self.S=[]# 解p支配哪些解，
        self.n=0# 解p被几个解所支配
        self.feasible=False#可行性


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
