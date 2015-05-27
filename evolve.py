import numpy as np
import pandas as pd
import tournament_1player_ver

import matplotlib.pyplot as plt

def fitness(parameter = None):
    reload(tournament_1player_ver)
    r =  tournament_1player_ver.fitness(parameter)
    plt.close()
    return r
step = 30
loop = 3
x = np.linspace(0.1, 0.7, step)
results = []
for i in xrange(loop):
    r = []
    for j in x:
        f = fitness(dict(
            caution_dist = j
        ))
        print f
        r.append(f)
    results.append(r)
results = pd.DataFrame(results)
print results
print results.mean(),  results.std()
plt.close()
fig = plt.axes()
fig.errorbar(x,results.mean(), yerr = results.std())
plt.show()