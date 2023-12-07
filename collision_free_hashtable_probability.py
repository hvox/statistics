from math import trunc, log2, ulp
from os import get_terminal_size


def hash_table_collisions(table_size: int, elements: int):
    p = 1
    for i in range(elements):
        p *= (table_size - i) / table_size
    return p if trunc(p * 100) != 100 or elements == 1 else (p - ulp(p))


cols = (get_terminal_size().columns - 5) // 4
print("     " + " ".join(f"{x:3}" for x in range(1, cols + 1)))
colors = ["\x1b[91m", "\x1b[93m", "\x1b[92m", "\x1b[96m", "\x1b[96m"]
for i in range(1, max(10, get_terminal_size().lines - 1)):
    # table_size = round(i + 1.1958550179684941**i)
    table_size = max(1 + i, round(2 ** ((i + 2) / 4)))
    row = []
    for elements in range(1, min(table_size + 1, cols + 1)):
        p = hash_table_collisions(table_size, elements)
        # if i % 2 == 0:
        #     p = 1
        #     for k in range(elements, table_size+1):
        #         p *= 1 - hash_table_collisions(k, elements)
        #     p = 1 - p
        row.append(f"{trunc(p*100):3}%")
    row += ["  0%"] * (cols - len(row))
    row = [colors[int(x[:-1]) // 25] + x + "\x1b[0m" for x in row]
    table_size_str = f"{table_size:3}: " if table_size < 1000 else f"2^{log2(table_size):0.1f}: "
    for _ in range((len(table_size_str) - 5 + 3) // 4):
        row.pop(0)
    table_size_str = table_size_str.ljust(5 + (cols - len(row)) * 4)
    print(table_size_str + "".join(row))
