#Windy grid world Environment-2

#Stochastic wind policy
#King's moves allowed
#Allowed actions-8 N,S,E,W,NW,SW,SE,NE

#importing modules
import numpy as np
import random

#Representing Windy-grid as a list with boundaries
#Using Programming assignment-2 grid world representation
grid=[[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1], 
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
      [1, 2, 0, 0, 0, 0, 0, 0, 3, 0, 0, 1], 
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
      [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1], 
      [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]

#1-boundary wall
#0-free state
#2-Start
#3-end

#dimensions of the grid
n=len(grid)
n1=len(grid)
n2=len(grid[0])

#Encoding states and determining T(s,a,s') and R(s,a,s')
allstates=[]
nonterm=[]
validstates=[]
endstates=[]
startstate=[]

for i in range(n1):
    for j in range(n2):

        allstates.append((i,j))
        if(grid[i][j]!=1):
            validstates.append((i,j))
        if(grid[i][j]!=1 and grid[i][j]!=3):
            nonterm.append((i,j))
        if(grid[i][j]==2):
            startstate.append((i,j))
        if(grid[i][j]==3):
            endstates.append((i,j))
            
#Useful lists
#allstates,validstates,endstates,startstate
numS=len(validstates)
numT=len(nonterm)
numSta=len(startstate)
numEnd=len(endstates)
numA=8

#to get the state number corresponding to the coordinate of a valid state
def ctostates(x,y):
    s=0
    for i in range(numS):
        if(validstates[i][0]==x and validstates[i][1]==y):
            break
        s=s+1
    return(s)


# In[60]:


#Using the GRID-data to evaluate transtion matrice T(s,a,s') and R(s,a,s')
#These matrices are only present in environment and not accessible to agent
#T(s,a,s')
T=np.zeros((numS,numA,numS))
#R(s,a,s')
R=np.zeros((numS,numA,numS))

#Transitions
#all valid states
for i in range(numT):
    #Valid actions
    for j in range(numA):
        a=nonterm[i][0]
        b=nonterm[i][1]
        s=(a,b)
        p=1
        n=-1

        #Implementing-wind
        if(b==1 or b==2 or b==3 or b==10):
            w=0
        if(b==4 or b==5 or b==6 or b==9):
            w=1
        if(b==7 or b==8):
            w=2
            
        #Wind values at top-most column assumed to be zero except for move-SOUTH
        if(a==1):
            w=0;
        if(a==2 and (b==7 or b==8)):
            w=1;
        
        if(w==0):
            #North
            if(j==0):
                ap=a-1
                bp=b
                for k in range(numS):
                    if(validstates[k][0]==ap and validstates[k][1]==bp):
                        sp=(ap,bp)
                        break
                    else:
                        sp=(a,b)
                for kk in range(len(endstates)):
                    if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                        r=p
                        break
                    else:
                        r=n
                T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=1
                R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

            #South
            if(j==1):
                #Re-writing wind-values in top most row i.e a=2 and south move
                if(a==1 and (b==4 or b==5 or b==6 or b==9 or b==7 or b==8)):
                    w=1;

                ap=a+1
                bp=b
                for k in range(numS):
                    if(validstates[k][0]==ap and validstates[k][1]==bp):
                        sp=(ap,bp)
                        break
                    else:
                        sp=(a,b)
                for kk in range(len(endstates)):
                    if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                        r=p
                        break
                    else:
                        r=n
                T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=1
                R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

            #East
            if(j==2):
                ap=a
                bp=b+1
                for k in range(numS):
                    if(validstates[k][0]==ap and validstates[k][1]==bp):
                        sp=(ap,bp)
                        break
                    else:
                        sp=(a,b)
                for kk in range(len(endstates)):
                    if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                        r=p
                        break
                    else:
                        r=n
                T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=1
                R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

            #West
            if(j==3):
                ap=a
                bp=b-1
                for k in range(numS):
                    if(validstates[k][0]==ap and validstates[k][1]==bp):
                        sp=(ap,bp)
                        break
                    else:
                        sp=(a,b)
                for kk in range(len(endstates)):
                    if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                        r=p
                        break
                    else:
                        r=n
                T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=1
                R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

            #North-East
            if(j==4):
                ap=a-1
                bp=b+1
                for k in range(numS):
                    if(validstates[k][0]==ap and validstates[k][1]==bp):
                        sp=(ap,bp)
                        break
                    else:
                        sp=(a,b)
                for kk in range(len(endstates)):
                    if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                        r=p
                        break
                    else:
                        r=n
                T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=1
                R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

            #East-South
            if(j==5):
                #Re-writing wind-values in top most row i.e a=2 and south move
                if(a==1 and (b==4 or b==5 or b==6 or b==9 or b==7 or b==8)):
                    w=1;

                ap=a+1
                bp=b+1
                for k in range(numS):
                    if(validstates[k][0]==ap and validstates[k][1]==bp):
                        sp=(ap,bp)
                        break
                    else:
                        sp=(a,b)
                for kk in range(len(endstates)):
                    if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                        r=p
                        break
                    else:
                        r=n
                T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=1
                R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

            #South-West
            if(j==6):
                #Re-writing wind-values in top most row i.e a=2 and south move
                if(a==1 and (b==4 or b==5 or b==6 or b==9 or b==7 or b==8)):
                    w=1;

                ap=a+1
                bp=b-1
                for k in range(numS):
                    if(validstates[k][0]==ap and validstates[k][1]==bp):
                        sp=(ap,bp)
                        break
                    else:
                        sp=(a,b)
                for kk in range(len(endstates)):
                    if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                        r=p
                        break
                    else:
                        r=n
                T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=1
                R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

            #North-West
            if(j==7):
                ap=a-1
                bp=b-1

                for k in range(numS):
                    if(validstates[k][0]==ap and validstates[k][1]==bp):
                        sp=(ap,bp)
                        break
                    else:
                        sp=(a,b)
                for kk in range(len(endstates)):
                    if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                        r=p
                        break
                    else:
                        r=n
                T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=1
                R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')
                
        #This condition is to select positions from grid according to the grid. Later we make a list of possible transitions
        #looking at probabilities and will rnadomly select one out of 3-possible transition states.
        
        else:
            windlist=[w-1,w,w+1]
            setwind=w
            
            for xx in windlist:
                
                if(xx==setwind):
                    tpr=0.7
                else:
                    tpr=0.15
                    
                #North
                if(j==0):
                    w=xx
                    ap=a-1-w
                    if(ap<1):
                        ap=1
                    bp=b
                    for k in range(numS):
                        if(validstates[k][0]==ap and validstates[k][1]==bp):
                            sp=(ap,bp)
                            break
                        else:
                            sp=(a,b)
                    for kk in range(len(endstates)):
                        if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                            r=p
                            break
                        else:
                            r=n
                    T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]+=tpr
                    R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                    #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

                #South
                if(j==1):
                    w=xx
                    #Re-writing wind-values in top most row i.e a=2 and south move
                    if(a==1 and (b==4 or b==5 or b==6 or b==9 or b==7 or b==8)):
                        w=1;

                    ap=a+1-w
                    if(ap<1):
                        ap=1
                    bp=b
                    for k in range(numS):
                        if(validstates[k][0]==ap and validstates[k][1]==bp):
                            sp=(ap,bp)
                            break
                        else:
                            sp=(a,b)
                    for kk in range(len(endstates)):
                        if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                            r=p
                            break
                        else:
                            r=n
                    T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]+=tpr
                    R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                    #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

                #East
                if(j==2):
                    w=xx
                    ap=a-w
                    if(ap<1):
                        ap=1
                    bp=b+1
                    for k in range(numS):
                        if(validstates[k][0]==ap and validstates[k][1]==bp):
                            sp=(ap,bp)
                            break
                        else:
                            sp=(a,b)
                    for kk in range(len(endstates)):
                        if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                            r=p
                            break
                        else:
                            r=n
                    T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]+=tpr
                    R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                    #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

                #West
                if(j==3):
                    w=xx
                    ap=a-w
                    if(ap<1):
                        ap=1
                    bp=b-1
                    for k in range(numS):
                        if(validstates[k][0]==ap and validstates[k][1]==bp):
                            sp=(ap,bp)
                            break
                        else:
                            sp=(a,b)
                    for kk in range(len(endstates)):
                        if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                            r=p
                            break
                        else:
                            r=n
                    T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]+=tpr
                    R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                    #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

                #North-East
                if(j==4):
                    w=xx
                    ap=a-1-w
                    if(ap<1):
                        ap=1
                    bp=b+1
                    for k in range(numS):
                        if(validstates[k][0]==ap and validstates[k][1]==bp):
                            sp=(ap,bp)
                            break
                        else:
                            sp=(a,b)
                    for kk in range(len(endstates)):
                        if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                            r=p
                            break
                        else:
                            r=n
                    T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]+=tpr
                    R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                    #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

                #East-South
                if(j==5):
                    w=xx
                    #Re-writing wind-values in top most row i.e a=2 and south move
                    if(a==1 and (b==4 or b==5 or b==6 or b==9 or b==7 or b==8)):
                        w=1;

                    ap=a+1-w
                    if(ap<1):
                        ap=1
                    bp=b+1
                    for k in range(numS):
                        if(validstates[k][0]==ap and validstates[k][1]==bp):
                            sp=(ap,bp)
                            break
                        else:
                            sp=(a,b)
                    for kk in range(len(endstates)):
                        if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                            r=p
                            break
                        else:
                            r=n
                    T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]+=tpr
                    R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                    #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

                #South-West
                if(j==6):
                    w=xx
                    #Re-writing wind-values in top most row i.e a=2 and south move
                    if(a==1 and (b==4 or b==5 or b==6 or b==9 or b==7 or b==8)):
                        w=1;

                    ap=a+1-w
                    if(ap<1):
                        ap=1
                    bp=b-1
                    for k in range(numS):
                        if(validstates[k][0]==ap and validstates[k][1]==bp):
                            sp=(ap,bp)
                            break
                        else:
                            sp=(a,b)
                    for kk in range(len(endstates)):
                        if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                            r=p
                            break
                        else:
                            r=n
                    T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]+=tpr
                    R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                    #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

                #North-West
                if(j==7):
                    w=xx
                    ap=a-1-w
                    if(ap<1):
                        ap=1
                    bp=b-1

                    for k in range(numS):
                        if(validstates[k][0]==ap and validstates[k][1]==bp):
                            sp=(ap,bp)
                            break
                        else:
                            sp=(a,b)
                            
                    for kk in range(len(endstates)):
                        if(sp[0]==endstates[kk][0] and sp[1]==endstates[kk][1]):
                            r=p
                            break
                        else:
                            r=n
                    T[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]+=tpr
                    R[ctostates(s[0],s[1]),j,ctostates(sp[0],sp[1])]=r
                    #print('transition'+' '+str(ctostates(s[0],s[1]))+' '+str(j)+' '+str(ctostates(sp[0],sp[1]))+' '+str(r)+' '+'1')

            
            
#Start-state for algorithm to use as S0
#Note: s0 is accesible to agent and only s0
S0=startstate[0]
s0=ctostates(S0[0],S0[1])

#Goal-state dynamics
T[37,:,37]=1

def statetocor(state):
    [x,y]=validstates[state]
    return (x,y)

#Function that returns next state and reward using T and R matrices.
#only this function is accessible to agent and not T and R directly
def Environment3(x,y,action):
    # This function returns 
    # Ouput:
    # 1.reward
    # 2.next_state given 
    # Input:
    # 1.current_state
    # 2.action
    
    state=ctostates(x,y)
    possible_list=[];
    corr_prob=[];
    
    for i in range(numS):
        if(T[state,action,i]>0.001):
            possible_list.append(i)
            corr_prob.append(T[state,action,i])
      
    next_state=np.random.choice(possible_list,p=corr_prob)
    reward=R[state,action,next_state]
    
    xp,yp=statetocor(next_state)
    reward=R[state,action,next_state]
    return(xp,yp,reward)

#Returns the start-state and goal-state
def StartandGoal():
    return ctostates(4,1),ctostates(4,8)

def ImportDynamics():
    return T 