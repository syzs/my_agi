import math, copy
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('./deeplearning.mplstyle')
from lab_utils_uni import plt_house_x, plt_contour_wgrad, plt_divergence, plt_gradients

# Load our data set
x_train = np.array([1.0, 2.0])   #features
y_train = np.array([300.0, 500.0])   #target value


# Function to calculate the cost
def compute_cost(x, y, w, b):
    m = x.shape[0]
    cost = 0

    for i in range(m):
        f_wb = w * x[i] + b
        cost = cost + (f_wb - y[i]) ** 2
    total_cost = 1 / (2 * m) * cost

    return total_cost

def compute_gradient(x, y, w, b):
    """
    Computes the gradient for linear regression
    Args:
      x (ndarray (m,)): Data, m examples
      y (ndarray (m,)): target values
      w,b (scalar)    : model parameters
    Returns
      dj_dw (scalar): The gradient of the cost w.r.t. the parameters w
      dj_db (scalar): The gradient of the cost w.r.t. the parameter b
     """

    # Number of training examples
    m = x.shape[0]
    dj_dw = 0
    dj_db = 0

    for i in range(m):
        f_wb = w * x[i] + b
        dj_dw_i = (f_wb - y[i]) * x[i]
        dj_db_i = f_wb - y[i]
        dj_db += dj_db_i
        dj_dw += dj_dw_i
    dj_dw = dj_dw / m
    dj_db = dj_db / m

    return dj_dw, dj_db


if __name__ == '__main__':
    # X = np.array([[1], [2], [3], [4]])
    # w = np.array([2])
    # c = np.dot(X, w)
    # z1 = np.zeros((1,1))
    # z5 = np.zeros((1,))
    # print(z1.shape,z1,'\n', z5.shape, z5)
    #
    # print(f"X[1] has shape {X[1].shape}")
    # print(f"w has shape {w.shape}")
    # print(f"c has shape {c.shape}")

    # X_train = np.array([[2104, 5, 1, 45], [1416, 3, 2, 40], [852, 2, 1, 35]])
    # x_vec = X_train[0, :]
    # print(x_vec)

    x = np.arange(0, 20, 1)
    y = 1 + x ** 2
    X = x.reshape(-1, 1)

    save_interval = np.ceil(1000 / 10000)
    print(f"save_interval:{save_interval}")
    print(f"x.shape: {x.shape}, X.shape: {X.shape}, y.shape: {y.shape}")

    t = (np.squeeze(1000))
    print(f't:{t}')

    x = np.arange(9).reshape(1,3,3)
    print('数组 x：')
    print(x)
    print('\n')
    y = np.squeeze(x)
    print('数组 y：')
    print(y)
    print('\n')
    print('数组 x 和 y 的形状：')
    print(x.shape, y.shape)


    # initialize parameters
    initial_w = np.arange(1)
    T = X @ initial_w + 1.0
    print(f'-->X:{X}')
    print(f'-->w: {initial_w}')
    print(f'-->T:{T}, t.T:{t.T}')

    x = np.arange(0, 20, 1)
    y = x ** 2
    # engineer features .
    X = np.c_[x, x ** 2, x ** 3]

    print(f'-->X.shape:{X.shape}, x:{X}')
