def main():
    import random2
    cards = ["jack", "queen", "king", "ace"]
    random2.shuffle(cards)
    for i in range(2):
        for card in cards:
            print(card)
import sys
if len(sys.argv) < 2:
    print("too few arguments")
for i in range(1, len(sys.argv)):
    print(sys.argv[i])

