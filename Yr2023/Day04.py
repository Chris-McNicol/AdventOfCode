from dataclasses import dataclass
from typing import List

def get_lines(file):
    with open(file, 'r') as in_file:
        result_lines =  in_file.readlines()
    result_lines = [line.strip() for line in result_lines]
    return result_lines

@dataclass
class Card:
    id: int
    winners: List[int]
    owned: List[int]

    @classmethod
    def from_line(cls, line):
        colon_split = line.strip().split(':')
        id_str = colon_split[0].split(' ')[-1]
        cards_str = colon_split[-1].split('|')
        winner_list = [int(i) for i in cards_str[0].split(' ') if i.isdigit()]
        owned_list = [int(i) for i in cards_str[1].split(' ') if i.isdigit()]
        return Card(int(id_str), winner_list, owned_list)
    
    def num_matches(self):
        return sum([1 if val in self.winners else 0 for val in self.owned])
    
    def points(self):
        return int(2**(self.num_matches() - 1))
        
def play_cards(orig_card_list):
    card_list = orig_card_list
    card_counter = {card.id: 1 for card in card_list}
    for card in card_list:
        num_match = card.num_matches()
        for i in range(card.id+1, card.id + 1 + num_match):
            card_counter[i] += card_counter[card.id]
    return sum([v for k,v in card_counter.items()])



if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day04.txt' 
    lines = get_lines(filename)
    cards = [Card.from_line(line) for line in lines]
    part_one = sum([card.points() for card in cards])
    part_two = play_cards(cards)
    print(f"Part One: {part_one}    Part Two:  {part_two}")