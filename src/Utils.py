import copy
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
    return int(hash, 16)

def number2hash(number: int) -> str:
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

def pow(x, n):
    leftPowers = n

    currentPower = 0
    xs = {
        1: copy.copy(x)
    }

    leftPowers -= 1
    currentPower += 1

    ret = copy.copy(xs[1])

    while leftPowers > 0:
        iterPower = 1

        for tmpPower in sorted(xs.keys(), reverse=True):
            if leftPowers >= tmpPower:
                iterPower = tmpPower
                break

        ret *= xs[iterPower]
        ret = ~ret

        leftPowers -= iterPower
        currentPower += iterPower

        # add new x to xs
        xs[currentPower] = copy.copy(ret)
    
    return ret

def areCtxtsEqual(a, b, encrypted_one, HE_t):
    ret = pow(a - b, HE_t - 1)
    ret = -ret + encrypted_one

    return ret

def sumVector(v, slots):
    ret = copy.copy(v)
    a = copy.copy(v)

    print(slots)
    for i in range(slots - 1):
        if i % 10 == 0:
            print(i)
        a >>= 1
        ret += a
    
    return ret