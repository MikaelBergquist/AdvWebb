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


class bank:
    def __init__(self):
        p = 5
        q = 11
        self.n = p*q
        phi = (p-1)*(q-1)
        self.e = 7
        self.__d = xgcd(self.e,phi)[1]%phi
    
    def sign(self, b):
        map(lambda x: x**self.__d % self.n, b)
        return b
        
        
class alice:
    def __init__(self, e, n):
        self.id = 9
        self.n = n
        self.e = e
        #Save possible values of r into list
        self.r = []
        for i in range(2,n):
            if xgcd(i,n)[0] == 1: 
                self.r.append(i)
    def random_r(self):
        return self.r[random.randint(0,len(self.r)-1)]
        
        
    def generate_B (self, k):
        self.quads = []
        b = []
        for i in range(0,2*k):
            # save tuple on form (ai,ci,di,ri) to quads
            qi = (random.randint(0,self.n),random.randint(0,self.n),random.randint(0,self.n),self.random_r())
            self.quads.append(qi)
            
            #calculate bi from quad i
            (ai,ci,di,ri) = qi;
            xi = h(ai, ci)
            yi = h(ai^self.id, di)
            #append r^3 f(xi,yi)
            b.append((ri**self.e * f(xi,yi)) % self.n)
        return b
        
    def unblind (self, c):
        for i in range(0, len(c)):
            r = self.quads[i][3]
            rinv = self.rinv(r)
            c[i] = (c[i] * rinv) % self.n
        return c
        
    def rinv(self, r):
        return xgcd(r, self.n)[1] % self.n
    
    
        
        
    
    
    
b = bank()
a = alice(b.e, b.n)
bi = a.generate_B(10)
# alice sends B to bank
signed = b.sign(bi)

print(a.unblind(signed))

