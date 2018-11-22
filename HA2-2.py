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

adresses = []
for i in range(0, len(capfile.packets)):
    eth_frame = ethernet.Ethernet(capfile.packets[i].raw())
    ip_packet = ip.IP(binascii.unhexlify(eth_frame.payload))
    adresses.append((ip_to_int(ip_packet.src), ip_to_int(ip_packet.dst)))

print(adresses)