#操作背景
from data import Constant



class Environment():


    log_tank=[[0,0] for _ in range(len(Constant.TK))]
    #罐日志，数组下标+1=罐编号，元素为[chargeTIME,refinetime,cot1,cot2]

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