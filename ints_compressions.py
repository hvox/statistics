import random
from math import ceil, log2, exp
import zlib
from itertools import count, islice

MESSAGE_SIZE = 100 * 1024
PROBABILITIES = [3, 369, 235, 156, 268, 4, 695, 639, 1, 257, 10, 1, 999, 189, 1, 1]


def random_values(probabilities=PROBABILITIES, seed=12345):
    random.seed(12345, version=2)
    samples = list(range(len(probabilities)))
    for _ in count():
        yield from random.choices(samples, probabilities, k=1024)


def raw_bytes(probabilities: list[int]):
    return MESSAGE_SIZE


def zipped_bytes(probabilities: list[int]):
    data = bytes(islice(random_values(probabilities), MESSAGE_SIZE))
    compressed = zlib.compress(data, level=9)
    return len(compressed)


def raw_halfbytes(probabilities: list[int]):
    return (MESSAGE_SIZE + 1) // 2


def zipped_halfbytes(probabilities: list[int]):
    values = list(islice(random_values(probabilities), MESSAGE_SIZE))
    data = bytes(x1 + 16 * x2 for x1, x2 in chunked(values, 2))
    return len(zlib.compress(data, level=9))


def arithmetic_encoding(probabilities: list[int]):
    total = 0
    for x in islice(random_values(probabilities), MESSAGE_SIZE):
        total += -log2(probabilities[x] / sum(probabilities))
    return ceil(total / 8)


def chunked(iterable, n: int):
    it = iter(iterable)
    while chunk := list(islice(it, n)):
        yield chunk


settings = {
    "uniform distribution": [99] * 16,
    "marginal distribution": PROBABILITIES,
    "normal distribution": [round(round(exp(-abs(i - 7.6)) * 2000)) for i in range(16)],
}
fs = [
    raw_bytes,
    zipped_bytes,
    raw_halfbytes,
    zipped_halfbytes,
    arithmetic_encoding,
]
print()
for name, probabilities in settings.items():
    print(f"{name} {probabilities}:")
    for size, _, f in sorted((f(probabilities), -i, f) for i, f in enumerate(fs)):
        name = f.__name__.replace("_", " ").title()
        efficency = round(size / MESSAGE_SIZE * 100)
        eff_str = f"{efficency:4}%"
        if size <= (MESSAGE_SIZE) // 2:
            eff_str = f"\x1b[92m{eff_str}\x1b[0m"
        elif size < (MESSAGE_SIZE):
            eff_str = f"\x1b[93m{eff_str}\x1b[0m"
        else:
            eff_str = f"\x1b[91m{eff_str}\x1b[0m"
        print(f"{eff_str} {name} [{size} bytes]")
    print()
