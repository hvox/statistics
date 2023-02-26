import contextlib
import subprocess

ASCII = " !}\"#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~"
PUNCTUATION = "®°·‑–—−•…"
MATH = "¬±²³µ×÷"
GREEK = "αβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ"
ENGLISH = ASCII
FRENCH = "«»ÀÉàâäæçèéêëíîïñóôöùûüćœί‘’“”€"
ITALIAN = "§«º»ÁÈàäæèéìòùüōəɛɪί’“”"
GERMAN = "ÄÖÜßäæéöüł‘’‚“„"
SPANISH = "«»¿ÑÁáæéíñóúüə‘“”"
PORTUGUESE = "§«º»ÁÉàáâãæçéêíñóôõöúί’“”"
TURKISH = "nÇÖâæçîöüğİıŞş’“”"
RUSSIAN = "«»АБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяё’“„"
UKRAIN = "ЄІЇАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЮЯабвгдежзийклмнопрстуфхцчшщьюяєіїҐґ"
BELARUSIAN = "ЁІЎАБВГДЕЖЗЙКЛМНОПРСТУФХЦЧШЫЬЭЮЯабвгдежзйклмнопрстуфхцчшыьэюяёіў"
EFIGS = "".join(sorted(set(ENGLISH + FRENCH + ITALIAN + GERMAN + SPANISH)))


def paste_from_clipboard() -> str:
    with contextlib.suppress(ImportError):
        return __import__("pandas").read_clipboard().columns[0]
    with contextlib.suppress(OSError):
        cmd = ["/usr/bin/xsel", "-b"]
        output = subprocess.run(cmd, check=True, stdout=subprocess.PIPE).stdout
        return output.decode("utf-8")
    return input("Paste here: ")


def construct_charset_from_text_in_clipboard():
    text = paste_from_clipboard()
    print(end=repr("".join(sorted(set(text) - set(ASCII) - set(PUNCTUATION)))))
    print(f"  # {len(text)} chars processed")
    exit(0)


# construct_charset_from_text_in_clipboard()


for i in range(32, 2048, 32):
    row = []
    for j in range(i, i + 32):
        char = chr(j)
        cell = f" {char if char.isprintable() else '?'} "
        if char in EFIGS:
            cell = f"\x1b[102;30m{cell}\x1b[0m"
        elif char in RUSSIAN + UKRAIN + BELARUSIAN:
            cell = f"\x1b[103;30m{cell}\x1b[0m"
        elif char in MATH + PORTUGUESE + TURKISH:
            cell = f"\x1b[104;30m{cell}\x1b[0m"
        row.append(cell)
    print(f"{i:03x}", "".join(row))
print("total:", len(set(EFIGS + RUSSIAN + UKRAIN + BELARUSIAN + MATH + PORTUGUESE + TURKISH)), "letters")
