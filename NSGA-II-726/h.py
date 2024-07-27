import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
plt.barh(y= 1 , width=0.5,height=0.5, left=1, color='#FFB6C1',edgecolor='k')


plt.barh(y= 2 , width=0.5,height=0.5, left=1, color='#98FB98',edgecolor='k')
plt.barh(y= 3 , width=0.5,height=0.5, left=1, color='r',edgecolor='k')
plt.barh(y= 4 , width=0.5,height=0.5, left=1, color='y',edgecolor='k')
plt.barh(y= 5 , width=0.5,height=0.5, left=1, color='c',edgecolor='k')
plt.barh(y= 6 , width=0.5,height=0.5, left=1, color='#F4A460',edgecolor='k')
for i in range(6):
    plt.text(y=i+1, x=1.8, s="#"+str(i+1), ha='center', va='center', color='k', fontsize=13)
plt.xlim(0,7)
plt.ylim(0,7)
plt.show()
color = {0:'w',
                 1:'#FFB6C1',
                 2:'#98FB98',
                 3:'r',
                 4:'y',
                 5:'c',
                 6:'#F4A460'}