'''
Created on Apr 20, 2018

@author: Arango
'''

import tensorflow as tf

class Qnetwork(object):

    def __init__(self,inputLayerUnits,hiddenLayerUnits):
        #IM WHITE
        #32 cells, each having 5 numbers describing: 0 or 1 if its white or black-->file
        #0 or 1 if the piece is on the game-->0
        #m the type of piece:1KING,2Queen,3Tower,4Bishock,5Knight,6Pawn-->file
        #i,j describing the position of the piece, -1 -1 if its not on the game--->-1 -1
        #another cell for
        #i,j, k, l the possible movement
        self.inputs = tf.placeholder(shape=[1,164],dtype=tf.float32)
        self.net=tf.layers.dense(
            inputs = self.inputs, 
            units =inputLayerUnits,
            activation = tf.nn.tanh
            )
        for x in hiddenLayerUnits:
            self.net=tf.layers.dense(
                inputs = self.net, 
                units =x, 
                activation =tf.nn.tanh
            )
        self.Qout=tf.layers.dense(
                inputs = self.net, 
                units =1, 
                activation = tf.nn.tanh
            )
        #Below we obtain the loss by taking the sum of squares difference between the target and prediction Q values.
        self.nextQ = tf.placeholder(shape=[1,1],dtype=tf.float32)
        self.loss = tf.reduce_sum(tf.square(self.nextQ - self.Qout))
        self.trainer = tf.train.AdamOptimizer(learning_rate=0.001)
        self.updateModel = self.trainer.minimize(self.loss)
        