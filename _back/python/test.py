__author__ = 'alex'
import struct
import array

#
# a = -8100
#
# b = struct.pack('>h', a)
# print bin(a)
# # print bin(int(hex(ord(b[0])), base=16)), int(hex(ord(b[0])), base=16)
# # print bin(int(hex(ord(b[1])), base=16)), int(hex(ord(b[1])), base=16)
# # print ''
# f = (a >> 7) & 127
# s = 127 & a
# print bin(f), f
# print bin(s), s
#
# k = (f << 7) + s
# if k & 2 ** 13:
#     k = k - 2 ** 14
# print bin(k), int(bin(k), 2)

print ([elem.encode("hex") for elem in 'ololo'])

# for i in range(128):
#     print chr(i)