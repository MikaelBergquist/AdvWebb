import struct
import hashlib

def hex_to_int (s):
    return int(s, 16)
	
	
def int_to_hex (i):
    return hex (i)[2:]
	
	
def bytes_to_int (b):
    return int.from_bytes(b,'big')
	
	
def int_to_bytes (i):
    return bytes (i.to_bytes(10, 'big'))
	
	
def bytes_to_hex (b):
    return b.hex()
	
	
def hex_to_bytes (h):
    if h[1] == "x": h = h[2:]
    if len(h)%2 == 1: h = "0"+h
    if h[1] == "'": 
        h = h[2:-1]
    return bytes.fromhex(h)


def sha1_bytes (byte_array):
    if(type(byte_array)is int):
        byte_array = int_to_bytes(byte_array)
    if(type(byte_array)is str):
        byte_array = hex_to_bytes(byte_array)
    return hashlib.sha1(byte_array).digest()
    
def parse_file (file_path):
    file = []
    with open(file_path, "r") as f:
        for line in f:
            file.append(line.rstrip())
    return file

