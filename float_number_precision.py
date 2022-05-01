from ctypes import c_float
from itertools import count, islice
from random import randint


def check(bits: int, gamma: float):
    unit = 2**bits - 1
    for x in range(unit + 1):
        f = c_float((x / unit) ** gamma)
        x_restored = round(f.value ** (1 / gamma) * unit)
        if x != x_restored:
            yield f"{x} -> {f.value} -> {x_restored}"


for bits in [8, 16]:
    for gamma in [1.0, 2.2, 1 / 2.2, 9, 1 / 9]:
        gamma = round(gamma * 100000) / 100000
        print(end=f"{bits:5}b γ={gamma:0.5f} : ")
        errors = list(islice(check(bits, gamma), 5))
        if not errors:
            print("ok")
        else:
            print("FAILURE")
            for error in errors:
                print("\t" + str(error))
bits = 16
for test in count(1):
    gamma = randint(100000 // 9, 100000 * 9)
    print(end=f"\rtest#{test:<3} γ={gamma/100000:0.5f} ")
    errors = list(islice(check(bits, 100000 / gamma), 5))
    if errors:
        print("FAILURE")
        for error in errors:
            print("\t" + str(error))
        input()
