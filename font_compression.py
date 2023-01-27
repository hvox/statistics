import zlib
import io
from base64 import b64decode
from math import log2, ceil
import gzip

from PIL import Image

# https://font.gohu.org/
GOHUFONT_PNG = b64decode(
    b"iVBORw0KGgoAAAANSUhEUgAAAXgAAAAeAQMAAAAciZcWAAAABlBMVEUiJDbI0/X2fGT8AAACPElEQVQ4y8XUvYrbQBQF4MsgyBTLcllSqHAxhQoXKVwacTGXgxDGhBCWlC6CSZHS5RbDEFynWESqFCm2SLEPkufIgwQnd8Y/GydrQtLkSEKM5uMwGoTIwnSMoz+FmzFTzT486iU+4uObhpnLqBIvUiVJIjYgxUai3KQkmDroBpL98KHh4JmzRw1cqDqAyFNwnwB0qgC7Tr+sQEzb27e1+SF734/hnqpWQD3hxO4OUKiq+bneFz++9RPS6lXxi3nlmhiLD+Srn/xLHa6Lj7wwP91SIr72ftQ5eJkRKVX+LkXFzc2LxO713m+vuDv088qzS+bhiKyfP+/6Ufo3C5gZX4Xsy/oDfHCVA2fPienj0WNuvqxneNZR3p8JTcwrqjxb1RNPgd8d98dum774eN2aJzKv4pNUIizTelKRckLefxVMBWnTC1n4uV1MZKfSQ5jOpGxkyO93kkD/O/p3fKRTJrXD0YiUvU5O3/yS10RRomyBDTaJgx9TKD4Uz6ee2RPBwsU78x3xwROd82p+aLqqjEmWMpMwW65r5W9RlrOlSO5D+sX7nXcrAIIV+44HYIWVcvG5b0URURjNUI9tmP0MCgSA/dy8RXd9yH0D6WLuzN83HHYe5lPx673f9YG/8pP35rvsu4aVq4PXk/5dH0JZr3YAo+5w8D3Qa+ixXz96873N97rzLYQl+8Qu+zZKOwstRh6XAyS2Gi9am2+T+ZNf1MhN6fvDj85Tjrrjk+x/y3lfvodzEaL1qRf6l/wAwf2p3ZGa0usAAAAASUVORK5CYII="
)


image = Image.open(io.BytesIO(GOHUFONT_PNG))
GOHUFONT_BITS = [0] * image.width * image.height
pixels = image.load()
for y in range(image.height):
    for x in range(image.width):
        GOHUFONT_BITS[x + y * image.width] = pixels[x, y]
GOHUFONT_BYTES = [int("".join(map(str, GOHUFONT_BITS[i: i + 8])), 2) for i in range(0, len(GOHUFONT_BITS), 8)]
GOHUFONT_CHARS = []
for char in range(94):
    char_bits = []
    x0 = char % 47 * 8
    y0 = char // 47 * 15
    for x in range(x0, x0 + 8):
        assert GOHUFONT_BITS[x + (y0 + 14) * image.width] == 0
    for y in range(y0, y0 + 15):
        for x in range(x0, x0 + 8):
            char_bits.append(GOHUFONT_BITS[x + y * image.width])
    GOHUFONT_CHARS.append(char_bits)

# for char in range(94):
#     print("#" * 18, char)
#     for i in range(0, 120, 8):
#         print(end="#")
#         for x in GOHUFONT_CHARS[char][i: i + 8]:
#             print(end=("██" if x else "  "))
#         print("#")
#     print("#" * 18)


def optimized_png_file():
    return 8 * len(GOHUFONT_PNG)


def raw_bitmask():
    return 8 * len(GOHUFONT_BYTES)


def encoding_using_global_probability():
    p = sum(GOHUFONT_BITS) / len(GOHUFONT_BITS)
    bits = p * log2(p) + (1 - p) * log2(1 - p)
    return 4 * 8 - round(bits * len(GOHUFONT_BITS))


def encoding_using_local_probability():
    total = 0
    bit_arrays = [[GOHUFONT_BITS[j] for j in range(i, len(GOHUFONT_BITS), 120)] for i in range(120)]
    for array in bit_arrays:
        p = sum(array) / len(array)
        bits = p * log2(p + 1e-100) + (1 - p) * log2(1 - p + 1e-100)
        total += 4 * 8 + ceil(-bits * len(array))
    return total


def gzip_compress(data):
    return gzip.compress(data, compresslevel=9)


def zlib_compress(data):
    return zlib.compress(data, level=9)


def gzip_compressed_bytes():
    return len(gzip_compress(bytes(GOHUFONT_BYTES))) * 8


def gzip_compressed_bits():
    bit_arrays = [[GOHUFONT_BITS[j] for j in range(i, len(GOHUFONT_BITS), 120)] for i in range(120)]
    rearanged_bytes = []
    for array in bit_arrays:
        byte_array = [int("".join(map(str, array[i: i + 8])), 2) for i in range(0, len(array), 8)]
        rearanged_bytes.extend(byte_array)
    return len(gzip_compress(bytes(rearanged_bytes))) * 8


def gzip_compressed_chars():
    bits = [x for bits in GOHUFONT_CHARS for x in bits]
    data = [int("".join(map(str, bits[i: i + 8])), 2) for i in range(0, len(bits), 8)]
    return len(gzip_compress(bytes(data))) * 8


def zlib_compressed_chars():
    bits = [x for bits in GOHUFONT_CHARS for x in bits]
    data = [int("".join(map(str, bits[i: i + 8])), 2) for i in range(0, len(bits), 8)]
    return len(zlib_compress(bytes(data))) * 8


def zlib_compressed_dense_chars():
    bits = [x for bits in GOHUFONT_CHARS for x in bits[:-8]]
    data = [int("".join(map(str, bits[i: i + 8])), 2) for i in range(0, len(bits), 8)]
    return len(zlib_compress(bytes(data))) * 8


def theoretical_arithmetic_encoding():
    total = 0
    history = [0, 1] * 9
    stats = [1 + sum(history), 1 + sum(1 - x for x in history)]
    for x in GOHUFONT_BITS:
        total += -log2(stats[x] / sum(stats))
        history.append(x)
        stats[x] += 1
        stats[history.pop(0)] -= 1
    return ceil(total)


def theoretical_arithmetic_encoding_per_char():
    total = 0
    history = [0, 1] * 8
    stats = [1 + sum(history), 1 + sum(1 - x for x in history)]
    for x in (x for bits in GOHUFONT_CHARS for x in bits):
        total += -log2(stats[x] / sum(stats))
        history.append(x)
        stats[x] += 1
        stats[history.pop(0)] -= 1
    return ceil(total)


def subglyph_encoding():
    segments = {(), tuple(range(112))}
    for char in GOHUFONT_CHARS:
        char = set(i for i, bit in enumerate(char) if bit)
        new_segments = set()
        for segment in segments:
            new_segments.add(tuple(i for i in segment if i in char))
            new_segments.add(tuple(i for i in segment if i not in char))
        segments = new_segments
    return (len(segments) - 2) * len(GOHUFONT_CHARS)


def rowtable_encoding():
    rows = set()
    for char in GOHUFONT_CHARS:
        for row in (tuple(char[i: i + 8]) for i in range(0, len(char), 8)):
            rows.add(row)
    return log2(len(rows)) * 14 * 94 + len(rows) * 8


def columntable_encoding():
    columns = set()
    for char in GOHUFONT_CHARS:
        for col in (tuple(char[j] for j in range(i, 112, 8)) for i in range(8)):
            columns.add(col)
    return log2(len(columns)) * 8 * 94 + len(columns) * 14


print()
fs = [
    zlib_compressed_dense_chars,
    zlib_compressed_chars,
    gzip_compressed_chars,
    gzip_compressed_bytes,
    optimized_png_file,
    theoretical_arithmetic_encoding,
    theoretical_arithmetic_encoding_per_char,
    gzip_compressed_bits,
    encoding_using_global_probability,
    encoding_using_local_probability,
    raw_bitmask,
    subglyph_encoding,
    rowtable_encoding,
    columntable_encoding,
]
for bits, f in sorted((f(), f) for f in fs):
    name = f.__name__.replace("_", " ").title()
    efficency = round(bits / len(GOHUFONT_PNG) * 12.5)
    eff_str = f"{efficency:4}%"
    if bits <= 8 * len(GOHUFONT_PNG):
        eff_str = f"\x1b[92m{eff_str}\x1b[0m"
    elif bits < 8 * len(GOHUFONT_BYTES):
        eff_str = f"\x1b[93m{eff_str}\x1b[0m"
    else:
        eff_str = f"\x1b[91m{eff_str}\x1b[0m"
    print(f"{eff_str} {name} (bits={bits})")
print()
