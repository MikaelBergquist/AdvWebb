import struct
import hashlib

def hex_to_int (s):
    return int(s, 16)
	
	
def int_to_hex (i):
    return hex (i)
	
	
def bytes_to_int (b):
    return struct.unpack(">i", b)[0]
	
	
def int_to_bytes (i):
    return struct.pack(">i", i)
	
	
def bytes_to_hex (b):
    return b.hex()
	
	
def hex_to_bytes (h):
    return bytearray.fromhex(h)


def sha1_byte(byte_array):
    if(type(byte_array)is int):
        byte_array = int_to_bytes(byte_array)
    if(type(byte_array)is str):
        byte_array = hex_to_bytes(byte_array)
    return hashlib.sha1(byte_array).digest()
