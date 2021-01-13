import matplotlib.pyplot as plt
import numpy as np
import matplotlib as mpl

m = [[ 0,0,0 ],
    [0,1,0],
    [0,0,0]]
    
test = {1: [0,0], 2: [1,0], 3: [2,0], 4: [2,1], 5: [2,2], 6: [-1,-1]}
data = {"x":[], "y":[], "label":[]}
for label, coord in test.items():
    data["x"].append(coord[0])
    data["y"].append(coord[1])
    data["label"].append(label)

plt.figure()
# plt.matshow(m)
plt.scatter(data["x"], data["y"], marker = 'o')
plt.savefig("figure.png", format="png")


# x = np.linspace(0, 20, 100)
# plt.plot(x, np.sin(x))
# plt.show()


