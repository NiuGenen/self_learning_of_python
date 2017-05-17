#python3.6
#numpy-1.13
#scipy-0.19
#matplotlib-2.0.2
#an example from Internet
import numpy as np
import matplotlib.pyplot as plt

'''
plt.figure(1)  # 创建图表1
plt.figure(2)  # 创建图表2
ax1 = plt.subplot(211)  # 在图表2中创建子图1
ax2 = plt.subplot(212)  # 在图表2中创建子图2

x = np.linspace(0, 3, 100)
for i in range(0,5):
    plt.figure(1)  # ❶ # 选择图表1
    plt.plot(x, np.exp(i * x / 3))
    plt.sca(ax1)  # ❷ # 选择图表2的子图1
    plt.plot(x, np.sin(i * x))
    plt.sca(ax2)  # 选择图表2的子图2
    plt.plot(x, np.cos(i * x))

plt.show()
'''
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D #<-- Note the capitalization!
fig = plt.figure()

ax = Axes3D(fig) #<-- Note the difference from your original code...

X, Y, Z = axes3d.get_test_data(0.05)
#print(Z)
#cset = ax.contour(X, Y, Z, 16, extend3d=True)
#ax.clabel(cset, fontsize=9, inline=1)
ax.bar3d([1,2,3],[4,5,6],[7,8,9],[.5,1,2],[.5,1,2],[.5,1,2])
plt.show()