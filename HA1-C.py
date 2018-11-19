import random
import HA0
from functools import reduce

#Extended Euclidian Algorithm
#taken from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
def xgcd(b, a):
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return  b, x0, y0

def h(x,y):
    xh = HA0.int_to_hex(x)
    yh = HA0.int_to_hex(y)
    h = HA0.bytes_to_int(HA0.sha1_bytes(xh+yh[2:]))
    return h
    
def f(x,y):
    return h(x,y)

def decrypt(m, b):
    return m**b.e%b.n
def b_from_quad (qi, id, e, n):
    #calculate bi from quad i
    (ai,ci,di,ri) = qi;
    xi = h(ai, ci)
    yi = h(ai^id, di)
    #append r^3 f(xi,yi)
    return ((ri**e) * (f(xi,yi))) % n
    
def mod_inv(r, n):
    return xgcd(r, n)[1] % n

def select_indices(indices, l):
    ret = []
    for i in range(0,len(indices)):
        ret.append(l[indices[i]])
    return ret

def invert_indices(l):
    ret = []
    for i in range(0,len(l)*2):
        if(i not in l):
            ret.append(i)
    return ret
    
    
class Bank:
    def __init__(self):
        p = 89
        q = 73
        self.n = p*q
        phi = (p-1)*(q-1)
        self.e = 127
        self.d = mod_inv(self.e, phi)
        self.k = len(bin(p))+len(bin(q))-4
        
    
    # choose and return half of indices from i..2k as R, save indices not in R as serial_indices
    def cut_and_choose(self, b):
        self.b = b
        self.r = list(range(0,2*self.k))
        self.serial_indices = []
        for i in range(0,self.k):
            self.serial_indices.append(self.r.pop(random.randint(0, len(self.r)-1)))
            
        self.serial_indices.sort()
        return self.r
        
    def approve_and_make_coin (self, bi_in_r):
        for i in range(0, len(bi_in_r)):
            quad = bi_in_r[i]
            # calculate and compare Bi:s with the ones alice generated.
            # note: alice's id is hardcoded as 9. In a real implementation this would be established before initiating coin withdrawal
            if b_from_quad(quad, 9, self.e,self.n) != self.b[self.r[i]]:
                print("check failed")
                continue
        
        # generate blinded serial
        blinded_coin = []
        for i in self.serial_indices:
            blinded_coin.append(((self.b[i]**self.d)) % self.n)
        return blinded_coin
        

class Alice:
    def __init__(self, e, n, k):
        self.id = 9
        self.n = n
        self.e = e
        #Save possible values of r into list
        self.poss_r = []
        for i in range(1,k):
            if xgcd(i,n)[0] == 1: 
                self.poss_r.append(i)

                
    def random_r(self):
        return self.poss_r[random.randint(0, len(self.poss_r)-1)]
        
        
    def generate_B (self, k):
        self.quads = []
        self.b = []
        self.control_f = []
        for i in range(0,2*k):
            # generate and save (ai,ci,di,ri) to list quads
            qi = (random.randint(1,k),random.randint(1,k),random.randint(1,k),self.random_r())
            self.quads.append(qi)
            
            # calculate Bi and save to b
            self.b.append(b_from_quad (qi, self.id, self.e, self.n))
            
            # save all f(xi,yi) for control purposes, not supposed to be in real implementation
            (ai,ci,di,ri) = qi;
            xi = h(ai, ci)
            yi = h(ai^self.id, di)
            self.control_f.append(f(xi,yi)%self.n)
        
        return self.b
    
    #
    def get_bi_in_r (self, r):
        self.r_from_bank = r
        self.bi_in_r = []
        for i in range(0,len(r)):
            self.bi_in_r.append(self.quads[r[i]])
        return self.bi_in_r
    
    #Unblinds coin by multiplying with inverse of ri mod n
    def unblind (self, c):
        coin_indices = invert_indices(self.r_from_bank)
        coin = []
        for i in range(0,len(c)):
            index = coin_indices[i]
            inv = mod_inv(self.quads[index][3], self.n)
            coin.append(c[i]*inv%self.n)
        #return list(coin)
        return reduce(lambda x, y: x*y, coin)%self.n
        

    
    
#Instanciate bank and Alice with Alice knowing banks public exponent e and n
bank = Bank()
alice = Alice(bank.e, bank.n, bank.k)
k = bank.k
#alice generates B
b = alice.generate_B(k)

# alice sends B to bank and bank chooses a random half of the indices
r = bank.cut_and_choose(b)

#bank sends indices to alice extracts all Bi:s with indexes R
br  = alice.get_bi_in_r(r)

# Alice sends these Bi:s to the bank. If correct bank calculates and returns blinded coin
blinded_coin = bank.approve_and_make_coin(br)

# alice unblinds coin
coin = alice.unblind(blinded_coin)
rinv = select_indices(invert_indices(r), list(map(lambda x:mod_inv(x[3], bank.n), alice.quads)))
print("e:",bank.e,"d:",bank.d,"n:", bank.n)
print("r: ", select_indices(invert_indices(r), list(map(lambda x:x[3], alice.quads))))
print("i: ", select_indices(invert_indices(r), list(map(lambda x:mod_inv(x[3], bank.n), alice.quads)))) #r_inv
print("f: ", select_indices(invert_indices(r), alice.control_f))
#print("f^d ", list(map(lambda x: (x**bank.d)%bank.n, select_indices(invert_indices(r), alice.control_f))))
print("f^d", reduce(lambda x,y: x*y, map(lambda x: x**bank.d, select_indices(invert_indices(r), alice.control_f)))%bank.n)
print("b: ", select_indices(invert_indices(r), b))
r_list = select_indices(invert_indices(r), list(map(lambda x:x[3], alice.quads)))
bc = list(map(lambda x, n=bank.n,e=bank.e,d=bank.d: (((x[0]**e)*x[1])**d)%n, zip(r_list, select_indices(invert_indices(r), alice.control_f))))
print("bc:", bc)
#print("bc:", reduce(lambda x,y: x*y, bc)%bank.n)
prod_inv = reduce(lambda x,y,n=bank.n: (x*y)%n, rinv)
print("c: ", ( prod_inv * reduce(lambda x,y: x*y, bc))%bank.n)
#print("c: ", list(map(lambda x: (x[0]*x[1])%bank.n, zip(rinv, bc))))

print(" ---------- prog ------------")
print("b:", select_indices(invert_indices(r),b))
print("bc:", blinded_coin)
#print("c: ", list(map(lambda x: (x[0]*x[1])%bank.n, zip(rinv, blinded_coin))))
print("c: ", alice.unblind(blinded_coin))

