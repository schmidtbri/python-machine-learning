import random
import math as math
from collections import defaultdict
from operator import itemgetter
import csv as csv
from random import choice

def getdata():
    with open('cancerdata.txt', 'r') as f:
        rowdata = []
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            rowdata.append([row[10], row[1:10]])
    return rowdata

# a helper function compare a pattern and an antibody and decide whether the antibody identifies the sample as non-self
#this function uses a distance function that takes the eucledian distance between the antibody and the data
def compare(data, antibody):
    distance = 0
    for i in range(len(data)):
        distance = distance + pow(int(data[i]) - antibody[0][i], 2)
    distance = math.sqrt(distance)
    if distance > antibody[1]:
        return False
    else:
        return True

def distance(data, antibody):
    distance = 0
    for i in range(len(data)):
        distance = distance + pow(int(data[i]) - antibody[0][i], 2)
    distance = math.sqrt(distance)
    return distance

#used by the function below to generate a random antibody
def generate_random_antibody():
    antibody = []
    for i in range(9):
        antibody.append(choice([1,2,3,4,5,6,7,8,9,10]))
    antibody = [antibody, 1]
    return antibody
   
# this function will generate a set of random antibodies
def generate_antibodies(population_size):
    antibodies = []
    for x in range(0, population_size):
        antibodies.append(generate_random_antibody())        
    return antibodies
    
# this function will train a set of random antibodies
#the training algorithm goes like this:
#test whether all antibody match a self data point
    #if yes, replace
    #if no, leave alone
#for each antibody, find the data point that is closest to it
#make the radius of the antibody the floor function of the distance between the antibody and the closest data point    
def train_antibodies(D, antibodies, self_class):
    while True:
        found = False
        for i in range(len(antibodies)):
            for j in range(len(D)):
                if compare(D[j][1], antibodies[i]) and D[j][0] == self_class:
                    antibodies[i] = generate_random_antibody()
                    found = True
                else:
                    found = False
        if not found:
            break
    for i in range(len(antibodies)):
        #find the closes data point
        closest_point = [[], 1000000]
        for j in range(len(D)):
            if distance(D[j][1], antibodies[i]) < closest_point[1]:
                closest_point = [D[j], distance(D[j][1], antibodies[i])]
        antibodies[i][1] = math.floor(closest_point[1])
    return antibodies    
   

def classify(antibodies, data, self_name, foreign_name):
    match = False
    #compare the data point to all antibodies:
    for i in antibodies:
        #compare the data point to the antibody
        #if the data point matches an antibody, then we know that it belongs to the foreign class
        if compare(data[1], i):
            return foreign_name
    #if the data point does not match any antobodies, then we know that it belongs in the self class
    return self_name
    
def train_and_test(percent_train, num_data, population_size):
    D = getdata()

    num_train = int(math.floor(percent_train * num_data))
    num_test = int(num_data - num_train)

    #print 'using total data points: ', num_data
    #print 'number of training data points: ', num_train
    #print 'number of test data points: ', num_test
    #print " " 
    
    D_train = D[:num_train]
    D_test = D[num_train:num_data]

    #print "generating ", population_size, "antibodies..."
    antibodies = generate_antibodies(population_size)
    #print "done"
    #print " "
    
    #print "training antibodies..."
    antibodies = train_antibodies(D_train, antibodies, "2")
    #print "done"
    
    errors = 0
    for i in D_test:
        yhat = classify(antibodies, i, "2", "4")
        #print "actual: ", i[0]
        #print "predicted: ", yhat
        #print " "
        if i[0] != yhat:
            errors = errors + 1
    error = float(errors) / float(len(D_test))
    print len(D_train), ",", len(D_test), ",", population_size,",", error, ","
    #print 'error: ', error

    
'''    
print "input: training set size, ouput:error rate"
print "training set size, test set size, population size,  error rate, d"
for i in range(100, 600, 10):
    train_and_test(0.8, i, 1000)
'''
print "input: population size, ouput:error rate"
print "training set size, test set size, population size,  error rate, d"
for i in range(50, 10000, 50):
    train_and_test(0.8, 400, i)
    
print "input: d, ouput:error rate"
print "training set size, test set size, population size,  error rate, d"
for i in range(1, 21, 1):
    train_and_test(0.8, 400, 1000) 
