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
class Grid:
    grid: List[List[str]]
    move_map: Dict
    visited: List[Tuple[Tuple[int, int], Tuple[int,int]]]
    height: int
    width: int

    @classmethod
    def from_lines(cls, lines):
        move_map = {'.':{(0,-1):[(0,-1)], (0,1):[(0,1)], (-1,0):[(-1,0)], (1,0):[(1,0)]},
                    '/':{(0,-1):[(1,0)], (0,1):[(-1,0)], (-1,0):[(0,1)], (1,0):[(0,-1)]},
                    '\\':{(0,-1):[(-1,0)], (0,1):[(1,0)], (-1,0):[(0,-1)], (1,0):[(0,1)]},
                    '-':{(0,-1):[(1,0),(-1,0)], (0,1):[(1,0),(-1,0)], (-1,0):[((-1,0))], (1,0):[(1,0)]},
                    '|':{(0,-1):[(0,-1)], (0,1):[(0,1)], (-1,0):[(0,-1),(0,1)], (1,0):[(0,-1),(0,1)]}}
        return Grid(lines, move_map, visited=[], height=len(lines), width=len(lines[0]))
    
    def take_step(self, pos, heading):
        ch = self.grid[pos[1]][pos[0]]
        next_headings = self.move_map[ch][heading]
        next_pos = [((pos[0]+nh[0], pos[1]+nh[1]), nh) for nh in next_headings]
        return next_pos
    
    def is_in_bounds(self, pos):
        return (0 <= pos[0] < self.width) and (0 <= pos[1] < self.height)
    
    def ray_trace(self, start_pos=(-1,0), start_heading=(1,0)):       
        start_condition = (start_pos[0]+start_heading[0], start_pos[1]+start_heading[1])
        self.visited.append(start_condition)
        pos_list = self.take_step(start_condition, start_heading)        
        while pos_list:
            pos, hdg = pos_list.pop()            
            if (pos,hdg) in self.visited or not self.is_in_bounds(pos):                
                continue
            self.visited.append((pos,hdg))
            next_pos = self.take_step(pos, hdg)
            pos_list += next_pos
        return

    def maximum_energy(self):
        start_conditions, energies = [], []
        for x in range(0, self.width):
            start_conditions.append( ((x, -1),(0,1)) )
            start_conditions.append( ((x, self.height), (0,-1)) )
        for y in range(0, self.height):
            start_conditions.append( ((-1, y),(1,0)) )
            start_conditions.append( ((self.width, y), (-1,0)) )
        
        for start_pos, start_hdg in tqdm.tqdm(start_conditions):
            self.ray_trace(start_pos, start_hdg)
            energies.append(len(self.energized()))
            self.visited = []
        return max(energies)
    
    def energized(self):
        return set([pos for (pos,hdg) in self.visited])
    
    def printme(self):
        energized = self.energized()        
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        #print(self.visited)
        for line_idx, line in enumerate(self.grid):
            line_str = ''
            for ch_idx, ch in enumerate(line):
                #line_str += '#'  if (ch_idx, line_idx) in visit_set and ch =='.' else ch
                line_str += '#'  if (ch_idx, line_idx) in energized else '.'
            print(line_str)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")


@dataclass
class ComplexGrid:
    grid: Dict
    visited: List[Tuple[complex,complex]]
    height: int
    width: int
    
    @classmethod
    def from_lines(cls, lines):
        grid = {}
        for line_idx, line in enumerate(lines):
            for ch_idx, ch in enumerate(line):
                grid[ch_idx + 1j * line_idx] = ch
        return ComplexGrid(grid, [], len(lines), len(lines[0]))
    
    def take_step(self, state):
        pos, hdg = state
        ch = self.grid[pos]
        if ch == '/':
            next_hdg = [(hdg*1j).conjugate()]
        elif ch == '\\':
            next_hdg = [(hdg*-1j).conjugate()]
        elif ch == '|' and hdg.imag == 0:
            next_hdg = [1j, -1j]
        elif ch == '-' and hdg.real == 0:
            next_hdg = [1, -1]
        else:
            next_hdg = [hdg]
        return [(pos+n_hdg, n_hdg) for n_hdg in next_hdg]
    
    def ray_trace(self, start_state=(0, 1)):
        
        state_list = [start_state]
        while state_list:
            state = state_list.pop()
            if state in self.visited or state[0] not in self.grid:
                continue
            self.visited.append(state)
            next_states = self.take_step(state)
            state_list += next_states
                
        return
    
    def energized(self):
        return set([pos for (pos,hdg) in self.visited])
    
    def maximum_energy(self):
        start_states, energies = [], []
        for x in range(0, self.width):
            start_states.append( (x, 1j) )
            start_states.append( (x + (self.height-1)*1j, -1j) )
        for y in range(0, self.height):
            start_states.append( (1j*y, 1 ))
            start_states.append( (self.width-1 + 1j*y, -1 ))
        
        for start_state in tqdm.tqdm(start_states):
            self.visited = []
            self.ray_trace(start_state)
            energies.append(len(self.energized()))           
        return max(energies)
    
    def printme(self):
        energized = self.energized()        
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
        for line_idx in range(self.height):
            line_str = ''
            for ch_idx in range(self.width):
                line_str += '#'  if (ch_idx + line_idx*1j) in energized else '.'
            print(line_str)
        print("xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    

if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day16.txt'
    #filename = r'Yr2023\PuzzleData\Example.txt'
    lines = get_lines(filename) 
    #grid = Grid.from_lines(lines)
    grid = ComplexGrid.from_lines(lines)
    
    grid.ray_trace()
    #grid.printme()
    part_one = len(grid.energized())
    part_two = grid.maximum_energy()
    print(f"Part One: {part_one}    Part Two:  {part_two}")
