import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import itertools
import operator
import math as math

def classify(point, weights):
    cutoff = 0
    an = (weights[0]*point[0]) + (weights[1]*point[1]) + (weights[2]*point[2]) + (weights[3]*point[3])
    if an > 0:
        return 1
    if an <= 0:
        return 0


def train(class1, other_class):
    #learning rate 
    n = 0.2
    
    #initialize the weights with random values
    weights = [-0.05,-0.02,0.02,0.01]
    
    #if the weights are changed then this variable is true, which means that the algorithm should keep going
    weights_changed = True
    
    while weights_changed:
        weights_changed = False
        #cycle through the given class, the output should be True for this one
        for v in class1:
            #if the answer is 0, we know it is incorrect, so we calculate new weights
            if classify(v, weights) == 0:
                for w in range(len(weights)):
                    weights[w] = weights[w] + n*(1-0) * v[w]
                weights_changed = True
        #cycle through the other_class, the output should False for this one    
        for v in other_class:
            #if the answer is 0, we know it is incorrect, so we calculate new weights
            if classify(v, weights) == 1:
                for w in range(len(weights)):
                    weights[w] = weights[w] + n*(0-1) * v[w]
                weights_changed = True
    return weights
          
         
R1 = [[0,-1,-1, -1], [-1,0,0, -1], [-3,0,1, -1], [-2,1,0, -1]]
R2 = [[-14,5,7, -1], [-12,4,9, -1], [-10,6,8, -1], [-15,9,7, -1]]
R3 = [[8,5,-5, -1], [10,3,6, -1], [11,7,-3, -1], [10,4,4, -1]]

categories = [R1, R2, R3]

r1 = train(R1, R2+R3)
r2 = train(R2, R3+R1)
r3 = train(R3, R1+R2)

print "the linear function separating R1 and R2, R3 is defined by: ", r1
print "the linear function separating R2 and R1, R3 is defined by: ", r2
print "the linear function separating R3 and R1, R2 is defined by: ", r3
print ""

points = [[-12,5,9, -1], [-1,-1,-1, -1], [0,0,0, -1], [7,5,-6, -1], [-14,4,8, -1], [16,16,16, -1]]

#now classifying
for p in points:
    if classify(p, r1) == 1:
        print "point: ", p, " belongs to class: R1"
    elif classify(p, r2) == 1:
        print "point: ", p, " belongs to class: R2"
    elif classify(p, r3) == 1:
        print "point: ", p, " belongs to class: R3"
    else:
        print "point: ", p, " could not be classified"
