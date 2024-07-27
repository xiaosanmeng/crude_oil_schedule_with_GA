import random
from individual import Individual
from decode import decode

#0.83>1250,,,,0.38>>833,,,,,
# indi.chromosome=[8, 0, 0.83,
#                  2, 2, 1,
#                  6, 0, 0.38,
#                  0, 0, 1,
#                  4, 1, 1,
#                  3, 0, 1,
#                  9, 1, 1,
#                  4, 0, 0.38,
#                  3, 0, 0.83,
#                  5, 1, 0.83,
#                  6, 1, 0.38,
#                  2, 0, 0.38]

#调度1，改良正确
indi=Individual()
indi.chromosome=[2,0,0.83,
                 6,0,0.83,
                 1,0,0.83,
                 4,0,0.83,
                 0,0,0,
                 1,1,0.83,
                 0,0,0,
                 7,1,0.83,
                 ]
decode(indi)
print("")


from tqdm import tqdm
#0到1375,5的倍数
# def calRate(x):#------------------------新增0.00362------------------------传入一个0~1的随机数，计算对应的泵速
#     for i in range(275):
#         x-=(1/276)+(i-(276/2))*10e-7               #0.0022>>>0.00362>>0.00499
#         if(x<=0):
#             return i*5
#     return 1375
# ans=0
# for i in range(276):
#     ans+=(1/276)+(i-(276/2))*10e-6
#     print(i,ans)




# #600-1375，5的倍数,,,,,0.0064,,理想
# def calRate(x):
#     for i in range(156):
#         x-=(1/156)+(i-(156/2))*10e-6
#         if(x<=0):
#             return i*5+600
#     return 1375
def calRate(x):
    for i in range(1375):
        x-=(1/1376)+(i-(1375/2))*10e-7
        if(x<0):
            return i
print(calRate(0.83))