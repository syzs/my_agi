import numpy as np
import matplotlib.pyplot as plt

plt.style.use('./deeplearning.mplstyle')

x_train = np.array([1.0, 2.0])
y_train = np.array([300.0, 500.0])
print(f"x_train = {x_train}")
print(f'y_train = {y_train}')
print(f"x_train.shape: {x_train.shape}")

m = x_train.shape[0]
print(f"number of training example is: {m}")
m = len(x_train)
print(f"Number of training example is: {m}")

i = 0
x_i = x_train[i]
y_i = y_train[i]
print(f'(x^({i}), y^({i})) = ({x_i}, {y_i})')

plt.scatter(x_train, y_train, marker='x', c='r')
# plt.show()
plt.title("housing prices")
plt.xlabel('Size (1000 sqft)')
plt.ylabel('Price (in 1000s of dollars)')
plt.show()

w,b = 200,100
def compute_model_output(x, w, b):
    m = x.shape[0]
    f_wb = np.zeros(m)
    print(f'np.zeros = {f_wb}')
    for i in range(m):
        f_wb[i] = w*x[i] + b
    return f_wb

print(f'w={w}, b={b}')
tmp_f_wb = compute_model_output(x_train, w,b)
plt.plot(x_train, tmp_f_wb,  c = 'b', label='predict values')
plt.scatter(x_train, y_train, marker='x', c = 'r', label='actual values')
plt.title('Housing Proces')
plt.xlabel('Size')
plt.ylabel('Price')
plt.legend()
plt.show()
