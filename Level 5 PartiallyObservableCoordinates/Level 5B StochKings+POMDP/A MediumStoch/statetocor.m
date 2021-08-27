function [x,y]=statetocor(state)

a=state/10;
b=mod(state,10);

%x- down_coordinate
%y- side_coordinate

x=ceil(a);
if(b==0)
    y=10;
else
    y=b;
end
end