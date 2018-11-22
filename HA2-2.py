import HA0
from pcapfile import savefile
from pcapfile.protocols.linklayer import ethernet
from pcapfile.protocols.network import ip
import binascii
from functools import reduce


testcap = open('cia.log.1337.pcap', 'rb')
capfile = savefile.load_savefile(testcap, verbose=True)

def ip_to_int(ip):
    l = str(ip)[2:-1].split(".")
    l = list(map(lambda x: HA0.int_to_hex(int(x)), l))
    hex = reduce(lambda x, y: x+y, map(lambda x: "00"[len(x):]+x, l))
    return int(hex,16)

mix_ip = b'85.14.156.21'


#for i in range(0, 1): #len(capfile.packets)):
#    eth_frame = ethernet.Ethernet(capfile.packets[i].raw())
#    ip_packet = ip.IP(binascii.unhexlify(eth_frame.payload))

eth_frame = ethernet.Ethernet(capfile.packets[0].raw())
ip_packet = ip.IP(binascii.unhexlify(eth_frame.payload))

print(ip_packet.src)

print(ip_to_int(mix_ip))