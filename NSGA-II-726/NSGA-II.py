import math
from collections import defaultdict
import random
import matplotlib.pyplot as plt
from time import time
from tqdm import tqdm


from individual import Individual



def main():
    generations = 200 # 迭代次数
    popnum = 200 # 种群大小
    factor_c=0.8 #交叉概率
    factor_m=0.1 #变异概率
    # 随机生成第一代种群，并解码
    P = []
    # 创建种群，每个个体都是一个实体类Individual,该实体类有相应的解码函数decode
    for i in range(popnum):
        individual=Individual()
        individual.decode()
        P.append(individual)
    # 非支配排序
    fast_non_dominated_sort(P)
    # 生成新种群Q，并解码
    Q = make_new_pop(P,0,generations,factor_c,factor_m)
    for indi in Q:
        indi.decode()
    P_t = P  # 当前这一届的父代种群
    Q_t = Q  # 当前这一届的子代种群
    # 迭代开始
    for gen_cur in tqdm(range(generations)):
        R_t = P_t + Q_t #合并两个种群
        F = fast_non_dominated_sort(R_t) #非支配排序
        P_n = []  # 即为P_t+1,表示下一届的父代
        i = 1
        while len(P_n) + len(F[i]) < popnum:
            crowding_distance_assignment(F[i]) #计算拥挤距离
            P_n = P_n + F[i]
            i = i + 1
        # 到达临界层
        F[i].sort(key=lambda x: x.distance)  # 按拥挤距离排序
        P_n = P_n + F[i][:popnum - len(P_n)]  # 填充种群，直到数量到达popnum
        Q_n = make_new_pop(P_n,gen_cur,generations,factor_c,factor_m)
        # 求得下一届的父代和子代成为当前届的父代和子代，，进入下一次迭代 《=》 t = t + 1
        P_t = P_n
        Q_t = Q_n
        for indi in P_t:
            indi.decode() # 对每个个体进行解码
        for indi in Q_t:
            indi.decode() # 对每个个体进行解码
        # 绘图
        plt.clf()
        plt.title('current generation:' + str(gen_cur + 1))
        plot_P(P_t)
        plt.pause(0.1)
    plt.show()
    for indi in P_t:
        if(indi.rank==1):
            print(indi.fitness,indi.chromosome)
    return 0

def fast_non_dominated_sort(P):
    """
    非支配排序
    :param P: 种群 P
    :return F: F=(F_1, F_2, ...) 将种群 P 分为了不同的层，
    返回值类型是dict，键为层号，值为 List 类型，存放着该层的个体
    """
    F = defaultdict(list)

    for p in P:
        p.S = []
        p.n = 0
        for q in P:
            if p < q:  # if p dominate q
                p.S.append(q)  # Add q to the set of solutions dominated by p
            elif q < p:
                p.n += 1  # Increment the domination cofunter of p
        if p.n == 0:
            p.rank = 1
            F[1].append(p)

    i = 1
    while F[i]:
        Q = []
        for p in F[i]:  # 遍历每个pareto层的每个解
            for q in p.S:
                q.n = q.n - 1
                if q.n == 0:
                    q.rank = i + 1
                    Q.append(q)
        i = i + 1
        F[i] = Q



    return F
def crowding_distance_assignment(L):
    # 传进来的参数为，某一pareto层,类型为list
    for i in range(len(L[0].fitness)):#遍历每个方向
        max_fitness=max(individual.fitness[i] for individual in L)# 该方向的最大最小值
        min_fitness=min(individual.fitness[i] for individual in L)
        if(max_fitness==min_fitness):
            continue
        for ind_self in L:
            for ind_other in L:
                ind_self.distance+=abs(ind_self.fitness[i]-ind_other.fitness[i])/max_fitness-min_fitness

def binary_tournament(ind1, ind2):
    """
    二元锦标赛
    :param ind1:个体1号
    :param ind2: 个体2号
    :return:返回较优的个体
    """
    if ind1.rank != ind2.rank:  # 如果两个个体有支配关系，即在两个不同的rank中，选择rank小的
        return ind1 if ind1.rank < ind2.rank else ind2
    elif ind1.distance != ind2.distance:  # 如果两个个体rank相同，比较拥挤度距离，选择拥挤读距离大的
        return ind1 if ind1.distance > ind2.distance else ind2
    else:  # 如果rank和拥挤度都相同，返回任意一个都可以
        return ind1


def crossover_mutation(parent1, parent2,factor_c,factor_m):
    """

    """
    offspring1 = Individual()
    offspring2 = Individual()
    chromosome_length=len(parent1.chromosome)
    r = random.uniform(0, 1)
    p = r * chromosome_length  # crossover position
    if random.uniform(0,1)<factor_c:
        for i in range(chromosome_length):
            # 交叉
            offspring1.chromosome[i]=parent2.chromosome[i] if i<p else offspring1.chromosome[i]
            offspring2.chromosome[i]=parent1.chromosome[i] if i<p else offspring2.chromosome[i]

    for i in range(chromosome_length):
        if random.uniform(0,1)<factor_m:
            offspring1.chromosome[i]=random.randint(0,offspring1.env.n_actions-1)
            offspring2.chromosome[i]=random.randint(0,offspring2.env.n_actions-1)

    return [offspring1, offspring2]

def make_new_pop(P,gen_cur,gen_max,factor_c,factor_m):
    """
    use select,crossover and mutation to create a new population Q
    :param P: 父代种群
    :return Q : 子代种群
    """
    popnum = len(P)
    Q = []
    # binary tournament selection
    for i in range(int(popnum / 2)):
        # 从种群中随机选择两个个体，进行二元锦标赛，选择出一个 parent1
        i = random.randint(0, popnum - 1)
        j = random.randint(0, popnum - 1)
        parent1 = binary_tournament(P[i], P[j])

        # 从种群中随机选择两个个体，进行二元锦标赛，选择出一个 parent2
        i = random.randint(0, popnum - 1)
        j = random.randint(0, popnum - 1)
        parent2 = binary_tournament(P[i], P[j])

        while (parent1.chromosome == parent2.chromosome):  # 如果选择到的两个父代完全一样，则重选另一个
            i = random.randint(0, popnum - 1)
            j = random.randint(0, popnum - 1)
            parent2 = binary_tournament(P[i], P[j])

        # parent1 和 parent1 进行交叉，变异 产生 2 个子代
        Two_offspring = crossover_mutation(parent1, parent2,factor_c,factor_m)

        # 产生的子代进入子代种群
        Q.append(Two_offspring[0])
        Q.append(Two_offspring[1])
    return Q
def plot_P(P):
    X=[1,2,3,4,5]


    plt.xlabel('optim')
    plt.ylabel('FITNESS')
    for i in  range(len(P)):
        if(P[i].rank==1):
            P[i].fitness[4]/=10
            plt.plot(X, P[i].fitness)

if __name__ == '__main__':
    start = time()
    print("程序开始,迭代进化..")
    main()
    print("迭代完毕..")
    end = time()
    print("程序执行时间为:%ds" % (end - start))