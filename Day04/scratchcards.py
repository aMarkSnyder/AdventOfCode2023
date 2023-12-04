from collections import defaultdict

def find_matches(input_line):
    input_line = input_line.strip()
    numbers = input_line.split(':')[1]
    winning_numbers, present_numbers = numbers.split('|')
    winning_numbers = [int(number) for number in winning_numbers.split()]
    present_numbers = [int(number) for number in present_numbers.split()]
    matches = 0
    for number in present_numbers:
        if number in winning_numbers:
            matches += 1
    return matches

def main():
    points = 0
    num_copies = defaultdict(int)
    final_card_no = 1
    with open('input.txt','r') as input:
        for card_no, line in enumerate(input, start=1):
            matches = find_matches(line)
            # Star 1
            if matches:
                points += 2**(matches-1)

            # Star 2
            num_copies[card_no] += 1
            for copy_card_offset in range(1, matches+1):
                num_copies[card_no+copy_card_offset] += num_copies[card_no]
            final_card_no = card_no

    print(points)
    print(sum(num_copies[card_no] for card_no in range(1, final_card_no+1)))

if __name__ == '__main__':
    main()
