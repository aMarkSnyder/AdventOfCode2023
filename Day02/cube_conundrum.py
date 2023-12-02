class GameHand:
    def __init__(self, red=0, blue=0, green=0) -> None:
        self.red = red
        self.blue = blue
        self.green = green

class GameData:
    def __init__(self, gid, hands) -> None:
        self.gid = gid
        self.hands = hands

    def is_valid_replace(self, max_red, max_blue, max_green):
        for hand in self.hands:
            if hand.red > max_red or hand.blue > max_blue or hand.green > max_green:
                return False
        return True
    
    def power(self):
        min_red, min_blue, min_green = 0, 0, 0
        for hand in self.hands:
            if hand.red > min_red:
                min_red = hand.red
            if hand.blue > min_blue:
                min_blue = hand.blue
            if hand.green > min_green:
                min_green = hand.green
        return min_red * min_blue * min_green

def parse_game(game_string):
    idx_part, hands_part = game_string.split(':')
    game_idx = int(idx_part.split()[-1])

    game_hands = []
    hands = hands_part.split(';')
    for hand in hands:
        color_vals = {}
        for color in hand.split(','):
            color_vals[color.split()[1]] = int(color.split()[0])
        game_hands.append(GameHand(**color_vals))

    return GameData(game_idx, game_hands)

def main():
    games = []
    with open('input.txt','r') as input:
        for line in input:
            games.append(parse_game(line))

    # Star 1
    max_red, max_green, max_blue = 12, 13, 14
    valid_game_id_sum = 0
    for game in games:
        if game.is_valid_replace(max_red, max_blue, max_green):
            valid_game_id_sum += game.gid
    print(valid_game_id_sum)

    # Star 2
    game_power_sum = 0
    for game in games:
        game_power_sum += game.power()
    print(game_power_sum)

if __name__ == '__main__':
    main()