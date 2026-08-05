import string

def strings(filename, min_length=8):
    with open(filename, 'rb') as f:
        data = f.read()
    
    result = []
    current = []
    printable = set(string.printable.encode('ascii'))
    
    for b in data:
        if b in printable:
            current.append(chr(b))
        else:
            if len(current) >= min_length:
                result.append("".join(current))
            current = []
            
    if len(current) >= min_length:
        result.append("".join(current))
        
    for s in result:
        print(s)

if __name__ == "__main__":
    strings("junior_developer.png")
