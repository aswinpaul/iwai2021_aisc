#Importing Environment and Dynamics
from env_1_nonstochastic_kings import Environment1,StartandGoal,ImportDynamics
[startstate,endstate]=StartandGoal()

import numpy as np
import math
import random

#startstate
start=startstate
#goal-state
goal=endstate

def SophAgentActions(Time_horizon,B):
    #Kings Moves
    numA=8

    #Time horizon
    T=Time_horizon

    #Number of states
    numS=len(B)
    States=[]
    for i in range(numS):
        States.append(i)

    #prior preference
    C=np.zeros(numS)
    C[goal]=1
    #Goal-state-11

    def kl_div(P,Q):

        n=len(P)
        for i in range(n):
            if(P[i]==0):
                P[i]+=0.0000000000001
            if(Q[i]==0):
                Q[i]+=0.0000000000001

        dkl=0
        for i in range(n):
            dkl=dkl-P[i]*math.log(Q[i])+P[i]*math.log(P[i])
        return(dkl)

    Q=np.zeros((numS,numA,numS))
    Q=B
    G=np.zeros((T-1,numA,numS))

    def softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    #planning horizon
    G=np.zeros((T-1,numA,numS))
    Qpi=np.zeros((T-1,numA,numS))

    for k in range(T-2,-1,-1):
        for i in range(numA):
            for j in range(numS):

                if(k==T-2):
                    G[k,i,j]=kl_div(Q[j,i,:],C)

                else:
                    G[k,i,j]=kl_div(Q[j,i,:],C)
                    for jj in range(numS):
                        for kk in range(numA):
                            G[k,i,j]+=Qpi[k+1,kk,jj]*Q[j,i,jj]*G[k+1,kk,jj]

        #Distribution for action-selection
        for ppp in range(numS):
            Qpi[k,:,ppp]=softmax(-1*G[k,:,ppp])
    
    return Qpi