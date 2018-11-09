import HA0

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