import HA0
import math
import Crypto as Cry

tree = []
with open("tree.txt", "r") as f:
    for line in f:
        tree.append(line.rstrip())



tree = tree[2:]
if len(tree) % 2 != 0:
    tree.append(tree[len(tree)-1])

def get_parent_val(val1, val2):
    #hash = HA0.bytes_to_hex(HA0.sha1_bytes(HA0.hex_to_bytes(val1 + val2)))
    #print(hash)
    hash = val1 + val2
    return hash

'''
tree = ['fcfdd2a12d8b0b75c2edb47d691470dd0178c566',
'031e3057d40d25472cdb80e4952ed6738936aba8',
'7164148d695971de1b9f31be8e730299823b1def',
'64d866d14053a33e75744d966daa4f47b92018b9',
'a7e62ee4822cb29ec7004841d8f819965be169d9',
'c176f7a3dc7a3f59136b42163efa8f6350bb073c',
'c25053cedc71463287168687accf4e701a7ace0f',
'2af15e40605eb51d3a2e041f9799f3a070398eb1',
'053dfa25bf07b0d530c6bb9f803d60062f4e0e00',
'6c136b269efa9535f02732d68c80371625783cfc',
'd1705b195fb31e4e9c0b03570c677e59a19250b8',
'e5fb3dc4357332ec108e5d4d25991942e4ec9a95']
'''
tree = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'I', 'J', 'K', 'L']
nbr_leaves = len(tree)


def setup(leaf_list):
    tree = [[leaf_list], [0 for x in range(nbr_leaves)]]


def hasher(duplet_array):
    var1 = duplet_array.pop(0)
    if len(duplet_array) == 1:
        return duplet_array[0]

    elif duplet_array[0][1] = var1[1]:
        var2 = duplet_array.pop(0)
        hash_val = HA0.bytes_to_hex(HA0.hex_to_bytes(var1[0]+var2[0]))
        duplet_array.append(hash_val, (var1[1]+1))
    else:
        hash_val = HA0.bytes_to_hex(HA0.hex_to_bytes(var1[0]+var1[0]))
        duplet_array.append(hash_val, [var1[1]+1])



setup(tree)
        

print(tree_n_lvl)
print(tree[len(tree)-1])

