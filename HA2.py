import HA0

_sa = "27C2"
_sb = "0879"
_da = "35F6"
_db = "1A4D"
_m = "27BC"
_b = "1"

file = list(map(lambda x: str.split(x)[1], HA0.parse_file("dc.txt")))
[_sa, _sb, _da, _db, _m, _b] = file

sa = HA0.hex_to_int(_sa)
da = HA0.hex_to_int(_da)
sb = HA0.hex_to_int(_sb)
db = HA0.hex_to_int(_db)
m = HA0.hex_to_int(_m)
b = HA0.hex_to_int(_b)

if(b == 0):
    broadcasted = HA0.int_to_hex(sa^sb)
    message = HA0.int_to_hex(sa^sb^da^db)
    print(broadcasted+message)
if(b == 1):
    broadcasted = HA0.int_to_hex(sa^sb^m)
    broadcasted = "0000"[:4-len(broadcasted)] + broadcasted
    print(broadcasted)
    
    