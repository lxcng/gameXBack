__author__ = 'alex'
import struct
import array
import time
#
a = -8100
#
# start = time.time()
# for i in range(10000):
b = struct.pack('>h', a)
# print type(b)
#     a += 1
# print time.time() - start
# print bin(int(hex(ord(b[0])), base=16)), int(hex(ord(b[0])), base=16)
# print bin(int(hex(ord(b[1])), base=16)), int(hex(ord(b[1])), base=16)
# print type(b.encode())

start = time.time()

ba = bytearray(2)
# for i in range(10000):
struct.pack_into('>h', ba, 0, a)
    # a += 1
# print time.time() - start
print bin(ba[0])
print bin(ba[1])
print ba[0]
print ba[1]
# # print ''
# f = (a >> 8)
# s = 127 & a
# print bin(f), f
# print bin(s), s
#
# k = (f << 7) + s
# if k & 2 ** 13:
#     k = k - 2 ** 14
# print bin(k), int(bin(k), 2)

# print [elem.encode("hex") for elem in 'ololo']

# for i in range(128):
#     print chr(i)
def to_bytes(a):
    pass