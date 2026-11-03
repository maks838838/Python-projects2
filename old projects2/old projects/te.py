import string
from collections import Counter

def analyze_text(filename):
    translator = str.maketrans("", "", string.punctuation + "“”‘’")

    with open(filename, "r", encoding="utf-8", errors="ignore") as file:
        words = [
            word.translate(translator)
            for word in file.read().lower().split()
        ]

    # Remove empty strings
    words = [word for word in words if word]

    unique_words = set(words)
    counts = Counter(words)

    print(f"File: {filename}")
    print("-" * 40)
    print(f"Total words: {len(words)}")
    print(f"Unique words: {len(unique_words)}")
    print(f"Most common word: {counts.most_common(1)[0][0]}")
    print(f"Occurrences: {counts.most_common(1)[0][1]}")
    print(f"Longest word: {max(unique_words, key=len)}")
    print(f"Shortest word: {min(unique_words, key=len)}")
    print(f"Average word length: {sum(len(word) for word in words) / len(words):.2f}")
    print("\nTop 10 words:")
    for word, count in counts.most_common(1000):
        print(f"{word}: {count}")
    ##
    ##print("\n10 longest words:")
    ##for word in sorted(unique_words, key=len, reverse=True)[:10]:
    ##    print(word)
    ##
analyze_text("harry.txt")