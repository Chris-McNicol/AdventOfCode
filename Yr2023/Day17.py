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
class LavaCity:
    heatmap: Dict
    optipaths: Dict
    height: int
    width: int

    @classmethod
    def from_lines(cls, lines):
        heatmap = {}
        for line_idx, line in enumerate(lines):
            for ch_idx, ch in enumerate(line):
                heatmap[ch_idx + (line_idx*1j)] = int(ch)
        return LavaCity(heatmap, {}, len(lines), len(lines[0]))
    

    @staticmethod
    def heapify(a_cost, a_pos, a_dir):
        return (a_cost, (int(a_pos.real),int(a_pos.imag)), (int(a_dir.real),int(a_dir.imag)) )
    
    @staticmethod
    def unheapify(heap_state):
        a_cost, a_pos_tuple, a_dir_tuple = heap_state
        return (a_cost, complex(*a_pos_tuple), complex(*a_dir_tuple))
  
    def path_find(self, start_pos=0, start_dirs=[1,1j], end_pos=None, min_steps =1, max_steps=3):
        end_pos = (self.width-1) + (self.height-1)*1j if end_pos is None else end_pos
        visited = set([])        
        search_heap = []
        for start_dir in start_dirs:
            heappush(search_heap, self.heapify(0, start_pos, start_dir))

        while search_heap:
            cost, pos, d = self.unheapify(heappop(search_heap))
            if pos == end_pos: return cost
            if (pos, d) in visited: continue            
            visited.add( (pos, d))

            for new_d in [-1j*d, 1j*d]:
                for num_steps in range(min_steps, max_steps+1):
                    new_pos = pos + num_steps * new_d
                    if new_pos in self.heatmap:
                        new_cost = cost + sum([self.heatmap[pos + new_d*step] for step in range(1, num_steps+1)])
                        heappush(search_heap, self.heapify(new_cost, new_pos, new_d))
                

if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day17.txt'
    #filename = r'Yr2023\PuzzleData\Example.txt'
    lines = get_lines(filename) 
    lava = LavaCity.from_lines(lines)
    part_one = lava.path_find(min_steps = 1, max_steps = 3)
    part_two = lava.path_find(min_steps = 4, max_steps = 10)
    print(f"Part One: {part_one}    Part Two:  {part_two}")
