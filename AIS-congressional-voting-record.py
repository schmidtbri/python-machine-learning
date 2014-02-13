import random
import math as math
from collections import defaultdict
from operator import itemgetter
import csv as csv
from random import choice

def getdata():
    with open('congressional_votes.txt', 'r') as f:
        rowdata = []
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            rowdata.append([row[0], row[1:]])
    return rowdata

# a helper function compare a pattern and an antibody and decide whether the antibody identifies the sample as non-self
def compare(data, antibody, r):
    match = 0
    for i in range(len(data)):
        if data[i] == antibody[i]:
            match = match + 1
    if match >= r:
        return True
    else:
        return False


#used by the function below to generate a random antibody
def generate_random_antibody():
    antibody = []
    for i in range(16):
        antibody.append(choice(['y','n']))
    return antibody
   
# this function will generate a set of random antibodies
def generate_antibodies(population_size):
    antibodies = []
    for x in range(0, population_size):
        antibodies.append(generate_random_antibody())        
    return antibodies
    
# this function will train a set of random antibodies
#the training algorithm goes like this:
#if any of the antibodies matches a self data point, delete the antibody and replace it with a randomly generated antibody
#do until all antibodies detect non-self
#the "self" class is selected by the self_class variable
#currently the matching is r-16 or 100% match

def train_antibodies(D, antibodies, self_class, r):
    while True:
        found = False
        #negative selection will happen in here
        #for all antibodies:
        for i in range(len(antibodies)):
            #and all data points:
            for j in range(len(D)):
                #compare the data point to the antibody
                if compare(D[j][1], antibodies[i], r) and D[j][0] == self_class:
                    #if the antibody matches the data point and the class is self then replace the antibody with a random antibody
                    #print "found antibody matching self class: ", D[j], "  ", antibodies[i]
                    antibodies[i] = generate_random_antibody()
                    found = True
                else:
                    found = False
        if not found:
            break
    return antibodies   
   
#this is where all the action happens
def classify(antibodies, data, self_name, foreign_name, r):
    match = False
    #compare the data point to all antibodies:
    for i in antibodies:
        #compare the data point to the antibody
        #if the data point matches an antibody, then we know that it belongs to the foreign class
        if compare(data[1], i, r):
            return foreign_name
    #if the data point does not match any antobodies, then we know that it belongs in the self class
    return self_name
    
def train_and_test(percent_train, num_data, population_size, r):
    D = getdata()

    num_train = int(math.floor(percent_train * num_data))
    num_test = int(num_data - num_train)
    
	# print info about this run
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
    antibodies = train_antibodies(D_train, antibodies, "democrat", r)
    #print "done"
    
    errors = 0
    for i in D_test:
        yhat = classify(antibodies, i, "democrat", "republican", r)
        #print "actual: ", i[0]
        #print "predicted: ", yhat
        #print " "
        if i[0] != yhat:
            errors = errors + 1

    error = float(errors) / float(len(D_test))
    print len(D_train), ",", len(D_test), ",", population_size,",", error, ",", r
    #print 'error: ', error


print "training set size, test set size, population size,  error rate, r"

for i in range(4, 17, 1):
    train_and_test(0.8, 1000, 1000, i)
