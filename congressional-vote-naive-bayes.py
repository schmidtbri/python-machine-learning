import random, sys
import numpy as np
import math as math
import csv as csv

def getdata():
    with open('congressional_voting_record.txt', 'r') as f:
        rowdata = []
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            rowdata.append(row)
    return rowdata

def get_class_list(documents):
    classes = []
    for document in documents:
        if document[0] not in classes:
            classes.append(document[0])
    return classes
    
    
def get_class_probability(class_name, documents):
    count = 0
    class_count = 0
    for document in documents:
        if document[0] == class_name:
            count += 1
            class_count += 1
        else:
            count += 1
    return float(class_count) / float(count)


def get_vote_probability_given_class(vote, content, class_name, documents):
    #returns the probability of the class, given the vote and "yes", "no", or "?"
    #go through the votes, counting all of the votes that have the given vote in them, and all of the documents in this class
    class_documents = 0
    documents_with_vote = 0
    
    for document in documents:
        if document[0] == class_name:
            class_documents += 1
    
    for document in documents:
        if document[0] == class_name:
            if document[vote] == content:
                documents_with_vote += 1
                
    if class_documents > 0:
        return float(documents_with_vote)+1 / float(class_documents)+3
    else:
        return 0.0  
    

def predict(D, x):
    
    predicted_class = "none"
    predicted_probability = -1000
    
    for class_name in get_class_list(D):
        class_probability = math.log(get_class_probability(class_name, D))

        word_probability_given_class = 0
        
        vote = 1
        for content in x[1:]:
            prob = get_vote_probability_given_class( vote, content, class_name, D)
            vote+=1
            if prob != 0:
                word_probability_given_class += math.log(prob)

        class_probability = class_probability + word_probability_given_class   
        
        if class_probability > predicted_probability:
            predicted_class = class_name
            predicted_probability = class_probability
        
    return predicted_class, predicted_probability
    
        

def train_and_test(percent_train, percent_validate, num_documents):
    
    D = get_data()
    
    num_train = int(math.floor(percent_train * num_documents))
    num_validate = int(math.floor(percent_validate * num_documents))
    num_test = num_documents - (num_train + num_validate)
    
    # print info about this run
    print 'using {0} documents'.format(num_documents)
    print 'number of train documents:', num_train
    print 'number of validate documents:', num_validate
    print 'number of test documents:', num_test
    
    D_train = D[:num_train] 
    D_validate = D[num_train:num_validate + num_train] 
    D_test = D[num_validate + num_train:num_documents]
	
    errors = 0
    total_test = 0
    for i in D_test:
        
        yhat, probability = predict(D_train, i)
        #print "actual: ", i[0]
        #print "predicted: ", yhat
        #print " "
        if i[0] != yhat:
            errors = errors + 1
        total_test += 1
            
    error = float(errors) / float(total_test)
    print 'error: ', error

train_and_test(0.8, 0.1, 400)