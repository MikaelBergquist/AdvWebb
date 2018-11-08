import struct

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
	
	

print ("hex2int:", hex_to_int ("fedcba9876543210"))
print ("int2hex:", int_to_hex (18364758544493064720))
print ("bytes2int:", bytes_to_int (bytearray(b'\x00\x00\x01\xf4')))
print ("int2bytes:", int_to_bytes (500), int_to_bytes(-500))
print ("bytes2hex:", bytes_to_hex (bytearray(b'\x00\x00\x01\xf4')))
print ("hex2bytes:", hex_to_bytes ("0a"))
print (bytes_to_hex(hex_to_bytes ("0a")))