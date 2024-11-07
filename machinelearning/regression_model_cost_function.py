import numpy as np
import matplotlib.pyplot as plt
from lab_utils_uni import plt_intuition, plt_stationary, plt_update_onclick, soup_bowl

plt.style.use('./deeplearning.mplstyle')

x_train = np.array([1.0, 2.0])
y_train = np.array([300.0, 500.0])
plt_intuition(x_train, y_train)
