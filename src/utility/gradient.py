import numpy as np
import matplotlib.pyplot as plt

def fun(x):
    return (x - 3)**2

def dfun(x):
    return 2*(x - 3)

def dfun_stoch(x):
    return 2*(x - 3) + np.random.normal()

x = np.linspace(-10,10)
plt.plot(x, fun(x))
plt.savefig("quadratic.pdf")
plt.clf()


for alpha in [0.01, 0.1, 0.6]:
    n_iterations = 100
    x = np.zeros(n_iterations)
    for t in range(n_iterations - 1):
        x[t+1] = x[t] - alpha * dfun(x[t])
    plt.plot(x)

plt.legend([0.01, 0.1, 0.6])
plt.savefig("gradient-descent.pdf")

plt.clf()
for alpha in [0.01, 0.1, 0.6]:
    n_iterations = 100
    x = np.zeros(n_iterations)
    for t in range(n_iterations - 1):
        x[t+1] = x[t] - alpha * dfun_stoch(x[t])
    plt.plot(x)


for alpha in [1]:
    x = np.zeros(n_iterations)
    for t in range(n_iterations - 1):
        x[t+1] = x[t] - (alpha/(alpha+t)) * dfun_stoch(x[t])
    plt.plot(x)

plt.legend([0.01, 0.1, 0.6, "1/t"])
plt.savefig("stochastic-gradient-descent.pdf")

    
    

