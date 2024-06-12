import os
import hashlib
from time import monotonic as get_current_time


def simple_multiplication_modulo(x, y):
    return (x + 1) * (y + 1) % 65537 % 257 % 13


def bryc_hash(x, y):
    x = 0xDEADBEEF ^ x
    y = 0x41C6CE57 ^ y
    x = (x ^ (x >> 16)) * 2246822507 % 2**32
    x ^= (y ^ (y >> 13)) * 3266489909 % 2**32
    y = (y ^ (y >> 16)) * 2246822507 % 2**32
    y ^= (x ^ (x >> 13)) * 3266489909 % 2**32
    return (4294967296 * (2097151 & y) + x) // 65537


def sha3(x: int, y: int):
    x = x.to_bytes(2, "little")
    y = y.to_bytes(2, "little")
    return hashlib.sha384(x + y).digest()[0]


def squirrel_eiserloh_noise_v5(x, y):
    SQ5_BIT_NOISE1 = 0xD2A80A3F
    SQ5_BIT_NOISE2 = 0xA884F197
    SQ5_BIT_NOISE3 = 0x6C736F4B
    SQ5_BIT_NOISE4 = 0xB79F3ABB
    SQ5_BIT_NOISE5 = 0x1B56C4F5
    mangledBits = x + (y << 16)
    mangledBits *= SQ5_BIT_NOISE1
    mangledBits ^= mangledBits >> 9
    mangledBits += SQ5_BIT_NOISE2
    mangledBits ^= mangledBits >> 11
    mangledBits *= SQ5_BIT_NOISE3
    mangledBits ^= mangledBits >> 13
    mangledBits += SQ5_BIT_NOISE4
    mangledBits ^= mangledBits >> 15
    mangledBits *= SQ5_BIT_NOISE5
    mangledBits ^= mangledBits >> 17
    return mangledBits


def mine(x: int, y: int):
    bits = x + y * 0x741D6837
    for _ in range(2):
        bits *= 0x6C736F4B
        bits ^= bits >> 9
    return bits


def show_braille_pattern(grid: list[list[object]]):
    def get(x: int, y: int) -> bool:
        return bool(grid[y][x] if y < len(grid) and x < len(grid[y]) else 0)

    for y in range(0, len(grid), 4):
        row: list[str] = []
        for x in range(0, len(grid[y]), 2):
            character_code = (
                get(x, y)
                + (get(x + 0, y + 1) << 1)
                + (get(x + 0, y + 2) << 2)
                + (get(x + 1, y + 0) << 3)
                + (get(x + 1, y + 1) << 4)
                + (get(x + 1, y + 2) << 5)
                + (get(x + 0, y + 3) << 6)
                + (get(x + 1, y + 3) << 7)
            )
            row.append(chr(0x2800 + character_code))
        print("".join(row))


for generator in [
    simple_multiplication_modulo,
    bryc_hash,
    sha3,
    squirrel_eiserloh_noise_v5,
    mine,
]:
    name = " ".join(w.capitalize() for w in generator.__name__.split("_"))
    w, h = os.get_terminal_size()
    t0 = get_current_time()
    grid = [[generator(x, y) % 2 for x in range(2 * w)] for y in range(4 * (h - 2))]
    dt = get_current_time() - t0
    balance = sum(sum(2 * x - 1 for x in row) for row in grid) / sum(map(len, grid))
    print(f"\n  {name:{w-14}} {round(100*balance)}%  {dt:.3f}")
    show_braille_pattern(grid)
