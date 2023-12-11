from dataclasses import dataclass
from typing import List, Dict, Set
import tqdm
from functools import lru_cache, reduce
from itertools import combinations
import numpy as np
from enum import Enum
import math

def get_lines(file):
    with open(file, 'r') as in_file:
        result_lines =  in_file.readlines()
    result_lines = [line.strip() for line in result_lines]
    return result_lines


@dataclass
class Universe:
    galaxy_pos: Set
    max_row: int
    max_col: int

    @classmethod
    def from_line_arr(cls, line_arr):
        pos_set = set()
        max_row, max_col = len(line_arr), 0
        for line_idx, line in enumerate(line_arr):
            if max_col < len(line)-1:
                max_col = len(line)-1
            for ch_idx, ch in enumerate(line):
                if ch == '#':
                    pos_set.add((ch_idx, line_idx))
        return Universe(pos_set, max_row, max_col)
    
    def expand_vertical(self, row_idx, expansion_factor=2):
        self.galaxy_pos = set([(c,r) if r < row_idx else (c, r+expansion_factor-1) for c,r in self.galaxy_pos])
        self.max_row +=1
        return
    
    def expand_horizontal(self, col_idx, expansion_factor=2):
        self.galaxy_pos = set([(c,r) if c < col_idx else (c+expansion_factor-1, r) for c,r in self.galaxy_pos])
        self.max_col +=1
        return
    
    def is_row_empty(self, row_idx):
        return not any([row == row_idx for _col, row in self.galaxy_pos])
    
    def is_col_empty(self, col_idx):
        return not any([col == col_idx for col, _row in self.galaxy_pos])

    def expand(self, expansion_factor=2):
        empty_cols = [col_idx for col_idx in range(0, self.max_col) if self.is_col_empty(col_idx)]
        empty_rows = [row_idx for row_idx in range(0, self.max_row) if self.is_row_empty(row_idx)]
        for expand_col_counter, expand_col_idx in enumerate(empty_cols):
            self.expand_horizontal(expand_col_idx + expand_col_counter*(expansion_factor-1), expansion_factor=expansion_factor)
        for expand_row_counter, expand_row_idx in enumerate(empty_rows):
            self.expand_vertical(expand_row_idx + expand_row_counter*(expansion_factor-1), expansion_factor=expansion_factor)
        return
    
    @staticmethod
    def taxicab(pos_one, pos_two):
        return abs(pos_two[0]-pos_one[0]) + abs(pos_two[1]-pos_one[1])
    
    def sum_distances(self):
        return sum([self.taxicab(pos_one, pos_two) for pos_one, pos_two in combinations(self.galaxy_pos, 2)])


if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day11.txt' 
    #filename = r'Yr2023\PuzzleData\Example.txt' 
    lines = get_lines(filename) 
    
    universe = Universe.from_line_arr(lines)
    universe.expand(expansion_factor=2)
    part_one = universe.sum_distances()

    universe_two = Universe.from_line_arr(lines)
    universe_two.expand(expansion_factor=1_000_000)
    part_two = universe_two.sum_distances()

    print(f"Part One: {part_one}    Part Two:  {part_two}")
