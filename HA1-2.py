import random
import statistics
import math
import time

def simulation(u, k, c):
    num_of_buckets = 2**u
    buckets = [0] * num_of_buckets
    coin_count = 0
    x = 0
    while(coin_count < c):
        r = random.randint(0, num_of_buckets-1)
        buckets[r]+=1
        if buckets[r] == k:
            coin_count+=1
        x+=1
    return x
    
def avg_simulation (u,k,c,target):
    temp = []
    dev = 10000000000.0;
    i = 0;
    while dev >target:
        temp.append(simulation(u,k,c))
        i+=1
        if i>1:
            dev = 3.66*statistics.stdev(temp)/math.sqrt(len(temp));        
            print (i, dev)

    return (statistics.mean(temp), 3.66*statistics.stdev(temp)/math.sqrt(len(temp)))

start_time = time.time()

print(avg_simulation(20,7,10000,4783))

print("simulation time:", time.time()-start_time)
