import os
import numpy as np
import pandas as pd
import scipy.stats as stats

df_true = pd.read_csv('suvr_true.csv', header=None)
df_pet = pd.read_csv('suvr_abeta.csv', header=None)

true_arry = df_true[1].to_numpy()
pet_arry = df_pet[1].to_numpy()

true_arry[true_arry <= 1.19] = 0.0
true_arry[true_arry > 1.19] = 1.0

pet_arry[pet_arry <= 1.19] = 0.0
pet_arry[pet_arry > 1.19] = 1.0

# res = stats.ttest_ind(true_arry, pet_arry)
# res = stats.ttest_rel(true_arry, pet_arry)
# print(res.pvalue)

# res = stats.pearsonr(true_arry, pet_arry)

acc_arry = np.array(true_arry == pet_arry)
print(len(acc_arry[acc_arry]) / len(acc_arry))