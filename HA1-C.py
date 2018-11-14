import random
import HA0

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
    return (ri**e * f(xi,yi)) % n

class Bank:
    def __init__(self):
        p = 5
        q = 11
        self.n = p*q
        phi = (p-1)*(q-1)
        self.e = 7
        self.d = xgcd(self.e,phi)[1]%phi #d = inverse of e mod n

    
    # choose and return half of indices from i..2k as R, save indices not in R as serial_indices
    def cut_and_choose(self, b):
        self.b = b
        k = len(b)//2
        self.r = list(range(0,len(b)))
        self.serial_indices = []
        for i in range(0,k):
            self.serial_indices.append(self.r.pop(random.randint(0, len(self.r)-1)))
        return self.r
        
    def approve_and_make_coin (self, bi_in_r):
        for i in range(0, len(bi_in_r)):
            quad = bi_in_r[i]
            # calculate and compare Bi:s with the ones alice generated.
            # note: alice's id is hardcoded as 9. In a real implementation this would be established before initiating coin withdrawal
            if b_from_quad(quad, 9,self.e,self.n) != self.b[self.r[i]]:
                print("check failed")
                return
        
        # generate blinded serial
        blinded_coin = []
        for i in self.serial_indices:
            #print(i,self.b[i]**self.d%self.n)
            blinded_coin.append(((self.b[i]**self.d)) % self.n)
        return blinded_coin
        

class Alice:
    def __init__(self, e, n):
        self.id = 9
        self.n = n
        self.e = e
        #Save possible values of r into list
        self.poss_r = []
        for i in range(2,n):
            if xgcd(i,n)[0] == 1: 
                self.poss_r.append(i)
                
                
    def random_r(self):
        return self.poss_r[random.randint(0, len(self.poss_r)-1)]
        
        
    def generate_B (self, k):
        self.quads = []
        self.b = []
        for i in range(0,2*k):
            # generate and save (ai,ci,di,ri) to list quads
            qi = (random.randint(0,self.n),random.randint(0,self.n),random.randint(0,self.n),self.random_r())
            self.quads.append(qi)
            
            # calculate Bi and save to b
            self.b.append(b_from_quad (qi, self.id, self.e, self.n))
        return self.b
    
    def get_bi_in_r (self, r):
        self.bi_in_r = []
        for i in range(0,len(r)):
            self.bi_in_r.append(self.quads[r[i]])
        return self.bi_in_r
        
    def unblind (self, c):
        for q in self.bi_in_r:
            r_inv = self.r_inv(q[3])
            map(lambda x: x*(r_inv), c)
        return c
        
    def r_inv(self, r):
        return xgcd(r, self.n)[1] % self.n
    
    
#Instanciate bank and Alice with Alice knowing banks public exponent e and n
bank = Bank()
alice = Alice(bank.e, bank.n)
k = 10
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

print(coin)

