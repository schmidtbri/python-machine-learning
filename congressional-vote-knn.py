import random
import math as math
from collections import defaultdict
from operator import itemgetter
import csv as csv

def getdata():
    with open('congressional_voting_record.txt', 'r') as f:
        rowdata = []
        reader = csv.reader(f)
        reader.next()
        for row in reader:
            rowdata.append(row)
    return rowdata
    
def distance(x1, x2):
    if len(x1) != len(x2):
    	return False
    else:
        distance = 0
        for i in range(1,len(x1)):
            if x1[i] != x2[i]:
                distance += 1            
            if x1[i] == "?" or x2[i] == "?":
                distance = distance
        return distance

def knn_predict(D, x, k):
    distances = []
    for xp in D:
        distances.append((xp[0], distance(xp, x) ))
    if k == 1:
        # k = 1 is treated as a special case
        return min(distances, key=itemgetter(1))[0]
    # k > 1
    distances.sort(key=itemgetter(1))
    nn = distances[:k]
    counts = defaultdict(int)
    for yp, d in nn:
        counts[yp] += 1
    return max(counts.items(), key=itemgetter(1))[0]

def test_knn(k=1, k_max=22, percent_train=0.80, percent_validate=0.1, N=None):
    D = getdata()
    N_original = len(D)
    if N is None:
        N = len(D)
    else:
        # only use N examples from the data set
        D = D[:N]

    num_train = int(math.floor(percent_train * N))
    num_validate = int(math.floor(percent_validate * N))
    num_test = N - (num_train + num_validate)
    
    # print infor about this run
    print 'using {0} of {1} examples'.format(N, N_original)
    print 'number train:', num_train
    print 'number validate:', num_validate
    print 'number test:', num_test
    print 'starting k:', k
    print 'max k:', k_max

    D_train = D[:num_train] # {(x_1, y_1),...(x_num_train-1, y_num_train-1)}
    D_validate = D[num_train:num_validate + num_train] # {(x_1, y_1),...(x_num_train-1, y_num_train-1)}
    D_test = D[num_validate + num_train:] # {(x_num_train, y1_num_train),...(x_N, y_N)}
    

    chosen_k = k;
    least_error = 1000000000;
    #choosing the k with the least errors by using the validation set
    for k_test in range(k, k_max+1):
        errors = 0
        for x in D_validate:
            yhat = knn_predict(D_train, x, k_test)
            #print "predivcted:", yhat
            #print "actual:", x[0]
            errors += int(x[0] != yhat)
            
        print "testing k= " + str(k_test) + ", total errors for this k: " + str(errors)
        #if this k has less error than the already chosen k, then replace
        if(errors < least_error):
            chosen_k = k_test
            least_error = errors
            
    print "chose k= " +  str(chosen_k) + ", with error=" +  str(least_error) + "/" + str(num_validate)
    
    error_count = 0
    for x in D_test:
        yhat = knn_predict(D_train, x, chosen_k)
        if x[0] != yhat:
            error_count += 1
        #print "predivcted:", yhat
        #print "actual:", x[0]
        
    print "error percent:" + str(float(error_count) / float(num_test))

#test_knn( k_start, k_max, training_proportion, validation_proportion, testing_proportion, sample_size)
test_knn(2, 12, 0.8, 0.1, 400)
