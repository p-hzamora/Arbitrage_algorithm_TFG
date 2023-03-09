import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

denom = 25000
rango = 10000000

#[print(x, '%',denom,'= ',x%denom) for x in range(rango)]

print(hash(1.1))
print(hash(4504.1))
x =[x for x in range(rango)]
y =[x%denom for x in range(rango)]
plt.plot(x,y)
print(rango% denom)
plt.show()