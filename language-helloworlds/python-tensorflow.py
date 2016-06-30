import tensorflow as tf
constant = matrix1 = tf.constant('Hello World')
sess = tf.Session()
result = sess.run(constant)
print (result)
sess.close()
