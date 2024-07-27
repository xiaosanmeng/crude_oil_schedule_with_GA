#操作背景
from data import Constant



class Environment():


    log_tank=[[0,0] for _ in range(len(Constant.TK))]
    #罐日志，数组下标+1=罐编号，元素为[chargeTIME,refinetime,cot1,cot2]
    SecureState=True
    time_ODT = 0
    time_ODF = [0, 0, 0]
    def __init__(self,constant):
        self.TK = constant.TK
        self.RT = constant.RT
        self.log_tank=[[0,0] for _ in range(len(Constant.TK))]
        self.emptyTK=self.update_emptyTK(self.TK)
        self.undoneRT=self.update_undoneRT(self.RT)

    def update_emptyTK(self,TK):#更新空罐列表
        self.emptyTK=[]
        for i in range(len(TK)):
            if(TK[i][3]==0 and self.log_tank[i][1]<=self.time_ODT):
                self.emptyTK.append(TK[i])

        return self.emptyTK

    def update_undoneRT(self,RT):#更新为完成计划
        self.undoneRT=[]
        for i in range(len(RT)):
            if(RT[i][2]!=0 or RT[i][4]!=0):
                self.undoneRT.append(RT[i])

        return self.undoneRT

    def isSecureState(self):
        # 判断是否为安全状态
        # # TKi=[编号，类型，容量，存量],RTi=[编号，炼油类型，炼油量,炼油类型，炼油量]
        for distiller in self.undoneRT:
            distiller_num=distiller[0]-1#编号-1=下标
            desired_COT = self.RT[distiller_num][1] if self.RT[distiller_num][2] != 0 \
                else self.RT[distiller_num][3]  # 所需类型
            #情况A：用适配的TK可供使用
            available_time = 240#可用罐时间
            for tank in self.TK:
                if (tank[1] == desired_COT and tank[3] != 0
                        and self.log_tank[tank[0] - 1][0] < available_time):
                    available_time = self.log_tank[tank[0] - 1][0]
            #情况B：无适配的TK，须调度
            if(available_time==240 ):
                if(len(self.emptyTK)!=0):
                    min_Va = min(tank[2] for tank in self.emptyTK)
                    min_Vb = self.RT[distiller_num][2] if self.RT[distiller_num][2] != 0 \
                        else self.RT[distiller_num][4]
                    if (self.time_ODT + min(min_Va, min_Vb) / 1375 + Constant.RESIDENCE_TIME > self.time_ODF[distiller_num]):
                        self.SecureState = False
                else:
                    self.SecureState=False