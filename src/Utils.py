def string2number(string: str) -> int:
    bytes = string.encode('utf-8')
    return int.from_bytes(bytes, 'little')

def number2string(number: int) -> str:
    if not isinstance(number, int):
        number = int(number)
    
    bytes = number.to_bytes((number.bit_length() + 7) // 8, 'little')
    return bytes.decode('utf-8')

def hash2number(hash: str) -> int:
    print("hash2number()", "hash:", hash, "num:", int(hash, 16))
    return int(hash, 16)

def number2hash(number: int) -> str:
    print("number2hash()", "got:", number, "hex:", hex(number), "aaa:", hex(number)[2:])
    if hex(number)[0] == '-':
        return hex(number)[3:]
    return hex(number)[2:]

def splitNumberInto15bits(number: int):
    ret = []

    while number > 0:
        ret += [number & 0b111111111111111]
        number >>= 15
    
    return ret

def getNumberFromSplittedInto15bits(splitted) -> int:
    splitted = list(splitted.ravel())
    splitted.reverse()
    
    ret = 0

    for s in splitted:
        ret <<= 15
        ret |= s
    
    return ret
