#!/bin/env python2

import string
import random
from Crypto.Util.number import inverse, long_to_bytes

dict = string.ascii_letters + string.digits + '{}_@$!'


def load64(b):
    return sum((b[i] << (8*i)) for i in range(8))


def pad(x, n):
    # n = 16
    x = hex(x).lstrip('0x').strip('L')
    return '0'*(n - len(x)) + x


def ACAC(x):
    assert x < 2**64
    #print(1, x)
    x ^= x >> 27
    #print(2, x)
    x *= 0x2a636f7468616e2b
    x &= 0xffffffffffffffff
    #print(3, x)
    x ^= x >> 34
    #print(4, x)
    x *= 0x49534954445455c9
    x &= 0xffffffffffffffff
    #print(5, x)
    x ^= x >> 23
    return x

def rev3(x, shr):
    a = x >> 64 - shr
    #print(bin(a))
    b = (x % (1 << 64 - shr)) >> 64 - 2 * shr
    #print(bin(b))
    b ^= a
    #print(bin(b))
    c = x % (1 << 64 - 2 * shr)
    c ^= b >> 3 * shr - 64
    #print(bin(c))
    return (a << 64 - shr) | (b << 64 - 2 * shr) | c

def rev2(x, shr):
    a = x >> 64 - shr
    #print(bin(a))
    b = x % (1 << 64 - shr)
    b ^= x >> shr
    #print(bin(b))
    return (a << 64 - shr) | b

#x * m % (2 ^ 64) = y
def rev_mul(x, m):
    return x * inverse(m, 1 << 64) % (1 << 64)

def encode(flag):
    result = ''
    print(len(flag)-8)
    for i in range(0, len(flag), 8):
        print(i, flag[i:i+8])
        result += pad(ACAC(load64(flag[i:i+8])), 16)
        print(result)
    return result


if __name__ == "__main__":
    data = 'testtesttesttest'
    print(load64(b'testtest'))

    # You know what this mean, right?
    data = list(data)
    print(data)
    for i, j in enumerate(data):
        if j not in dict:
            data[i] = chr(random.randint(0x7f, 0xff))
    print(data)
    #data = bytearray(data)

    data = b'testtesttesttest'
    data = b'_tru3}  '
    cipher = encode(data)

    print(cipher)

def rev(x):
    #x = 0x4985ac600805a7fc
    #print(x)
    x = rev3(x, 23)
    #print(x)
    x = rev_mul(x, 0x49534954445455c9)
    #print(x)
    x = rev2(x, 34)
    #print(x)
    x = rev_mul(x, 0x2a636f7468616e2b)
    #print(x)
    x = rev3(x, 27)
    #print(x)
    return long_to_bytes(x)[::-1]

#rev(0x4985ac600805a7fc)
print(rev(0xb567c3a7da2cd244))

cipher = 'f29dccd7c48ac587c11ca4036e9bf45e0c28fcec3bd8d783ff87f9574bcb9a73d1c7225fddbd976ea3ee0145efe8b7fb65b9f80781fbbc48b001ec256dee4af31e237cbb3af4ab16fafbeff4b27f9e0a1cfa4f2b2c5a0b56a57ef6349b391070ab6885cce5ce5d4823224b5a92f33be3515eddc8efbcf0ffe7bb82f263a8004d7a33be3f1875c75689df2cf3a4d27e8ea7da07acfe24b2ef682999cfca0a1a4eefd40950f9306cc97d6a533b6c9c1d97fc5a1d7d51f76b172ce875a476c97021cf83c028c53143ec53a3020ab0423289df550b44b828a2a457e47f7f51d35db28ad80a32177dc3cf9a17402b966d9c86fa888de9ba816818a72f5e7a990aa0a0b23ee0743ba57fb73b174905584617a7dfe7a329521620260fc853ce8beb806dfb82837cdcc8eb2f010687d76f6be8919139ff344e68f9d55a88ba3672ce8bc926974488e2dd9993b290d6b3199fcf86991004383a021bbe24aba2f01dd2a314604a2471394e88ba855afc359f742af947334654215bf4f1a29d30f1d098391762b9311fc8f405c19b98e111087bf44e2297f19406805eaf95328dabd4f43a6f27a8b8e1da1f3e23e228c6f494c344c1d969c2172ae90bdc04a14591bdb51ca5937f3a7720b9e3f2bcca7ac00e34f7ad24c842378738c60586a962adc55a6b3cf8fec3a9f87cdc3b5d994391b1d140b50275166bbd92b7bc43cf4937189ed5aaf901d06335aa023962365a0ec43d59c3d1c7225fddbd976edcec76577e49dae72ad5aaa240fe663aa5c39da125752368f85429fbc32ac89dd6e8fe5dba5f24d81d08c66f1aef25b6eb42f3c3515c8b915290013bf822d41d7069cca0d9643e3a27366d09b29591e88cb6ea5b2b6713932db8fa6da6d5f460b4f6c26702892124a34450ab29be32a4206696ed21feb3af185392d104c830b1028c8ef533439090e8b31d541832e618477a2dac3136cd2bf4ff499e562b8f8182f71688cf623226d8f0e25e5031e46595ec38dc5864dad4e4f6e0df30e91a81f3e515368ecfdcd6bc620ba01112215e9679c18004a10192beb6ec7faf4a8d92b567c3a7da2cd2448042af8155c06eb6ae30df318e70522e523bae7b4169cbbcf051402f3a5171ebf86523a57e51cb28397f87d611de4f9d296e4f7670b24c67e7714d718b9b85b650f8e0475290d61f84a855e40831733fee07cba2c02b27c187796e076bfe33b1b374898944c67abd3213f538cb6fbd32b0e67b4d9ac9c8ac9be9fe0859593cff3050de90b20466851d5430001c52823990d691cdb10e49537060b80bdb11c6c1951918c7c2af31b05fc0a34edf00ad6038a4a1c21f44dcea46be833ea2ef25e01ec5dd3cb0f2d654774d0d3ac01cbabebacccfa42b1ca22edb8270e4434f555966d3eeddba92c5ebe5b2f9ac816f92e98aff5d5e8893839f83fdbee3a9b2d9cfb94699318d702c02710de4f880b3efd9d98e8c85da394842ec38b451e4a0905d039dc43b95ed1e7013b0e8821b13db44654f82202d768daf1360af1c079bd44a345f428e46c9fd6118d6c4454c8275d9492edfee8a71bc7556e0caffdbc74c874bbff8f938da8a130559c49db773d094717f32fd907c3c1d6ba6e77d67287e3045544c2d3b804a0d2127e90aec36eb84e2538544858e8d337da7e2ec77fbaa09fecfd5a20fb24b2aaae3b6216d76fe4d9ef493246aac3a2fd7957ae70fb5d42aa827a14580610885d32efa0927db49eb1b70d28b1c2109da853ebf97e3487117207e8f10a4ee25542e4520bf7929331ee476cc43d5702e19a4fd19c21d49de0218282638a66f9c1ec98ce7bcb5cef7b1e7255cdc7cfbf4fc130410bbb9b1c5413ab6787c693ae022e304e532e56e3a07d7a0eb0187097b9007d2ff96aa5c7d853c431fd8c78ed2968b77ecbb5a8246b3e1d6a9b9ae830d39d3d19d473f748c834357817959e7e33e46ee75b2d92fceda0034dde1122bfac63baac95f3eca2735ac452c6b7027fb28fad326dbafff2f62c2efd365f84e2555bc236687a52d8b1a79e50adfbba68b2cc60c1005cf9a4d538a4dd22c54d266830ca5da2b55cadf18b63909363f91a87edb98c45f24c5329106048fb68c7fcae6e9cf40ebd221f144d88cc6ae1fe10df6181f5aaf6ebb3805eaa66a42e9079e216da3aee702bcb83edc54e4d91bb88bd1de95ea5dd23e8883dd408f042490e67b05f2e2b86ff13c2161e92f184f814e8a4e68ec6a173166dcd828c4940782ade04d1df147b6e7d74d5bc226ef582e55e92bf7183d046ee8016d860b5b8e5bcaa694775995d2104ec1d986c2b084bae25cf36276b83edc666a93bfb903e8b423234e4fa0454d3b9c63bc35033734ce8c02ed143c6ee202bb3bab4b88ea947e8b54473439d35b7c6dbb00a2e04ee69abd3333d23c063c88471cffafcf876ac9f37422bd5c99f782c0c3bf2539321a01d52511cdc82c0122b78616aede169c2a1c428d8fd8543e00816b59fa5aa07ba7e65bf47e768e14197d3a2a4b6a9db3f58f9fb82fa3b6179d43146f7f8d3c84e94f0e5f2f9e45ab3719dedaef3d5ec5677a2eee57c5cb8dadd39e7c1575f60135acff87870fac4d795143e7656a24fad702f704661efaa38a15201cad39428c151044e1cfea9b134f14286b329da7785380d5'
pt = b''
for x in range(0, len(cipher), 16):
    ct = cipher[x:x+16]
    ct = int(ct, 16)
    r = rev(ct)
    #print(r, cipher[x:x+16])
    pt += r
print(pt)
result = ''
for i, j in enumerate(pt):
    #print(i, j)
    if j >= 0x20 and j <= 0x7f:
        result += chr(pt[i])
    else:
        result += ' '
print(result)
