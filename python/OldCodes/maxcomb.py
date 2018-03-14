from math import *
import matplotlib.pyplot as plt
def maxComb(n):

    npart = 3
    ncomb = factorial(n)/(factorial(npart)*factorial(n-npart))
    return ncomb


y = []
x = []
for i in range(3,15):
    y.append(maxComb(i))
    x.append(i)
plt.plot(x,y,linewidth=4)
plt.axvline(x=6,linewidth=4, color='r')
plt.ylabel('Number of combinations')
plt.xlabel('Number of AK-4 jets')

plt.show()


