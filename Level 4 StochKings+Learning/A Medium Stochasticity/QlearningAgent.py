from env_2_stochastic_medium import Environment2,StartandGoal
import numpy as np
import random

[startstate,goalstate]=StartandGoal()
numS=70
numA=8

def QAgent(Timehorizon,Trainingloops):
    #Agent parameters:
    epsilon=0.1; #exploration rate
    alpha=0.5; #alpha in update-rule
    gamma=1; #gamma in target discount rate
    
    #Initiliasing Q for every master-loop i.e updated learned for every random seed
    Q=np.zeros((numS,numA));
    seedloops=10
    
    for j in range(seedloops):
        #Changing random seeds
        rseed=j;
        random.seed(rseed)
        np.random.seed(rseed)

        #initilialising very first step
        state=startstate; #At time step-1
        action=random.randint(0,numA-1);

        #Q-Learning
        for i in range(int(Trainingloops/10)):
            
            #Exploration-rate for e-greedy
            exploration_rate = random.uniform(0, 1)

            #Fetching next-state reward from envrionment-function
            [reward,new_state]=Environment2(state,action)

            #Random-action
            if(exploration_rate > epsilon):
                new_action=np.argmax(Q[new_state,:])
            #greedy-action
            else:
                new_action=random.randint(0,numA-1) #random-action

            #print(state,action)
            #Updating Q (Q-learning off policy)
            Target= reward + gamma*np.max(Q[new_state,:])
            Q[state,action] = Q[state,action] + alpha*(Target-Q[state,action]) # update Q value

            #starting from the new-state
            state = new_state  # updating position in the environment
            action= new_action

            #Restarting episode when goal is reached
            if(state==goalstate):
                #incrementing episode number
                state=startstate #Reset
                action=random.randint(0,numA-1)
                
    return Q