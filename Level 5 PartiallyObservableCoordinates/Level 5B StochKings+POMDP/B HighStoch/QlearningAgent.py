from env_2_stochastic_high import Environment3,StartandGoal,statetocor
import numpy as np
import random

[startstate,goalstate]=StartandGoal()
numX=7
numY=10
numA=8

def QAgent(Timehorizon,Trainingloops):
    #Agent parameters:
    epsilon=0.1; #exploration rate
    alpha=0.5; #alpha in update-rule
    gamma=1; #gamma in target discount rate
    
    start_x,start_y=statetocor(startstate)
    goal_x,goal_y=statetocor(goalstate)
    #Initiliasing Q for every master-loop i.e updated learned for every random seed
    Q=np.zeros((numX,numY,numA));
    seedloops=10
    
    for j in range(seedloops):
        #Changing random seeds
        rseed=j;
        random.seed(rseed)
        np.random.seed(rseed)

        #initilialising very first step
        x=start_x; #At time step-1
        y=start_y;
        action=random.randint(0,numA-1);

        #Q-Learning
        for i in range(int(Trainingloops/10)):
            
            #Exploration-rate for e-greedy
            exploration_rate = random.uniform(0, 1)

            #Fetching next-state reward from envrionment-function
            [xp,yp,reward]=Environment3(x,y,action)

            #Random-action
            if(exploration_rate > epsilon):
                new_action=np.argmax(Q[xp-1,yp-1,:])
            #greedy-action
            else:
                new_action=random.randint(0,numA-1) #random-action

            #print(state,action)
            #Updating Q (Q-learning off policy)
            Target= reward + gamma*np.max(Q[xp-1,yp-1,:])
            Q[x-1,y-1,action] = Q[x-1,y-1,action] + alpha*(Target-Q[x-1,y-1,action]) # update Q value

            #starting from the new-state
            x=xp # updating position in the environment
            y=yp
            action=new_action

            #Restarting episode when goal is reached
            if(x==goal_x and y==goal_y):
                #incrementing episode number
                x=start_x #Reset
                y=start_y
                action=random.randint(0,numA-1)
                
    return Q