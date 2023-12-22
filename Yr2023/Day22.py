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
class Brick:
    id: int
    start_x: int
    start_y: int
    start_z: int
    end_x: int
    end_y: int
    end_z: int
    supports: List[int]
    supported_by: List[int]

    def __lt__(self, otherBrick):
        return min(self.start_z, self.end_z) < min(otherBrick.start_z, otherBrick.end_z)
    
    def inject_peak_height(self, peak_map):
        height = max(self.start_z, self.end_z)
        for x,y in itertools.product(*[range(self.start_x, self.end_x+1), range(self.start_y, self.end_y+1)]):
            peak_map[x+y*1j] = height
        return
    
    def get_peak_height_underneath(self, peak_map):
        return max( [peak_map[x+y*1j] if x+y*1j in peak_map else 0 for x,y in itertools.product(*[range(self.start_x, self.end_x+1), range(self.start_y, self.end_y+1)])] )
    
    def __repr__(self):
        shift = self.id
        char_str = ''
        while shift >= 0:
            char_str += chr((shift % 26) + 65)
            shift -= 26
        return f"Brick {char_str}   ({self.start_x}, {self.start_y}, {self.start_z}) - ({self.end_x}, {self.end_y}, {self.end_z})" \
                f"{[b.id for b in self.supports]}  {[b.id for b in self.supported_by]}"

    @classmethod
    def from_line(cls, line, line_idx):
        start_str, end_str =line.split('~')
        start_x, start_y, start_z = start_str.split(',')
        end_x, end_y, end_z = end_str.split(',')
        my_start_x, my_end_x = min(int(start_x), int(end_x)), max(int(start_x), int(end_x))
        my_start_y, my_end_y = min(int(start_y), int(end_y)), max(int(start_y), int(end_y))
        my_start_z, my_end_z = min(int(start_z), int(end_z)), max(int(start_z), int(end_z))
        return Brick(line_idx, my_start_x, my_start_y, my_start_z, my_end_x, my_end_y, my_end_z, [], [])
             
    @staticmethod
    def overlap(start_one, end_one, start_two, end_two):
        return (start_one <= end_two and  start_two <=end_one)
   
    def overlaps(self, otherBrick):
        overlap_x =  self.overlap(self.start_x, self.end_x, otherBrick.start_x, otherBrick.end_x)
        overlap_y =  self.overlap(self.start_y, self.end_y, otherBrick.start_y, otherBrick.end_y)
        overlap_z =  self.overlap(self.start_z - 1 , self.end_z - 1, otherBrick.start_z, otherBrick.end_z)
        return (overlap_x and overlap_y and overlap_z)
        
    def fall(self, peak_map):
        dist_to_fall = self.start_z - self.get_peak_height_underneath(peak_map) - 1
        self.start_z -= dist_to_fall
        self.end_z -= dist_to_fall
        self.inject_peak_height(peak_map)
        return
    

@dataclass
class BrickPile:
    bricks: List[Brick]
    peak_map : Dict

    @classmethod
    def from_lines(cls, lines):
        return BrickPile(sorted([Brick.from_line(line, line_idx) for line_idx, line in enumerate(lines)]), {})
        
    def gravity(self):        
        for brick in tqdm.tqdm(self.bricks):
            brick.fall(self.peak_map)       
        return
    
    def printbricks(self):
        for brick in self.bricks:
            print(brick)

    def check_supports(self):
        self.support_count = {b.id: 0 for b in self.bricks}
        for brick, otherbrick in itertools.product(*[self.bricks, self.bricks]):
            if brick == otherbrick: continue
            if brick.overlaps(otherbrick):
                brick.supported_by.append(otherbrick)
                otherbrick.supports.append(brick)
                self.support_count[brick.id] += 1
    
    def count_reduntant_bricks(self):
        return len(set([id for brick in self.bricks for id in brick.supported_by if len(brick.supported_by) > 1]))
    
    def count_standalone_bricks(self):
        return len([brick.id for brick in self.bricks if len(brick.supports) == 0])
    
    def disintegrate(self):
        self.disintegrated = [brick for brick in self.bricks if all( [len(top.supported_by) > 1 for top in brick.supports] )]
        return self.disintegrated

    def count_collapses(self, brick):        
        queue, count = [brick] , 0
        removed_supports = {b.id:0 for b in self.bricks}        
        while queue:
            count += 1
            x = queue.pop()
            for b in x.supports:                                
                removed_supports[b.id] += 1                
                if removed_supports[b.id] == self.support_count[b.id]:
                    queue.append(b)        
        return count - 1 # as not counting the brick itself

    def count_chain_reaction(self):
        return sum([self.count_collapses(brick) for brick in tqdm.tqdm([b for b in self.bricks if b not in self.disintegrated])])


if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day22.txt'
    #filename = r'Yr2023\PuzzleData\Example.txt'
    
    lines = get_lines(filename)
    pile = BrickPile.from_lines(lines)   
    pile.gravity()
    pile.check_supports()

    part_one = len(pile.disintegrate())
    part_two = pile.count_chain_reaction()

    print(f"Part One: {part_one}    Part Two:  {part_two}")
