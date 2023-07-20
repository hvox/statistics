from pathlib import Path


def is_hex(s: str):
    return all(char.lower() in "0123456789abcdef" for char in s)


words_path = Path(__file__).resolve().parent / "data/words.txt"
words = words_path.read_text().splitlines()
for i, word in enumerate(w for w in words if is_hex(w) and len(w) > 2):
    integer = int(word, base=16)
    print(f"{i:2}: {word} = {integer}")
