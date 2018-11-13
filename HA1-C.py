import random

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
    return x^y
    
def f(x,y):
    return x^y
    
def randint():
    return random.randint(0, 40)
    
def quads(n):
    l = []
    for i in range(0,n):
        l.append((randint(),randint(),randint(),randint()))
    return l
    

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
    
    def sign(self, c):
        return c ** self.__d % self.n
        
        
class alice:
    def __init__(self, n, e):
        self.id = 9
        self.n = n
        self.e = e
        self.__r = 3
        self.make_rinv()
        
    def quads (self, k):
        self.__r = 3
        self.make_rinv()
        l = []
        for i in range(0,2*k):
            l.append((random.randint(0,self.n),random.randint(0,self.n),random.randint(0,self.n),random.randint(0,self.n)))
        return l
    def unblind (self, c):
        return c*self.__rinv**self.e%self.n
    def blind (self, c):
        return c*self.__r**self.e%self.n
    def make_rinv(self):
        self.__rinv = xgcd(self.__r, self.n)[1] % self.n
    
        
        
        
    
    
    
b = bank()
a = alice(b.n, b.e)
c = a.blind(10) 
print (c)
print(a.unblind(c))

