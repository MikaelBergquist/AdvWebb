import HA0
in_sa = "27C2"
in_sb = "0879"
in_da = "35F6"
in_db = "1A4D"
in_m = "27BC"
in_b = "1"

sa = HA0.hex_to_int(in_sa)
da = HA0.hex_to_int(in_da)
sb = HA0.hex_to_int(in_sb)
db = HA0.hex_to_int(in_db)
m = HA0.hex_to_int(in_m)
b = HA0.hex_to_int(in_b)

if(b == 0):
    broadcasted = HA0.int_to_hex(sa^sb)
    message = HA0.int_to_hex(sa^sb^da^db)
    print(broadcasted+message)
if(b == 1):
    broadcasted = HA0.int_to_hex(sa^sb^m)
    broadcasted = "0000"[:4-len(broadcasted)] + broadcasted
    print(broadcasted)
    
    