import tensorflow as tf
import numpy as np

matrix1 = tf.constant([[3, 3]])
matrix2 = tf.constant([[2],
                       [2]])

# matrix multiply == np.dot(m1, m2)
product = tf.matmul(matrix1, matrix2)

### method 1 ###
# sess = tf.Session()
# result = sess.run(product)
# print(result)
# sess.close()


### method 2 ###
# 自动 close session
with tf.Session() as sess:
    result2 = sess.run(product)
    print(result2)
