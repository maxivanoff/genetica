import numpy as np
from itertools import combinations,permutations


def update(values, maxvalues):
    numvalues = len(values)
    stop=False
    count=numvalues-1
    for v,m in zip(reversed(values),reversed(maxvalues)):
        if v==m:
            values[count:numvalues]=int(numvalues-count)*[0]
            print "count=",count
            if not values[count-1]==m:values[count-1]+=1
        count+=-1
    return values,stop
values=[0,0,0,0]
stop=False
count=0
while not stop:
    print values
    values[-1] += 1
    values,stop = update(values, [3,3,3,3]) 
    if count==20: break
    count+=1



