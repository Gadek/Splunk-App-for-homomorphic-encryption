import numpy as np

from src.operations.GroupAndCountOperation import GroupAndCountOperation, GroupAndCountResult
import src.Utils as Utils

class IpGroupAndCountResult(GroupAndCountResult):
    def __init__(self, prefix, result):
        self.prefix = prefix
        super().__init__(result)

    def decrypt(self, HE):
        max_bits = Utils.getHEMaxBits(HE)
        
        decryptedPrefix = Utils.number2string(
            Utils.arrayIntoNumber(
                HE.decrypt(self.prefix),
                max_bits
            )
        )

        super().decrypt(HE)

        for ip_int in self.result:
            ip_str = self.__int2ip(ip_int)
            ip_str = f'{decryptedPrefix}.{ip_str}'
            self.result[ip_str] = self.result.pop(ip_int)

    def __int2ip(self, i):
        parts = []
        
        i = np.array([i], dtype=np.ushort)[0]

        while i > 0:
            parts += [str(i & 0xff)]
            i >>= 8
        
        if len(parts) == 0:
            parts = [str(0), str(0)]
        elif len(parts) == 1:
            parts += [str(0)]
        
        return '.'.join(reversed(parts))

class IpGroupAndCountOperation(GroupAndCountOperation):
    def __init__(self, data = []):
        self.prefix = self.__getPrefix(data)

        if self.prefix is None:
            print("ERROR")
            print("IP addresses have to have the same first 2 octets!")
            raise Exception("IP addresses have to have the same first 2 octets!")

        super().__init__(
            list(
                map(
                    lambda x: self.__ip2int(
                        self.__removePrefixFromIP(x)
                    ),
                    data
                )
            )
        )
    
    def __getPrefix(self, data):
        prefix = None
        for currIP in data:
            currIPPrefix = self.__splitIP(currIP)[0]

            if prefix is None:
                prefix = currIPPrefix
            else:
                if currIPPrefix != prefix:
                    return None
        
        return prefix
    
    def __removePrefixFromIP(self, ip):
        return self.__splitIP(ip)[1]
    
    def __splitIP(self, ip):
        ipSegments = ip.split('.')

        if len(ipSegments) != 4:
            raise Exception(f"IP have to have 4 octets! Invlaid IP: {ip}")
        
        return [
            f'{ipSegments[0]}.{ipSegments[1]}',
            f'{ipSegments[2]}.{ipSegments[3]}'
        ]
    
    def __ip2int(self, ip):
        ip = ip.split('.')

        if len(ip) > 2:
            raise Exception("Only 2 octets of IP are supported!")

        ret = 0

        for x in ip:
            ret <<= 8
            ret |= int(x)

        return ret
    
    def encrypt(self, HE):
        max_bits = Utils.getHEMaxBits(HE)

        self.prefix = HE.encrypt(
            Utils.numberIntoArray(
                Utils.string2number(self.prefix),
                max_bits
            )
        )

        super().encrypt(HE)
    
    def run(self) -> IpGroupAndCountResult:
        res = super().run()

        return IpGroupAndCountResult(self.prefix, res.result)
