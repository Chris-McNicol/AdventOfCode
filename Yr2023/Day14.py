from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
import tqdm
from functools import lru_cache, reduce
import itertools
import numpy as np
from enum import Enum
import math



def get_lines(file):
    with open(file, 'r') as in_file:
        result_lines =  in_file.readlines()
    result_lines = [line.strip() for line in result_lines]
    return result_lines

@dataclass
class Platform:
    pos_arr: np.ndarray
    original_arr: np.ndarray

    def __eq__(self, other):
        return self.pos_arr == other.pos_arr
    
    def reset(self):
        self.pos_arr = self.original_arr.copy()

    @classmethod
    def from_line_arr(cls, line_arr):        
        return Platform(line_arr.copy(), line_arr.copy())
    
    @staticmethod
    def fast_shift(row, reverse=False):
        return '#'.join(''.join(sorted(section, reverse=reverse)) for section in row.split('#'))
    
    def transpose(self):        
        self.pos_arr = [''.join(row) for row in itertools.zip_longest(*self.pos_arr)]
        return self
        
    def east(self):
        self.pos_arr[:] = [self.fast_shift(row) for row in self.pos_arr]
        return self
    
    def west(self):
        self.pos_arr[:] = [self.fast_shift(row, reverse=True) for row in self.pos_arr]
        return self

    def north(self):
        self.transpose().west().transpose()
        return self
    
    def south(self):
        self.transpose().east().transpose()
        return self

    def cycle(self, num_cycles=1):
        for _ in range(num_cycles):
            self.north().west().south().east()
        return self

    @property
    def load(self):
        load_counter = 0
        for y, line in enumerate(self.pos_arr):
            load_counter += sum([(len(self.pos_arr) - y) for ch in line if ch == 'O'])
        return load_counter


@dataclass
class CycleFinder:
    tortoise: Platform
    hare: Platform

    @classmethod
    def from_lines(cls, line_arr):
        return CycleFinder(Platform.from_line_arr(line_arr), Platform.from_line_arr(line_arr))

    def find_cycles(self):
        ### Using Brent's Cycle Detection
        ### https://en.wikipedia.org/wiki/Cycle_detection#Brent's_algorithm
        power, lam, mu = 1, 1, 0
        self.hare.cycle()                
        while self.tortoise != self.hare: 
            if power == lam:                
                self.tortoise.pos_arr = self.hare.pos_arr.copy()
                power *= 2
                lam = 0
            self.hare.cycle()            
            lam += 1

        self.tortoise.reset()
        self.hare.reset()        
        self.hare.cycle(num_cycles=lam)
        
        while self.tortoise != self.hare:
            self.tortoise.cycle()
            self.hare.cycle()
            mu += 1
        return lam, mu


if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day14.txt' 
    #filename = r'Yr2023\PuzzleData\Example.txt' 
    lines = get_lines(filename) 
    plat = Platform.from_line_arr(lines)

    cyc = CycleFinder.from_lines(lines)  
    plat.north()
    part_one = plat.load
    plat.reset()
    
    testing_limit = 1_000_000_000
    lam, mu = cyc.find_cycles()    
    cycle_skip = mu + (testing_limit - mu) % lam   
    part_two = plat.cycle(num_cycles=cycle_skip).load

    print(f"Part One: {part_one}    Part Two:  {part_two}")
