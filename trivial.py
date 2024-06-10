import os
import shutil
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

abeta_ls_159 = []
abeta_ls_adni = []
d = dict()

with open('/data/hohokam/Yanxi/Data/mri2pet/adni/data_split.csv') as f:
    for line in f:
        linelist = line.split('\n')[0].split(',')
        abeta_ls_adni.append(float(linelist[5]))
        d[linelist[0]] = float(linelist[5])

with open('/data/hohokam/Yanxi/Data/mri2pet/adni/mapping1.csv') as f:
    for line in f:
        linelist = line.split('\n')[0].split(',')
        abeta_ls_159.append(d[linelist[0]])

print(len(abeta_ls_159))
print(len(abeta_ls_adni))

abeta_arry_159 = np.array(abeta_ls_159)
abeta_arry_adni = np.array(abeta_ls_adni)
fig, axs = plt.subplots(1, 2, sharey=True, tight_layout=True)

axs[0].hist(abeta_arry_159, bins=5)
axs[1].hist(abeta_arry_adni, bins=5)

plt.show()
plt.savefig('hist.png')