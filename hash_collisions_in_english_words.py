import string
from pathlib import Path

ASCII = "".join(sorted(string.printable[:95]))
SAFE_ASCII = "abcdefghijklmnopqrstuvwxyz0123456789_."
WORDS = (Path(__file__).resolve().parent / "data/words.txt").read_text().splitlines()


def hash(data: str) -> int:
    hash = 0
    for char in data.encode("utf-8"):
        hash = ((hash << 5) - hash + char) & 0xFFFFFFFF
    return hash


hashes = {}
collisions = 0
for word in WORDS:
    hsh = hash(word)
    if hsh in hashes:
        collisions += 1
        equation = f"{word} = {hashes[hsh]} ".ljust(34, "-")
        print(equation + f" with hash={hsh:08X}")
    hashes[hsh] = word

print(collisions, "collisions per", len(WORDS), "words")
