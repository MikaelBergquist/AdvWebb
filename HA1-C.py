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
    return pow(m,b.e,b.n)
def Bi_from_quad (qi, id, e, n):
    #calculate Bi from quad i
    (ai,ci,di,ri) = qi;
    xi = h(ai, ci)
    yi = h(ai^id, di)
    #append r^3 f(xi,yi)
    return (pow(ri,e,n) * (f(xi,yi))) % n
    
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
        p = 1021
        q = 859
        self.n = p*q
        phi = (p-1)*(q-1)
        self.e = 1277
        self.d = mod_inv(self.e, phi)
        self.k = len(bin(p))+len(bin(q))-4
        
    
    # choose and return half of indices from i..2k as R, save indices not in R as serial_indices
    def cut_and_choose(self, b):
        self.B = b
        self.r = list(range(0,2*self.k))
        self.serial_indices = []
        for i in range(0, self.k):
            self.serial_indices.append(self.r.pop(random.randint(0, len(self.r)-1)))
            
        self.serial_indices.sort()
        return self.r
        
    def approve_and_make_coin (self, Bi_in_R):
        for i in range(0, len(Bi_in_R)):
            quad = Bi_in_R[i]
            # calculate and compare Bi:s with the ones alice generated.
            # note: alice's id is hardcoded as 9. In a real implementation this would be established before initiating coin withdrawal
            if Bi_from_quad(quad, 9, self.e,self.n) != self.B[self.r[i]]:
                print("check failed")
                continue
        
        # generate blinded serial
        blinded_coin = 1
        for i in self.serial_indices:
            blinded_coin *= pow(self.B[i],self.d,self.n)
        return blinded_coin
        

class Alice:
    def __init__(self, e, n, k):
        self.id = 9
        self.n = n
        self.e = e
        #Save possible values of r into list
        self.poss_r = []
        for i in range(1,n):
            if xgcd(i,n)[0] == 1: 
                self.poss_r.append(i)

    # Returns a random allowed r-value
    def random_r(self):
        return self.poss_r[random.randint(0, len(self.poss_r)-1)]
        
    # Generates B = Bi for i = 1..2k
    def generate_B (self, k):
        self.quads = []
        self.B = []
        self.control_f = []
        for i in range(0,2*k):
            # generate and save (ai,ci,di,ri) to list quads
            qi = (random.randint(1,self.n),random.randint(1,self.n),random.randint(1,self.n),self.random_r())
            self.quads.append(qi)
            
            # calculate Bi and save to b
            self.B.append(Bi_from_quad (qi, self.id, self.e, self.n))
            
            # save all f(xi,yi) for control purposes, not supposed to be in real implementation
            (ai,ci,di,ri) = qi;
            xi = h(ai, ci)
            yi = h(ai^self.id, di)
            self.control_f.append(f(xi,yi)%self.n)
        
        return self.B
    
    # returns quads for indices in R
    def get_quads_in_R (self, R):
        self.R_from_bank = R
        self.Bi_in_R = []
        for i in range(0,len(R)):
            self.Bi_in_R.append(self.quads[R[i]])
        return self.Bi_in_R
    
    # Unblinds coin by multiplying with inverse of ri and then taking mod n
    def unblind (self, c):
        # Indices not in R
        coin_indices = invert_indices(self.R_from_bank)
        
        # product of ri inverse for all indices in coin
        inv_prod = 1
        for i in range(0,len(coin_indices)):
            index = coin_indices[i]
            ri = self.quads[index][3]
            # inverse of ri
            rinv = mod_inv(ri, self.n)
            
            inv_prod *= rinv
        #(blind coin) * (product of all ri in coin) mod n
        return c * inv_prod % self.n
        

# Creates a coin calculated using an approach that uses the real approach as well as a directly calculated control value    
def create_coin_control ():

    ### Simulated withdrawal of one coin ###
    
    #Instanciate bank and Alice with Alice knowing banks public exponent e and n
    bank = Bank()
    alice = Alice(bank.e, bank.n, bank.k)
    k = bank.k
    #alice generates B
    b = alice.generate_B(k)

    # alice sends B to bank and bank chooses a random half of the indices
    R = bank.cut_and_choose(b)

    #bank sends indices to alice extracts all Bi:s with indexes R
    br  = alice.get_quads_in_R(R)

    # Alice sends these Bi:s to the bank. If correct bank calculates and returns blinded coin
    blinded_coin = bank.approve_and_make_coin(br)

    # alice unblinds coin
    coin = alice.unblind(blinded_coin)

    
    
    ### Direct calculation for the product of all f(x,y)^d mod n with indices not in r (meaning they are in coin) ###
    
    # step1: get values of f in coin
    coin_f = select_indices(invert_indices(R), alice.control_f)
    
    # step2: calculate f^d mod n for all f in coin
    fd = map(lambda x, d = bank.d, n = bank.n: pow(x,d,n), coin_f)
    
    # step3: calculate (product of all values from step2) mod n
    control = reduce(lambda x,y: x*y, fd) % bank.n
    print(coin)
    return (coin, control)

    
# Makes 100 coins and checks them against control value
for i in range(0,1):
    (coin, control) = create_coin_control()
    if coin != control:
        print("failed")
    

