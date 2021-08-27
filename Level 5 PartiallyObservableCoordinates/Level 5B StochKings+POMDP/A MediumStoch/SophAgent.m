clear;

%Environmental dynamics

f = fopen("TransDyn.txt");
data = textscan(f,'%s');
fclose(f);
variable = str2double(data{1}(1:end));
T=reshape(variable,[70,70,8]);

numS=70;
numA=8;

%Start-state
startstate=31;
%Allowable actions N-1, S-2, E-3, W-4
goalstate=38;
goal_x=4;
goal_y=8;
%ActiveInference AGENT

%constructing MDP for SPM_MDP_VB_X.m
D{1}=zeros(numS,1);
D{1}(startstate)=128;

%G: Modalities here, G1: State
%for Modality-1: down_cordinate
A{1}=zeros(17,numS);
for i=1:numS
    [x,y]=statetocor(i);
    A{1}(x+y,i)=1;
end

%for Modality-2: side_cordinate
A{2}=zeros(70,numS);
for i=1:numS
    [x,y]=statetocor(i);
    A{2}(x*y,i)=1;
end


% Transition matrice
% MDP.B{F}(NF,NF,PF)     - transitions among states under PF control states
%F-Factors here F-1: Location
B{1}=zeros(numS,numS,numA);
B{1}=T;
%B{1}=permute(T,[2,1,3]);

%Down_Coordinate
C{1}=zeros(17,1);
C{1}(goal_x+goal_y)=2;

%Side_Coordinate
C{2}=zeros(70,1);
C{2}(goal_x*goal_y)=2;


mdp.A=A;
mdp.D=D;
mdp.B=B;
mdp.C=C;

T_max=10;

ActionProb=zeros(T_max,numA,T_max-1);

for ii=2:T_max
    tic
    T=ii;
    mdp.T=T;
    if(T>6)
        mdp.N=7;
    end
    clear MDP
    MDP=spm_MDP_VB_XX(mdp);
    for jj=1:ii-1
        ActionProb(ii,:,jj)=MDP.P(:,jj);
    end
    toc
end

writematrix(ActionProb,'ActionProb.txt','Delimiter','tab')