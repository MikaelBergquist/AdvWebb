import random as rand
from fractions import gcd
import HA0

#Extended Euclidian Algorithm
#taken from https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm#Python
def xea(b, a): #inverse of b mod a
    moda = a
    x0, x1, y0, y1 = 1, 0, 0, 1
    while a != 0:
        q, b, a = b // a, a, b % a
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    if(b ==1): #modification to get modular inverse
        return x0 % moda

'''
pick r value in range 1 to phi -1
'''
def getr(phi):
    r= rand.randint(1, phi-1)
    while(gcd(r, phi) != 1):
        r += 1
    return r

'''
Find modular multiplicative inverse of e (mod(phi)) aka private key aka d
'''
def getPriv(e, phi):
    d = xea(e, phi)
    #I am incomplete - add modular check
    print("this is the inverse of e, also known as d", d)
    return d

'''
Function f & h = SHA1 hash function
'''
def hashfunc(a, b):
   abh = str(a) + str(b) #concat a & b
   h_int = HA0.bytes_to_int(HA0.sha1_bytes(HA0.hex_to_bytes(abh)))
   #print("the hash_val of ", a, "is ", h_int)
   return h_int
    
ID = 123123
p = 61 #if p & q too small RSA breaks :o e == d for tiny primes
q = 53
n = p*q
phi = (p-1)*(q-1)
r = getr(phi)
e = r
d= getPriv(e, phi)

'''
Generate test quadruples 
'''
test_set = [[x+1, x+1, x+1, getr(phi)] for x in range(5)]
print (test_set)
candidates = test_set

'''
Blinder 
B = r^e *f(x, y)mod n
'''
def blind(candidates, e, n, ID):
    i = 0
    Bi = [0]*(len(candidates))
    fi = [0]*(len(candidates))
    ri = [0]*(len(candidates))
    while(i<len(candidates)):
        ai = candidates[i][0]
        ci = candidates[i][1]
        di = candidates[i][2]
        ri[i] = candidates[i][3]
        xi = hashfunc(ai, ci)
        yi = hashfunc(ai^ID, di)
        fi[i] = hashfunc(xi, yi)
        Bi[i] = pow(ri[i], e, n)
        Bi[i] = Bi[i]*fi[i]
        i+=1
    return Bi, fi, ri #we'r plenty for testy reasons
'''
Get signature, all bi values -> bi[i]**d mod n
'''
def sign(Bi, d, n):
    signed = [pow(x, d, n) for x in Bi]
    return signed

'''
Extract coin, inv_r[i] * Bi[i] mod n 
'''
def get_coin(Bi, inv_r, n):
    c = [0]*len(Bi)
    i = 0
    while(i<len(c)):
        c[i] = inv_r[i]*Bi[i]
        i += 1
    print("Here is c", c)
    return c

that, fi, ri = blind(candidates, e, n, ID)
signed_Bi = sign(that, d, n)
inverses_r = [xea(x, n) for x in ri]
coin = get_coin(signed_Bi, inverses_r, n)

'''
Test: Does the inverse of r cancel out r? 
'''
inde = 0
out = [0]*len(ri)
while (inde < len(ri)):
    out[inde] = (inverses_r[inde]*ri[inde])%n
    inde += 1
if(all(i == 1 for i in out)):
    print("Inverse of R cancels r!")
else:
    print("The so called inverse of r is not the inverse of r")
    print(out)

'''
Test: will it RSA?! 
'''
m = 16 #I am a message!
c = (m**e) % n #encrypt m^e mod n = c
de = c**d % n #decrypt c^d mod n = m
if(de == m):
    print("IT WILL RSA!!", m, c, de)
else:
    print("IT WONT RSA :c ", m, c, de)

'''
Test: One last RSA check, this time on the signed coin 
      test if coin[i]**e gets fi[i]%n, 
'''
i = 0
comp = [0]*len(coin)
while(i < len(coin)):
    comp[i] = pow(coin[i], e, n)
    if(comp[i] != (fi[i]%n)):
        print("Something is wrong at index ", i, ",", comp[i], "!=", fi[i]%n)
        break
    i += 1
print("If something wasn't wrong at any indices -> the RSA is still fine ")
