import string

TEXT = """
Привіт, світе! Світ великий і прекрасний.
Привіт, друже! Світ чекає на тебе.
"""


def normalize(word):
    return word.strip(string.punctuation).lower()


def build_frequency(text):
    freq = {}
    for token in text.split():
        key = normalize(token)
        if not key:
            continue
        freq[key] = freq.get(key, 0) + 1
    return freq


freq = build_frequency(TEXT)

print("--- За алфавітом ---")
for k in sorted(freq):
    print(f"  {k:<15} : {freq[k]}")

print("\n--- За спаданням частоти ---")
for k, v in sorted(freq.items(), key=lambda kv: kv[1], reverse=True):
    print(f"  {k:<15} : {v}")

threshold = 2
frequent = {k: v for k, v in freq.items() if v >= threshold}
print(f"\n--- Слова з частотою >= {threshold} ---")
for k, v in frequent.items():
    print(f"  {k:<15} : {v}")

print(f"\nЧастота 'космос': {freq.get('космос', 0)}")
