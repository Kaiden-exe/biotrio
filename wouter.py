import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

m = [[ 0,0,0 ],
    [0,1,0],
    [0,0,0]]
    
plt.figure()
plt.matshow(m)
plt.savefig("figure.png", format="png")


# x = np.linspace(0, 20, 100)
# plt.plot(x, np.sin(x))
# plt.show()