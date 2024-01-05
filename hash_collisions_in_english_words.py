import string
from pathlib import Path
from random import sample, shuffle
from typing import Literal

ASCII = "".join(sorted(string.printable[:95]))
SAFE_ASCII = "abcdefghijklmnopqrstuvwxyz0123456789_."
WORDS = (Path(__file__).resolve().parent / "data/words.txt").read_text().splitlines()


def hash(data: str) -> int:
    hash = 0
    for char in data.encode("utf-8"):
        hash = ((hash << 5) - hash + char) & 0xFFFFFFFF
    return hash


hashes = {0: ""}
collisions = 0
for word in WORDS:
    hsh = hash(word)
    if hsh in hashes:
        collisions += 1
        equation = f"{word} = {hashes[hsh]} ".ljust(34, "-")
        print(equation + f" with hash={hsh:08X}")
    hashes[hsh] = word

print(collisions, "collisions per", len(WORDS), "words")


def test_collisions_with_empty_string():
    for i, prefix in enumerate(WORDS):
        msg = "searching for collisions with empty string"
        print(f" \r{msg}: {i*len(WORDS)}", flush=True, end=" ")
        for suffix in WORDS:
            s = prefix + "-" + suffix
            if not hash(s):
                print(f"\r\x1b[91m FOUND \"{s}\"!\x1b[0m" + " " * len(msg))


def are_collision_free(words: list[str], hash_size: Literal[1, 2] = 1):
    hashes = {hash(word) for word in words}
    if len(hashes) < len(words):
        return False
    for p in reversed(range(len(hashes), 256**hash_size + 1)):
        if len({h % p for h in hashes}) == len(hashes):
            return True
    return False


def get_collision_free_prefix(words: list[str], hash_size: int = 1):
    hashes = [hash(word) for word in words]
    max_prefix = 0
    for module in range(2, 256**hash_size + 1):
        prefix_hashes = set()
        for hsh in (hash % module for hash in hashes):
            if hsh in prefix_hashes:
                break
            prefix_hashes.add(hsh)
        max_prefix = max(max_prefix, len(prefix_hashes))
        if max_prefix == len(hashes):
            break
    return max_prefix


def test_max_safe_amount_of_elements(hash_size: int):
    results = []
    TESTS = 10**4
    for test in range(1, TESTS + 1):
        words = sample(WORDS, 256**hash_size)
        shuffle(words)
        assert len(set(words)) == 256**hash_size
        n = get_collision_free_prefix(words, hash_size)
        results.append(n)
        results = list(sorted(results))
        avg = sum(results) / len(results)
        mid = (results[len(results) // 2] + results[(len(results) + (len(results) > 1)) // 2]) / 2
        p90 = results[len(results) // 10]
        p99 = results[len(results) // 100]
        msg = f"\rtests={test} {avg=:.1f} mid={round(mid)} {p90=} {p99=} min={results[0]} max={results[-1]}"
        print(msg, flush=True, end=" \n"[test == TESTS])


# test_collisions_with_empty_string()
test_max_safe_amount_of_elements(hash_size=1)
