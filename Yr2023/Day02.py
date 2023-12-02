from dataclasses import dataclass
from typing import List

def get_lines(file):
    with open(file, 'r') as in_file:
        result_lines =  in_file.readlines()
    return result_lines

@dataclass
class Handfull:
    red: int = 0
    green: int = 0
    blue: int = 0

    @classmethod
    def from_str(cls, in_str):
        h = Handfull()
        for part in in_str.split(','):
            num, color = part.strip().split(' ')
            setattr(h, color, int(num))
        return h
    
    def __add__(self, other_handfull):
        return Handfull(max([self.red, other_handfull.red]), max([self.green, other_handfull.green]), max([self.blue, other_handfull.blue]))
    
    def __radd__(self, other_handfull):
        return self if other_handfull == 0 else self.add_(other_handfull)
    
    @property
    def power(self):
        return self.red*self.green*self.blue


@dataclass
class Game:
    id: int
    handfulls: List[Handfull]

    @classmethod
    def from_line(cls, line):
        colon_split = line.split(':')
        id = int(colon_split[0].split(' ')[-1])
        handfull_str_list = colon_split[-1].split(';')
        return Game(id, [Handfull.from_str(h) for h in handfull_str_list])

    def is_possible(self, max_red=0, max_green=0, max_blue=0):
        for handfull in self.handfulls:
            if max_red < handfull.red or max_green < handfull.green or max_blue < handfull.blue:
                return False
        return True
    
    @property
    def min_power(self):        
        return sum(self.handfulls).power
    

if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day02.txt'    
    max_red, max_green, max_blue = 12, 13, 14    
    game_list = [Game.from_line(line) for line in get_lines(filename)]
    part_one = sum([g.id for g in game_list if g.is_possible(max_red, max_green, max_blue)])
    part_two = sum(g.min_power for g in game_list)    
    print(f"Part One: {part_one}    Part Two:  {part_two}")