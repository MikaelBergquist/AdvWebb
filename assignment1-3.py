import HA0
import math
from binarytree import tree, bst, heap

# --- Del1 ---
def parse_file(file):
    path = []
    path.append (("", file.pop(0)))
    while len(file) > 0:
        l = file.pop(0)
        path.append( (l[0], l[1:]) )
    return path

def calculate_root (path):
    current_hash = path.pop(0)[1]
    while len(path) > 0:
        sibling = path.pop(0)
        if (sibling[0] == "R"):
            temp = current_hash + sibling[1]
            current_hash = HA0.bytes_to_hex(HA0.sha1_bytes (temp))
        if (sibling[0] == "L"):
            temp = sibling[1]+current_hash
            current_hash = HA0.bytes_to_hex(HA0.sha1_bytes (temp))
    print (current_hash)

path = parse_file (HA0.parse_file ("path.txt"))
calculate_root (path)

# --- Del2 --- 
def depth(i):
    return i.bit_length()-1

    
def path_indices (i):
    path = [(i%2,i)]
    i = i>>1
    while i > 1:
        path.append((i%2,i))
        i = i >> 1
    return path
    

def file_to_tree (file_name):
    file = HA0.parse_file(file_name)
    _i = int(file.pop(0))
    _j = int(file.pop(0))
    l = len(file)
    leaf_depth = math.ceil(math.log2(2*l-1))-1
    n = 2**(leaf_depth+1)
    first_leaf = n//2-1 
    tree = [""]*(n-1)
    for i in range(first_leaf,first_leaf+l):
        tree[i] = file.pop(0)
    for i in reversed(range(0,first_leaf)):
        c = (i+1)*2-1
        if tree[c]=="" and tree[c+1]=="":
            continue;
        if tree[c]=="":
            tree[c]=tree[c+1]
            
        if tree[c+1] == "":
            tree[c+1] = tree[c]
            
        #tree[i] = tree[c]+tree[c+1]
        tree[i] = HA0.bytes_to_hex(HA0.sha1_bytes(tree[c]+tree[c+1]))
    return (_i,_j,tree) 
        
def build_string (i,j,t):
    s = ""
    i = i >> 1
    while i > 1:
        if i%2 == 0: s += "L"
        if i%2 == 1: s += "R"
        s += t[i]+"\n"
        i = i >> 1
    return s

def make_output (i,j,t):
    i=(len(t)+1)//2+i
    path=[]
    while i > 1:
        s=""
        if i%2 == 0: s += "R" + t[i]
        if i%2 == 1: s += "L" + t[i-2]
        path.append(s)
        i = i >> 1
    return path[len(path)-j]+t[0]
    
    
(i,j,t) = file_to_tree("leaves.txt")
#b = build_string (i,j,t)
print (make_output(i,j,t))
