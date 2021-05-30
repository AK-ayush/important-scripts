import tensorflow as tf
import numpy as np
import data_helper

#trainging parameters
batch_size = 32
num_epochs = 200


x_train, y_train = data_helper.read_csv('./data_iris/iris_training.csv')
x_test, y_test = data_helper.read_csv('./data_iris/iris_test.csv')

x = tf.placeholder(tf.float32, shape=[None, 4])
y_ = tf.placeholder(tf.int32, shape=[None, 3])

W1 = tf.Variable(tf.truncated_naromal([10, 4], stddev=0.1))
b1 = tf.Variable(tf.constant(0.1, shape=[10]))

W2 = tf.Variable(tf.truncated_normal([20, 10], stddev=0.1))
b2 = tf.Variable(tf.constant(0.1, shape=[20]))

W3 = tf.Variable(tf.truncated_normal([10, 3], stddev=0.1))
b3  = tf.variable(tf.constant(0.1, shape=[3]))

#first layer
h1 = tf.nn.relu(tf.matmul(x, W1) + b1)

#second layer
h2 = tf.nn.relu(tf.matmul(h1, W2) + b2)

#third layer
h3 = tf.nn.relu(tf.matmul(h2, W3) + b3)

#calculating metrics
loss = tf.nn.softmax_cross_entropy_with_logits(logits=h3 , labels=y_)
prediction = tf.argmax(h3, 1, name='prediction')
correct_prediction = tf.equal(prediction, tf.argmax(y_ , 1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, 'float'), name='accuracy')

#training operation
global_step = tf.Variable(0, name="global_step", trainable=False)
optimizer = tf.train.AdamOptimizer(1e-4)
grads_n_vars = optimizer.compute_gradients(loss)
train_op = optimizer.apply_gradients(grads_n_vars, global_step=global_step)

#summaary to display on the tensorboard
loss_summary = tf.scalar_summary('loss', loss)
accuracy_summary = tf.scalar_summary('accuracy', accuracy)
summary_op = tf.merge_summary([ loss_summary, accuracy_summary])

logs_path="./my_graph"
writer = tf.train.SummaryWriter(logs_path, graph=tf.get_default_graph())

with tf.Session() as sess:
        sess.run(tf.initialize_all_variables())
    batches = data_helper.batch_iter( list(zip(x_train, y_train)), batch_size, num_epochs)
    for batch in batches:
        x_batch,y_batch = zip(*batch)
        current_step = tf.train.global_step(sess, global_step)
        _, step, summaries, loss, accuracy = sess.run([train_op, global_step, summary_op, loss, accuracy],
            feed_dict={x:x_batch, y_:y_batch})
        print( 'step {}, loss {:g}, acc {:g}'.format(step, loss, accuracy))
        #summary writer
        writer.add_summary(summary, step)
        if current_step%100==0:
            accuracy = sess.run([accuracy], feed_dict={x:x_test,y_:y_test})
            print("Accuracy in test {:g}".format(accuracy[0]))