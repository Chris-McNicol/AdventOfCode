from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
import tqdm
from functools import lru_cache, reduce
import itertools
import numpy as np
from enum import Enum
import math
from heapq import heappush, heappop, heapify
from collections import deque


def get_lines(file):
    with open(file, 'r') as in_file:
        result_lines =  in_file.readlines()
    result_lines = [line.strip() for line in result_lines]
    return result_lines


@dataclass
class Garden:
    start: complex
    rocks: Set
    height: int
    width: int

    @classmethod
    def from_lines(cls, lines):
        rocks = set()
        for line_idx, line in enumerate(lines):
            for ch_idx, ch in enumerate(line):
                pos = ch_idx + line_idx*1j
                if ch == 'S': start = pos
                if ch == '#': rocks.add(pos)
        return Garden(start, rocks, len(lines), len(lines[0]))


    def is_rock(self, pos):
        ref_pos_real, ref_pos_imag = pos.real % self.width, pos.imag % self.height
        return ref_pos_real + ref_pos_imag*1j in self.rocks
       
    def valid_neighbours(self, pos):
        #return set([n_pos for n_pos in [pos+1, pos-1, pos+1j, pos-1j]])
        return set([n_pos for n_pos in [pos+1, pos-1, pos+1j, pos-1j] if 0<=n_pos.real<self.width and 0<=n_pos.imag<self.height])
    
    def nearby_plots(self, pos):
        return set([n_pos for n_pos in self.valid_neighbours(pos) if not self.is_rock(n_pos)])
    
    def next_step(self, current_step):
        return set([n_pos for pos in current_step for n_pos in self.nearby_plots(pos)])
    
    
    def dist_from_start(self, pos):
        return abs(pos.real-self.start.real) + abs(pos.imag-self.start.imag)
    
    def reachable_in_n_steps(self, n_steps, part_two_N = 26_501_365, start=None, print_garden=False):
        self.start = start if start is not None else self.start
        current_step = set([self.start])
        
        output_vals = []
        part_one, part_two = None, None
        odd_total, even_total = 0,0
        odd_corners, even_corners = 0,0
        for _i in tqdm.tqdm(range(1, n_steps+1)): 
            if print_garden:
                print(_i, len(current_step),  len(self.rocks))
                self.print_step(current_step)

            if _i == 65:
                part_one = len(current_step)

            if _i % 2 == 0:
                even_total = len(current_step)
                even_corners = len([pos for pos in current_step if self.dist_from_start(pos) > 65])
            else:
                odd_total = len(current_step)
                odd_corners = len([pos for pos in current_step if self.dist_from_start(pos) > 65])
                        
            if _i % self.width == self.width//2:
                output_vals.append( (_i, len(current_step) ))
            current_step = self.next_step(current_step)

        N = (part_two_N - self.width//2)/self.width        
        part_two = (odd_total)*(N**2) + (N+1)*(N+1)*even_total - ((N+1) * odd_corners) + (N*even_corners)  + (N+0.5)*324
        
        return part_one, int(part_two)
    
    def print_step(self, step):
        print("-------------------------------------------")
        for y in range(0, self.height):
            print(''.join('#' if x+y*1j in step else '.' for x in range(0, self.width)))
        print("-------------------------------------------")

    '''
    def quadratic_fit(self, big_N = 26_501_365):
        _, val_list = self.reachable_in_n_steps(n_steps = int(2.5*self.width) + 1)
        
        b0 = val_list[0][1]
        b1 = val_list[1][1] - b0
        b2 = val_list[2][1] - val_list[1][1]

        n = big_N//self.width
        estimate = b0 + b1*n + (n*(n-1)//2)*(b2-b1)
        return estimate
    '''
       

if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day21.txt'
    #filename = r'Yr2023\PuzzleData\Example.txt'
    
    n_steps = 64 if filename == r'Yr2023\PuzzleData\Day21.txt' else 6

    lines = get_lines(filename)    
    garden = Garden.from_lines(lines)
    

    part_one, part_two = garden.reachable_in_n_steps(n_steps = 135)

    print(f"Part One: {part_one}    Part Two:  {part_two}")
