#execfile('/root/SCALE-MAMBA/Programs/ring/ring.mpc')
from ring import Ring

p = 340282366920938463463374607431768211507

w = 216409912179401900965416891955038263635**16


n=512
lgN = 9
r = Ring(lgN, w)


testi = 0

print("--------------------------------------------------")
print("Test : reverse", testi)
testi = testi + 1

x = 6
nBitsx = 3
y = r.bitRev(x,3)

print("Expected: 3")
print("Actual:  ", y)

print("--------------------------------------------------")
print("Text : mod", testi)
testi = testi + 1

x = 2
y = 4
#if_then(x % 2)
if (x%2):
    y = 7
else:
    y = 9
y = 9

print("Expected: 9")
print("Actual:  ", y)


print("--------------------------------------------------")
print("Test : cint exponentiation", testi)
testi = testi + 1

x = 3
y = 6
nBitsY = 3

z = r.cPow(x, y, nBitsY)

print("Expected: 729")
print("Actual:  ", z)

print("---------------------------------------------------")
print("Test : getWExp", testi)
testi = testi + 1

n8 = 8
lgN8 = 3
w8 = w**64
r8 = Ring(lgN8, w8)


for d in range(lgN8):
  for i in range(n8):
    print("  ", r8.getWExp(d, i))
  print("")


print("--------------------------------------------------")
print("Test : checkW", testi)
testi = testi+1

neg1 = w8 ** n8
print("Expected:  ", -1)
print("Actual:  ", neg1)


# print("--------------------------------------------------")
# print("Test : c table", testi)
# testi = testi + 1
#
# n4 = 4
# lgN4 = 2
# w4 = w8 ** 2
# r4 = Ring(lgN4, w4)
#
#
# print("Expected:")
# # print("        ", w4, w4, w4**3, w4**3)
# # print("        ", w4**2, w4**2, w4**2, w4**2)
#
# print("Actual:")
# # @for_range(lgN4)
# # def findCRow(k):
# # for k in range(lgN4):
# #   # @for_range(n4)
# #   # def findCPow(i):
# #   for i in range(n4):
# #     print("  ", r4.cPow(w4, r4.getWExp(k, i), lgN4))
# # print("")
#
#
# print("---------------------------------------------------")
# print("Test : if cint", testi)
# testi = testi+1
#
# vTrue = 7
# vFalse = 8
# print("Expected:  ", vFalse)
# x = 1
# #if_then (x == cint(0))
# if (x == 0):
#     print("Actual:  ", vTrue)
# else:
#     print("Actual:  ", vFalse)
#
# print("---------------------------------------------------")
# print("Test : fastMult", testi)
# testi=testi+1
#
# a = [0 for i in range(4)]
# b = [0 for i in range(4)]
# for i in range(4):
#   a[i] = i
#   b[i] = i
#
# c = r4.ringMulFast(a, b)
# d = r4.ringMul(a, b)
#
# print("Expected:")
# for i in range(n4):
#   print(d[i])
# print("")
# print("Actual:")
# for i in range(n4):
#   print(c[i])
# print("")
#
# print("---------------------------------------------------")
# print("Test : fastMultMed", testi)
# testi = testi+1
#
# a = [0 for i in range(n)]
# b = [0 for i in range(n)]
# for i in range(n):
#   a[i] = i
#   b[i] = 1
#
# c = r.ringMulFast(a, b)
#
# # Since b is a 1-vector, the last elem of c should be the sum
# # of elems of a
# print("Expected:  ", (n-1)*n/2)
# print("Actual: ", c[n-1])
#
# print("----------------------------------------------------")
