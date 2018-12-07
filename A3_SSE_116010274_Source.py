import random
from datetime import datetime
from collections import defaultdict, Counter
from functools import reduce
from vector import vector_or, vector_and, distance, vector_mean

g_dataset = {}
g_test_good = {}
g_test_bad = {}

DATA_TRAINING = 'digit-training.txt'
DATA_TESTING = 'digit-testing.txt'
DATA_PREDICT = 'digit-predict.txt'
NUM_ROWS = 32
NUM_COLS = 32
PRINT_WIDTH = 40

g_data_model ={
    'or': lambda: data_by_or(),
    'and': lambda: data_by_and(),
    'mean': lambda: data_by_mean(),
    'rand': lambda: data_by_rand(),
    'all': lambda: data_by_all(),
    'kmeans': lambda: data_by_kmeans(),
    'or10': lambda: data_by_or10(),
    'and10': lambda: data_by_and10()
}


''' Load Data '''

def read_digit(p_fp):
    bits = p_fp.read(NUM_ROWS * (NUM_COLS+1))
    if bits == '':
        return -1,bits
    digit = int(p_fp.readline())
    bits = bits.replace('\n','')
    return digit,list(map(int,bits))

def load_data(p_fn = DATA_TRAINING):
    global g_dataset
    g_dataset = defaultdict(list)
    with open(p_fn,'r') as f:
        while True:
            d,v = read_digit(f)
            if d == -1:
                break
            g_dataset[d].append(v)


''' KNN Models '''

def knn_by_majority(p_nn):
    digits = [digit for dist,digit in p_nn]
    return Counter(digits).most_common(1)[0][0]

def knn_by_closest(p_nn):
    return p_nn[0][1]


def predict_by_knn(p_v1, p_knn = 'm1',p_nn = 10):
    nn = []    # nearest neighbors
    for digit in g_dataset:
        for v2 in g_dataset[digit]:
            dist = round(distance(p_v1,v2),2)
            nn.append((dist,digit))
    nn.sort()     # sort neighbors from closest to farthest distance 

    if p_knn == 'm1':
        return knn_by_closest(nn[:p_nn])
    else:
        return knn_by_majority(nn[:p_nn])


'''  Data Types  '''

def data_by_and():
    for digit in g_dataset.keys():
        v = reduce(vector_and,g_dataset[digit])
        g_dataset[digit] = [v]


def data_by_or():
    for digit in g_dataset.keys():
        v = reduce(vector_or,g_dataset[digit])
        g_dataset[digit] = [v]


def data_by_mean():
    for digit in g_dataset.keys():
        v = vector_mean(g_dataset[digit])
        g_dataset[digit] = [v]


def data_by_rand():
    for digit in g_dataset.keys():
        g_dataset[digit] = random.sample(g_dataset[digit],10)


def data_by_and10():
    for digit in g_dataset.keys():
        for grp in range(10):
            data = random.sample(g_dataset[digit],3)
            v = reduce(vector_or,data)
            g_dataset[digit].append(v)
        g_dataset[digit] = g_dataset[digit][-10:]

def data_by_or10():
    for digit in g_dataset.keys():
        for grp in range(10):
            data = random.sample(g_dataset[digit],3)
            v = reduce(vector_and,data)
            g_dataset[digit].append(v)
        g_dataset[digit] = g_dataset[digit][-10:]

def data_by_all():
    return


''' Process Data '''

def digit(p_digit, p_idx = 0):   # vector to original digit format
    vector = g_dataset[p_digit][p_idx]
    for offset in range(0,NUM_ROWS*NUM_COLS, NUM_COLS):
        bits = vector[offset:offset+NUM_COLS]
        bits_string = ''.join(map(str,bits))
        print(bits_string)
    print()

def process_data(p_dm = 'all'):
    if p_dm in g_data_model:
        dm = g_data_model[p_dm]
        load_data()
        dm()


''' Accuracy '''

def compute_accuracy(p_fn = DATA_TESTING, p_knn='m1'):
    global g_test_bad,g_test_good
    g_test_bad = defaultdict(int)
    g_test_good = defaultdict(int)
    t1 = datetime.now()
    show_data_info(t1)
    print('\nBusy figuring out those abstract numbers... Please wait for a while :)\n')
    with open(p_fn,'r') as f:
        while True:
            d,v = read_digit(f)
            if d == -1:
                break
            res = predict_by_knn(v,p_knn)
            g_test_bad[d] += res != d
            g_test_good[d] += res == d
    show_testing_info()
    t2 = datetime.now()
    print('End of Training @ ', t2)
    
    

''' Information Format '''

def show_data_info(t):
    print('Beginning of Training @ ', t)
    print('-'*PRINT_WIDTH)
    print('{:^{}s}'.format('Training Information', PRINT_WIDTH))
    print('-'*PRINT_WIDTH)
    cnt = 0
    for d in range(len(g_dataset)):
        count = len(g_dataset[d])
        print('{:>15d} = {:>3d}'.format(d, count))
        cnt += count
    print('-'*PRINT_WIDTH)
    print('{:>15s} = {}'.format('Total Samples', cnt))
    print('-'*PRINT_WIDTH)

def show_testing_info():
    print('-'*PRINT_WIDTH)
    print('{:^{}s}'.format('Testing Information', PRINT_WIDTH))
    print('-'*PRINT_WIDTH)
    correct_count = 0
    incorrect_count = 0
    for d in range(len(g_dataset)):
        accuracy = g_test_good[d] / (g_test_good[d] + g_test_bad[d]) * 100 
        correct_count += g_test_good[d]
        incorrect_count += g_test_bad[d]
        print('{:>15d} = {:>3d}, {:>3d}, {:3.0f}%'.format(d, g_test_good[d],g_test_bad[d],accuracy))
    print('-'*PRINT_WIDTH)
    accuracy = correct_count / (incorrect_count + correct_count) * 100
    print('{:>15s} = {:3.2f}%'.format('Accuracy',accuracy))
    print('{:>15s} ='.format('Correct/Total'), correct_count, '/',incorrect_count + correct_count)
    print('-'*PRINT_WIDTH)

''' Prediction '''

def predict(p_fn=DATA_PREDICT,p_knn='m1'):
    print()
    print('-'*PRINT_WIDTH)
    print('{:^{}s}'.format('Prediction', PRINT_WIDTH))
    print('-'*PRINT_WIDTH)
    num = 0
    with open(p_fn, 'r') as f:
        while True:
            d, v = read_digit(f)
            if d == -1:
                break
            num += 1
            print(' '*6,'figure {} : {}'.format(num,predict_by_knn(v)))
    print('-'*PRINT_WIDTH)

process_data('rand')
compute_accuracy(DATA_TESTING, 'm1')
predict()
print()
process_data('all')
compute_accuracy(DATA_TESTING, 'm1')
predict()
print()
process_data('mean')
compute_accuracy(DATA_TESTING, 'm1')
predict()