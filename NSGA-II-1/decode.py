#解码
import math

from environment import Environment
from individual import Individual
from data import Constant


def update_schduleOfpipe(tank,distiller,rateIndex,schedules_pipe,environment:Environment,constant:Constant):
    #计算出管道的运输信息，返回计划=[TANK,COT,V,START,END],tank,distiller为编号
    # tank=[编号，类型，容量，存量]  RT=[编号，炼油类型，炼油量,炼油类型，炼油量]
    #方法返回值为endtime
    # 计算开始时间
    if (len(schedules_pipe) != 0):  # 如果不为空，求出上一个管道运输信息[TANK,COT,V,START,END]
        startTime = schedules_pipe[-1][4]  # -1可定位到最后一个元素
    else:
        startTime = 0
    rate=constant.RATE[rateIndex]
    #停运&不停运
    if rate!=0:#非停运操作
        #计算转运体积&类型，分两种情况：炼油类型1＆2
        if(environment.RT[distiller-1][2]!=0):#炼油任务1未完成
            volume=environment.TK[tank-1][2] if environment.RT[distiller-1][2]>environment.TK[tank-1][2] else environment.RT[distiller-1][2]
            cot=environment.RT[distiller-1][1]

        else:
            volume=environment.TK[tank-1][2] if environment.RT[distiller-1][4]>environment.TK[tank-1][2] else environment.RT[distiller-1][4]
            cot=environment.RT[distiller-1][3]
        if(volume!=0):
            #得出计划i
            schdule=[tank,cot,volume,startTime,startTime+volume/rate,rate]
            schedules_pipe.append(schdule)
            #更新time_ODT
            environment.time_ODT=startTime+volume/rate
            #充油
            environment.TK[tank-1][1]=cot
            environment.TK[tank-1][3]=volume
            environment.log_tank[tank-1][0]=startTime+volume/rate+constant.RESIDENCE_TIME
    else:#停运
        #两种情况：endtime_a and endTime_b
        urge_time=min(environment.time_ODF)
        urge_distiller=environment.time_ODF.index(urge_time)#
        endTime_b =endTime_a= 240
        if(len(environment.emptyTK)!=0):

            mintank_v=min( tank[2] for tank in environment.emptyTK)
            endTime_a=urge_time-mintank_v/1250-constant.RESIDENCE_TIME
        for i in range(len(environment.TK)):
            if(environment.TK[i][3]==0 and environment.log_tank[i][1]<endTime_b and environment.log_tank[i][1]>startTime):#存量为0
                endTime_b = environment.log_tank[i][1]
        endTime=min(endTime_a,endTime_b)
        if(endTime<startTime):
            endTime=startTime
        schdule = [0, 0, 0, startTime, endTime, rate]
        schedules_pipe.append(schdule)
        # 更新time_ODT
        environment.time_ODT =endTime



def update_schduleOfdistiller(schedules_distiller,environment:Environment,constant: Constant):
    #炼油开始，schedules_distiller=[[],[],[]],子计划为[TANK,COT,V,START,END]
    # tank=[编号，类型，容量，存量],#RT/distiller=[编号，炼油类型，炼油量,炼油类型，炼油量]
    for distiller in environment.undoneRT:#对每个为完成的蒸馏塔进行炼油
        distillerNum=distiller[0]#蒸馏塔编号
        #先完成炼油类型1，再完成炼油类型2
        if(distiller[2]!=0):#类型1还未完成
            for tank in environment.TK:#对每个罐进行搜索
                tankNum = tank[0]
                if(tank[1]==distiller[1] and environment.log_tank[tankNum-1][0]<=environment.time_ODF[distillerNum-1] and distiller[2]!=0):
                    #类型相同，并且可用(chargetime时间已过，充油完成
                    cot=distiller[1]#炼油类型
                    volume_refine=tank[3]#炼油量
                    startTime=schedules_distiller[distillerNum-1][-1][4] if(len(schedules_distiller[distillerNum-1])!=0) else 0
                    endTime=startTime+volume_refine/constant.F_SDU[distillerNum-1]#炼油量/炼油速率
                    schedule=[tankNum,cot,volume_refine,startTime,endTime]#炼油计划
                    schedules_distiller[distillerNum-1].append(schedule)#加入总计划
                    #TIME_ODF的变化：
                    environment.time_ODF[distillerNum - 1]=endTime
                    #refine
                    #tk的变化
                    environment.log_tank[tankNum-1].append(cot)
                    environment.TK[tankNum-1][3]-=volume_refine#存量更新
                    if environment.TK[tankNum-1][3]==0:
                        environment.TK[tankNum-1][1]=0 #如果存量为0，类型置零
                    environment.log_tank[tankNum-1][1]=endTime#refine time更新
                    #RT的变化
                    environment.RT[distillerNum-1][2]-=volume_refine#RT蒸馏量更新


        if(distiller[4]!=0 and distiller[2]==0):#炼油类型2
            for tank in environment.TK:#对每个罐进行搜索
                tankNum=tank[0]
                if(tank[1]==distiller[3] and environment.log_tank[tankNum-1][0]<=environment.time_ODF[distillerNum-1] and distiller[4]!=0):#类型相同
                    cot=distiller[3]#炼油类型
                    volume_refine=tank[3]#炼油量
                    startTime=schedules_distiller[distillerNum-1][-1][4] if(len(schedules_distiller[distillerNum-1])!=0) else 0
                    endTime=startTime+volume_refine/constant.F_SDU[distillerNum-1]#炼油量/炼油速率
                    tankNum=tank[0]
                    schedule=[tankNum,cot,volume_refine,startTime,endTime]#炼油计划
                    schedules_distiller[distillerNum-1].append(schedule)#加入总计划
                    # TIME_ODF的变化：
                    environment.time_ODF[distillerNum - 1] = endTime
                    #refine
                    #tk的变化
                    environment.log_tank[tankNum-1].append(cot)
                    environment.TK[tankNum-1][3]-=volume_refine#存量更新
                    if environment.TK[tankNum-1][3]==0:
                        environment.TK[tankNum-1][1]=0 #如果存量为0，类型置零
                    environment.log_tank[tankNum-1][1]=endTime#refine time更新
                    #RT的变化
                    environment.RT[distillerNum-1][4]-=volume_refine#RT蒸馏量更新

def decode(individual: Individual):
    chromosome=individual.chromosome
    constant=Constant()#常量（实例
    environment=Environment(constant)#环境
    length= len(individual.chromosome)/3#染色体解组
    index=0#染色体定位
    schedules_pipe=[]#二维数组，存放管道调度信息：一维数组[TANK,COT,V,START,END,RATE]
    schedules_distiller=[[],[],[]]#二维数组，存放各个蒸馏塔的炼油信息，一维数组[TANK,COT,V,START,END]
    # 更新emptyTK和undoneRT
    environment.update_undoneRT(environment.RT)
    environment.update_emptyTK(environment.TK)
    while(index<length and len(environment.undoneRT)>0):

        if(len(environment.emptyTK)!=0):
            #根据染色体求出下标
            tankIndex=math.floor(chromosome[index*3+0]*len(environment.emptyTK))
            distillerIndex=math.floor(chromosome[index*3+1]*len(environment.undoneRT))
            rateIndex=math.floor(chromosome[index*3+2]*len(Constant.RATE))
            #根据下标求出需要的TK,DS编号
            tank=environment.emptyTK[tankIndex][0]#tank=[编号，类型，容量，存量]
            distiller=environment.undoneRT[distillerIndex][0]#RT=[编号，炼油类型，炼油量,炼油类型，炼油量]
        else:
            tank=distiller=rateIndex=0
        #更新ODF,炼油(预调度
        update_schduleOfdistiller(schedules_distiller,environment,constant)
        #更新ODT
        update_schduleOfpipe(tank,distiller,rateIndex,schedules_pipe,environment,constant)
        #更新emptyTK和undoneRT
        environment.update_undoneRT(environment.RT)
        environment.update_emptyTK(environment.TK)
        index+=1

    if(len(environment.undoneRT)==0):
        individual.feasible=True
        individual.fitness=[0,0,0,0,0,0,0]
        # #后续基因清空：
        # individual.chromosome=individual.chromosome[0:index*3]
        individual.schedules_pipe=schedules_pipe
        individual.schedules_distiller=schedules_distiller
        ##分别求：管道，罐底，换罐，用罐,能耗，波动，时间=fitness
        #管道[TANK,COT,V,START,END,RATE]
        cot_list=[]
        for i in range(len(individual.schedules_pipe)):
            if(individual.schedules_pipe[i][1]!=0):
                cot_list.append(individual.schedules_pipe[i][1])
        for i in range(len(cot_list)-1):
            pipe_cot_x=cot_list[i]
            pipe_cot_y=cot_list[i+1]
            individual.fitness[0]+=constant.Mp[pipe_cot_x-1][pipe_cot_y-1]
        #罐底混合,log_i为【cot1,cot2.....]
        for i in range(len(environment.log_tank)):
            log_i=environment.log_tank[i]
            for index in range(len(log_i)-3):
                individual.fitness[1]+=constant.Mt[log_i[2+index]-1][log_i[3+index]-1]
        #换罐，schedules_distiller=[[],[],[]] ，二维数组为各个蒸馏塔的炼油信息,一维数组[TANK,COT,V,START,END]
        for i in range(len(schedules_distiller)):
            individual.fitness[2]+=len(schedules_distiller[i])
        #用罐,log_i为【cot1,cot2.....]
        for i in range(len(environment.log_tank)):
            log_i=environment.log_tank[i]
            if(len(log_i)!=2):
                individual.fitness[3]+=1
        #能耗,管道[TANK,COT,V,START,END,RATE]
        for i in range(len(individual.schedules_pipe)):
            rate=individual.schedules_pipe[i][5]#RATE取值=[0,833.3,1250,1375]
            energy_consumption=0
            if(rate>0):
                energy_consumption=1
            if(rate>833.3):
                energy_consumption=2
            if(rate>1250):
                energy_consumption=3
            individual.fitness[4]+=energy_consumption
        #波动，管道[TANK,COT,V,START,END,RATE]
        for i in range(len(individual.schedules_pipe) - 1):
            rate_x=individual.schedules_pipe[i][5]#RATE取值=[0,833.3,1250,1375]
            rate_y=individual.schedules_pipe[i+1][5]#RATE取值=[0,833.3,1250,1375]
            individual.fitness[5]+=math.sqrt((rate_x-rate_y)**2)
        individual.fitness[5]*=0.01

        #结束时间
        individual.fitness[6]=individual.schedules_pipe[len(individual.schedules_pipe)-1][4]
        individual.fitness[6]*=0.1

