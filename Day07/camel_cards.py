from argparse import ArgumentParser
from collections import defaultdict
from functools import cmp_to_key

CARD_VALS = '23456789TJQKA'
JOKER_CARD_VALS = 'J23456789TQKA'
HAND_VALS = ['H','1P','2P','3','FH','4','5']

class Hand:
    def __init__(self, cards) -> None:
        self.cards = cards
        self.type = None
        self.card_counts = defaultdict(int)
        for card in cards:
            self.card_counts[card] += 1
        
        match len(self.card_counts):
            case 5:
                self.type = 'H'
            case 4:
                self.type = '1P'
            case 3:
                if max(self.card_counts.values()) == 2:
                    self.type = '2P'
                else:
                    self.type = '3'
            case 2:
                if max(self.card_counts.values()) == 3:
                    self.type = 'FH'
                else:
                    self.type = '4'
            case 1:
                self.type = '5'

    def jokerfy(self):
        jokers = self.card_counts['J']
        joker_type_conversion = {
            1: {
                '4': '5',
                '3': '4',
                '2P': 'FH',
                '1P': '3',
                'H': '1P',
            },
            2: {
                'FH': '5',
                '2P': '4',
                '1P': '3',
            },
            3: {
                'FH': '5',
                '3': '4',
            },
            4: {
                '4': '5',
            },
            5: {
                '5': '5',
            },
        }
        if jokers:
            self.type = joker_type_conversion[jokers][self.type]

def handbid_compare(handbid1, handbid2):
    hand1, hand2 = Hand(handbid1[0]), Hand(handbid2[0])
    if hand1.cards == hand2.cards:
        return 0
    if hand1.type == hand2.type:
        for card1,card2 in zip(hand1.cards,hand2.cards):
            if card1 == card2:
                continue
            if CARD_VALS.find(card1) < CARD_VALS.find(card2):
                return -1
            return 1
    if HAND_VALS.index(hand1.type) < HAND_VALS.index(hand2.type):
        return -1
    return 1

def handbid_compare_joker(handbid1, handbid2):
    hand1, hand2 = Hand(handbid1[0]), Hand(handbid2[0])
    hand1.jokerfy()
    hand2.jokerfy()
    if hand1.cards == hand2.cards:
        return 0
    if hand1.type == hand2.type:
        for card1,card2 in zip(hand1.cards,hand2.cards):
            if card1 == card2:
                continue
            if JOKER_CARD_VALS.find(card1) < JOKER_CARD_VALS.find(card2):
                return -1
            return 1
    if HAND_VALS.index(hand1.type) < HAND_VALS.index(hand2.type):
        return -1
    return 1

def main(data):
    handbids = []
    for line in data:
        handbids.append(line.split())

    # Star 1
    handbids = sorted(handbids, key=cmp_to_key(handbid_compare))
    total_winnings = 0
    for rank,handbid in enumerate(handbids, start=1):
        total_winnings += rank * int(handbid[1])
    print(total_winnings)

    # Star 2
    handbids = sorted(handbids, key=cmp_to_key(handbid_compare_joker))
    total_winnings = 0
    for rank,handbid in enumerate(handbids, start=1):
        total_winnings += rank * int(handbid[1])
    print(total_winnings)

def read_input(input_file):
    data = []
    with open(input_file, 'r') as input:
        for line in input:
            data.append(line.strip())
    return data

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input_file', nargs='?', default='input.txt')
    args = parser.parse_args()
    data = read_input(args.input_file)
    main(data)
