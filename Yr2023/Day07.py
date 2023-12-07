from dataclasses import dataclass
from typing import List, Dict
import tqdm
from functools import lru_cache, reduce
import numpy as np
from enum import Enum

def get_lines(file):
    with open(file, 'r') as in_file:
        result_lines =  in_file.readlines()
    result_lines = [line.strip() for line in result_lines]
    return result_lines


class Strength(Enum):
    HIGH_CARD = 0
    ONE_PAIR = 1
    TWO_PAIR = 2
    THREE_OF_A_KIND = 3
    FULL_HOUSE = 4
    FOUR_OF_A_KIND = 5
    FIVE_OF_A_KIND = 6

    def __lt__(self, other):
        return self.value < other.value

    def apply_single_joker(count_pattern):
        max_idx, max_val = 0, 0
        if sum(count_pattern) == 0:
            return [1,0,0,0,0]
        for val_idx, val in enumerate(count_pattern):
            if val != 0:
                max_idx, max_val = val_idx, val
        count_pattern[max_idx] -= 1 if max_val > 0 else 0        
        if max_idx < len(count_pattern) -1:
            count_pattern[max_idx + 1] +=1         
        return count_pattern

    @staticmethod
    def apply_joker(count_pattern, num_jokers):
        for _i in range(num_jokers):
            count_pattern = Strength.apply_single_joker(count_pattern)        
        return count_pattern

    @classmethod
    def from_hand_str(cls, hand_str, card_val_map, count_strength_map, part_one=False):        
        count_list = [hand_str.count(k) for k in card_val_map.keys()]
        num_jokers =  0 if part_one else count_list[-1]
        count_list = count_list if part_one else count_list[:-1]
        count_pattern = [count_list.count(i) for i in range(1,6)]
        count_pattern = Strength.apply_joker(count_pattern, num_jokers=num_jokers)        
        return Strength(count_strength_map[tuple(count_pattern)])



@dataclass
class Hand:
    hand_str: str
    strength: Strength
    bid: int
    card_val_map: Dict

    def comp_hand_str(self, other_hand_str):
        for ch_i,ch_j in zip(self.hand_str, other_hand_str):
            i,j = self.card_val_map[ch_i], self.card_val_map[ch_j]
            if i == j:
                continue
            return i < j

    def __lt__(self, other):
        if self.strength == other.strength:
            return self.comp_hand_str(other.hand_str)
        else: 
            return self.strength < other.strength

    @classmethod
    def from_line(cls, line, card_val_map, count_strength_map, part_one=True):
        hand_str, bid = line.split(' ')[0].strip(), line.split(' ')[-1].strip()
        strength = Strength.from_hand_str(hand_str, card_val_map, count_strength_map, part_one)
        return Hand(hand_str, strength, int(bid), card_val_map)


@dataclass
class CardGame:
    hands: List[Hand]

    @classmethod
    def from_line_arr(cls, lines, part_one=True):
        card_val_map_no_joker = {'A': 14, 'K': 13, 'Q': 12, 'J': 11, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5':5, '4': 4, '3': 3, '2': 2}
        card_val_map_joker = {'A': 14, 'K': 13, 'Q': 12, 'T': 10, '9': 9, '8': 8, '7': 7, '6': 6, '5':5, '4': 4, '3': 3, '2': 2, 'J': 0}
        card_val_map = card_val_map_no_joker if part_one else card_val_map_joker
        count_strength_map = {(5,0,0,0,0):0, (3,1,0,0,0):1, (1,2,0,0,0):2, (2,0,1,0,0):3, (0,1,1,0,0):4, (1,0,0,1,0):5, (0,0,0,0,1):6}
        hands = [Hand.from_line(line, card_val_map, count_strength_map, part_one) for line in lines]
        return CardGame(hands)
    
    def sort_hands(self):
        self.hands.sort()
        return
    
    def printme(self):
        for hand_idx, hand in enumerate(self.hands):
            print(f"Hand {hand.hand_str}  {hand.strength}   Bid: {hand.bid}  Rank {hand_idx+1}")
        print("-----------------------")

    def winnings(self):
        self.sort_hands()
        return sum( [(idx+1)*hand.bid for idx, hand in enumerate(self.hands)])


if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day07.txt' 
    #filename = r'Yr2023\PuzzleData\Example.txt' 
    lines = get_lines(filename)
    part_one_game = CardGame.from_line_arr(lines)
    part_two_game = CardGame.from_line_arr(lines, part_one=False)    
    
    part_one = part_one_game.winnings()
    part_two = part_two_game.winnings()

    do_print = True
    if do_print:
        part_one_game.printme()        
        part_two_game.printme()

    print(f"Part One: {part_one}    Part Two:  {part_two}")
