import math
import numpy as np

def string2number(string: str) -> int:
    bytes = string.encode('utf-8')
    return int.from_bytes(bytes, 'little')

def number2string(number: int) -> str:
    if not isinstance(number, int):
        number = int(number)
    
    bytes = number.to_bytes((number.bit_length() + 7) // 8, 'little')
    return bytes.decode('utf-8')

def hash2number(hash: str) -> int:
    # print("hash2number()", "hash:", hash, "num:", int(hash, 16))
    return int(hash, 16)

def number2hash(number: int) -> str:
    # print("number2hash()", "got:", number, "hex:", hex(number), "aaa:", hex(number)[2:])
    return hex(number)[2:]

def getHEMaxBits(HE):
    # floor was used, since cannot use numbers > t
    return math.floor(math.log2(HE.t / 2 - 1))

def numberIntoArray(number: int, max_bits):
    ret = []
    while number > 0:
        ret += [number & ((1 << max_bits) - 1)]
        number >>= max_bits
    return np.array(ret, dtype=np.int64)

def arrayIntoNumber(arr, max_bits):
    arr = arr.tolist()
    arr.reverse()
    
    ret = 0

    for s in arr:
        ret <<= max_bits
        ret |= s
    
    return ret
