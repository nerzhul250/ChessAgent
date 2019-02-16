'''
Created on Apr 20, 2018

@author: Arango
'''

import numpy as np
import random
import matplotlib.pyplot as plt
import tensorflow as tf
import os
from mundo.Qnetwork import Qnetwork
from model.Game import Game 
from _datetime import datetime

class State:
    def __init__(self, state=None,actions=None):
        self.state=state
        self.actions=actions
        self.reward=None
        self.qValueComputed=None
        self.takenAction=None
        self.priorState=None
        self.nextState=None

if __name__ == '__main__':
    print("getting to main")
    annealing_steps = 10 #How many steps of training to reduce startE to endE.
    num_episodes = 100 #    How many episodes of game environment to train network with.
    pre_train_steps = 100
    max_epLength = 100
    startE = 0.7 #Starting chance of random action
    endE = 0.1 #Final chance of random action
    load_model = False #Whether to load a saved model.
    gamma=0.7
    path = "../../dqn" #The path to save our model to.
    
    tf.reset_default_graph()
    mainQN = Qnetwork(500,[500,500,10])
    
    init = tf.global_variables_initializer()
    
    saver = tf.train.Saver()
    wons=0
    #Set the rate of random action decrease.
    e = startE
    stepDrop = (startE - endE)/annealing_steps
    
    rList = []
    lossList=[]
    
    #Make a path for our model to be saved in.
    if not os.path.exists(path):
        os.makedirs(path)
        
    with tf.Session() as sess:
        sess.run(init)
        if load_model == True:
            print('Loading Model...')
            ckpt = tf.train.get_checkpoint_state(path)
            saver.restore(sess,ckpt.model_checkpoint_path)
        for i in range(num_episodes):
            
            t = datetime.now().time()
            
            env=Game()
            csWhite=State()
            csBlack=State()
            j=0
            while(not env.isFinished() and j<max_epLength):
                if not e==endE:
                    e=e-stepDrop
                j+=1
                actions=env.getActions(0)
                csWhite.actions=actions
                actions=env.getActions(1)
                csBlack.actions=actions
                
                sw,sb=env.getStates()
                csWhite.state=sw
                csBlack.state=sb
                if env.getTurno()==0:
                    val=-500
                    a=0
                    randomNumber=(random.randint(0,10000)/10000)
                    if j>=pre_train_steps and randomNumber>=e:
                        a2=0
                        for act in csWhite.actions:
                            entrada=np.reshape(np.append(csWhite.state,act,axis=0),(1,164))
                            tempVal=sess.run(mainQN.Qout,feed_dict={mainQN.inputs:entrada})
                            if tempVal>val:
                                a=a2
                                val=tempVal
                            a2+=1
                    else:
                        a=random.randint(0,(csWhite.actions.size//4)-1)
                        entrada=np.reshape(np.append(csWhite.state,csWhite.actions[a],axis=0),(1,164))
                        val=sess.run(mainQN.Qout,feed_dict={mainQN.inputs:entrada})
                        
                    csWhite.takenAction=a
                    csWhite.qValueComputed=val
                    csBlack.takenAction=0
                    entrada=np.reshape(np.append(csBlack.state,csBlack.actions[0],axis=0),(1,164))
                    csBlack.qValueComputed=sess.run(mainQN.Qout,feed_dict={mainQN.inputs:entrada})
                    
                    movimiento=""
                    for number in csWhite.actions[a]:
                        movimiento=movimiento+str(int(float(number)))
                    r=env.mover(int(movimiento))
                    
                    csWhite.reward=r
                    csBlack.reward=r*-1
                else:
                    val=-500
                    a=0
                    if j>=pre_train_steps and (random.randint(0,10000)/10000)>=e:
                        a2=0
                        for act in csBlack.actions:
                            entrada=np.reshape(np.append(csBlack.state,act,axis=0),(1,164))
                            tempVal=sess.run(mainQN.Qout,feed_dict={mainQN.inputs:entrada})
                            if tempVal>val:
                                a=a2
                                val=tempVal
                            a2+=1
                    else:
                        a=random.randint(0,(csBlack.actions.size//4)-1)
                        entrada=np.reshape(np.append(csBlack.state,csBlack.actions[a],axis=0),(1,164))
                        val=sess.run(mainQN.Qout,feed_dict={mainQN.inputs:entrada})
                    csBlack.takenAction=a
                    csBlack.qValueComputed=val
                    csWhite.takenAction=0
                    entrada=np.reshape(np.append(csWhite.state,csWhite.actions[0],axis=0),(1,164))
                    csWhite.qValueComputed=sess.run(mainQN.Qout,feed_dict={mainQN.inputs:entrada})
                    
                    mov0=7-int(float(csBlack.actions[a][0]))
                    mov1=int(float(csBlack.actions[a][1]))
                    mov2=7-int(float(csBlack.actions[a][2]))
                    mov3=int(float(csBlack.actions[a][3]))
                    movimiento=str(mov0)+str(mov1)+str(mov2)+str(mov3)
                    r=env.mover(int(movimiento))
                    
                    csBlack.reward=r
                    csWhite.reward=r*-1
                    
                newWhiteState=State()
                newBlackState=State()
                csWhite.nextState=newWhiteState
                csBlack.nextState=newBlackState
                newWhiteState.priorState=csWhite
                newBlackState.priorState=csBlack
                csWhite=newWhiteState
                csBlack=newBlackState
            #BACKWARDS LEARNING    
            csWhite=csWhite.priorState
            csBlack=csBlack.priorState
            if csWhite!= None and csWhite.reward!=0:
                wons+=1
                targetQ=csWhite.qValueComputed*(1-gamma)+gamma*csWhite.reward
                entrada=np.reshape(np.append(csWhite.state,csWhite.actions[csWhite.takenAction],axis=0),(1,164))
                _,Qout1,loss= sess.run([mainQN.updateModel,mainQN.Qout,mainQN.loss],feed_dict={mainQN.inputs:entrada,mainQN.nextQ:targetQ})
                lossList.append(loss)
                targetQ=csBlack.qValueComputed*(1-gamma)+gamma*csBlack.reward
                entrada=np.reshape(np.append(csBlack.state,csBlack.actions[csBlack.takenAction],axis=0),(1,164))    
                _,Qout1,loss= sess.run([mainQN.updateModel,mainQN.Qout,mainQN.loss],feed_dict={mainQN.inputs:entrada,mainQN.nextQ:targetQ})
                lossList.append(loss)
                csBlack=csBlack.priorState
                while csBlack is not None:
                    val=-500
                    a=0
                    a2=0
                    for act in csBlack.nextState.actions:
                        tempVal=sess.run(mainQN.Qout,feed_dict={mainQN.inputs:np.reshape(np.append(csBlack.nextState.state,act,axis=0),(1,164))})
                        if tempVal>val:
                            a=a2
                            val=tempVal
                        a2+=1
                    targetQ=csBlack.qValueComputed*(1-gamma)+gamma*(csBlack.reward+val)
                    entrada=np.reshape(np.append(csBlack.state,csBlack.actions[csBlack.takenAction],axis=0),(1,164))
                    _,Qout1,loss= sess.run([mainQN.updateModel,mainQN.Qout,mainQN.loss],feed_dict={mainQN.inputs:entrada,mainQN.nextQ:targetQ})
                    lossList.append(loss)
                    csBlack=csBlack.priorState
                csWhite=csWhite.priorState
                while csWhite is not None:
                    val=-500
                    a=0
                    a2=0
                    for act in csWhite.nextState.actions:
                        tempVal=sess.run(mainQN.Qout,feed_dict={mainQN.inputs:np.reshape(np.append(csWhite.nextState.state,act,axis=0),(1,164))})
                        if tempVal>val:
                            a=a2
                            val=tempVal
                        a2+=1
                    targetQ=csWhite.qValueComputed*(1-gamma)+gamma*(csWhite.reward+val)
                    entrada=np.reshape(np.append(csWhite.state,csWhite.actions[csWhite.takenAction],axis=0),(1,164))
                    _,Qout1,loss= sess.run([mainQN.updateModel,mainQN.Qout,mainQN.loss],feed_dict={mainQN.inputs:entrada,mainQN.nextQ:targetQ})
                    lossList.append(loss)
                    csWhite=csWhite.priorState
            rList.append(wons)
            #Periodically save the model. 
            if i % 10 == 0:
                saver.save(sess,path+'/model-'+str(i)+'.ckpt')
                print("Saved Model")
            if i%10 == 0:
                print(str(i)+' '+str(wons))
            #print (str(i) + str(datetime.now().time() - t))
        plt.plot(lossList)
        plt.show()