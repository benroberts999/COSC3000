#!/usr/bin/env python3
import numpy as np
from matplotlib import pyplot as plt

x = np.linspace(-np.pi, np.pi, 500)

y1 = np.sin(x)
y2 = np.cos(x)
y3 = np.log(np.abs(x))

print(x)

plt.title("Data")
plt.xlabel("x")
plt.ylabel("y")
plt.ylim(-3.0, 3.0)
plt.plot(x, y1, "b-")
plt.plot(x, y2, "r-")
plt.plot(x, y3, "g-")

plt.show()

# plt.close()
# plt.clf()

fig, axs = plt.subplots(nrows=3, ncols=1)

axs[0].set_title("sin(x)")
axs[0].set_xlabel("x")
axs[0].set_ylabel("y")
axs[0].plot(x, y1, "b-")
axs[0].set_ylim(-2, 2)

axs[1].set_title("cos(x)")
axs[1].set_xlabel("x")
axs[1].set_ylabel("y")
axs[1].plot(x, y2, "r-")
axs[1].set_ylim(-2, 2)

axs[2].set_title("abs(x)")
axs[2].set_xlabel("x")
axs[2].set_ylabel("y")
axs[2].plot(x, y3, "g-")
axs[2].set_ylim(-2, 2)

plt.show()
