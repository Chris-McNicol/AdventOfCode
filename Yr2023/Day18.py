from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
import tqdm
from functools import lru_cache, reduce
import itertools
import numpy as np
from enum import Enum
import math
from heapq import heappush, heappop


def get_lines(file):
    with open(file, 'r') as in_file:
        result_lines =  in_file.readlines()
    result_lines = [line.strip() for line in result_lines]
    return result_lines

@dataclass
class BigHole:      
    def __init__(self, lines, part_one=True):
        part_one_d_map = {'U':-1j, 'D':1j, 'R':1, 'L': -1}
        part_two_d_map = {'0':1, '1':1j, '2':-1, '3':-1j}        
        self.perimeter, current_pos, current_d = 0, 0, 0              
        self.vertices = [current_pos]
        for line in lines:
            d_str, num_steps_str, rgb_str = line.split(' ')            
            (num_steps, current_d) = (int(num_steps_str), part_one_d_map[d_str]) if part_one else self.hex_to_steps(rgb_str, part_two_d_map)            
            current_pos = current_pos + (current_d)*num_steps
            self.perimeter += num_steps
            self.vertices.append(current_pos)
        return
    
    @staticmethod
    def hex_to_steps(rgb_str, part_two_d_map):
        return int(rgb_str[2:-2], 16), part_two_d_map[rgb_str[-2]]
    
    def shoelace_area(self):
        shoelace = sum([(pos.real*self.vertices[p_i+1].imag - pos.imag*self.vertices[p_i+1].real) for p_i, pos in enumerate(self.vertices[:-1])])        
        return int(abs(shoelace) + self.perimeter) // 2 + 1
        


if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day18.txt'
    #filename = r'Yr2023\PuzzleData\Example.txt'
    lines = get_lines(filename) 
    
    part_one_hole = BigHole(lines, part_one=True)
    part_two_hole = BigHole(lines, part_one=False)
    
    part_one = part_one_hole.shoelace_area()
    part_two = part_two_hole.shoelace_area()
    
    print(f"Part One: {part_one}    Part Two:  {part_two}")
