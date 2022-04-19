data = """
1 2 5
2 2 2
23 71 100
-9 9 -9
4 28 17
47 2 6
33 13 47
4 97 1812
16 18 21
74 13 28
10 39 4
666.666 e 47443838.15566313
3 17 20
""".strip().split("\n") # 2022-04-19

digits = {digit:0 for digit in "0123456789"}
probs = {digit:0 for digit in "0123456789"}
ocurs = {digit:0 for digit in "0123456789"}

for sample in data:
    cur_prob = 0
    cur_stat = {digit:0 for digit in "0123456789"}
    for digit in (ch for ch in sample if ch in digits):
        cur_stat[digit] += 1
        cur_prob += 1
    #accured_digits = sum((stat > 0) for stat in cur_stat.values())
    for digit, stat in cur_stat.items():
        digits[digit] += stat
        probs[digit] += stat / cur_prob
        ocurs[digit] += (stat > 0)

digits = list(sorted((stat, digit) for digit, stat in digits.items()))
probs = list(sorted((stat, digit) for digit, stat in probs.items()))
ocurs = list(sorted((stat, digit) for digit, stat in ocurs.items()))
for stat, digit in reversed(digits):
    print(stat, digit)
for stat, digit in reversed(probs):
    print(stat, digit)
for stat, digit in reversed(ocurs):
    print(stat, digit)
