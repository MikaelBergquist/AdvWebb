import HA0
from pcapfile import savefile
from pcapfile.protocols.linklayer import ethernet
from pcapfile.protocols.network import ip
import binascii
from functools import reduce

def ip_to_int(ip):
    l = str(ip)[2:-1].split(".")
    l = list(map(lambda x: HA0.int_to_hex(int(x)), l))
    hex = reduce(lambda x, y: x+y, map(lambda x: "00"[len(x):]+x, l))
    return int(hex, 16)   

    
def is_disjoint_all(ri, sets):
    ret = True
    for rj in sets:
        ret = ret and len(ri.intersection(rj)) == 0
    return ret
    
# File parsing
file = HA0.parse_file("nazir.txt")   
[_nazir_ip, _mix_ip, _num_partners, filename] = list(map(lambda x: x.split(": ")[1], file)) 


nazir = ip_to_int("b'"+_nazir_ip+"'")
mix = ip_to_int("b'"+_mix_ip+"'")  
num_partners = int(_num_partners)
testcap = open(filename, 'rb')
capfile = savefile.load_savefile(testcap, verbose = True)

# Create a list of (sender, reciever) as integer for all packets
adresses = []
for i in range(0, len(capfile.packets)):
    eth_frame = ethernet.Ethernet(capfile.packets[i].raw())
    ip_packet = ip.IP(HA0.hex_to_bytes(str(eth_frame.payload)[2:-1]))
    adresses.append((ip_to_int(ip_packet.src), ip_to_int(ip_packet.dst)))


sets = []
disjoint = []
senders = set({})
recievers = set({})
last_source = -1
# Discovery phase
for t in adresses:
    (src, dst) = t
    if mix == dst and mix == last_source:
        if nazir in senders:
            if (is_disjoint_all(recievers, disjoint)):
                disjoint.append(recievers)
                
            else: 
                sets.append(recievers)
        
        senders = set({})
        recievers = set({})
        
    if(src!=mix): senders.add(src)
    if(dst!=mix): recievers.add(dst)
    last_source = src
# need to do this one last time, otherwise last round is missed
if (is_disjoint_all(recievers, disjoint)):
    disjoint.append(recievers)             
else: 
    sets.append(recievers)

# Excluding phase
while sum(map(lambda x: len(x), disjoint)) > num_partners:
    for i in range(0, len(disjoint)):
        all_rj = disjoint.copy() 
        ri = all_rj.pop(i)
        
        for j in range(0, len(sets)):
            r = sets[j]
            if len(ri.intersection(r)) > 0 and is_disjoint_all(r, all_rj):
                disjoint[i] = ri.intersection(r)
print(disjoint)
ip_sum = sum (map(lambda x: sum(x), disjoint))
print (ip_sum)