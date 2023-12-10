from dataclasses import dataclass
from typing import List, Dict
import tqdm
from functools import lru_cache, reduce
import numpy as np
from enum import Enum
import math

def get_lines(file):
    with open(file, 'r') as in_file:
        result_lines =  in_file.readlines()
    result_lines = [line.strip() for line in result_lines]
    return result_lines


class Grid:    
    def __init__(self, lines: List[str], pipe_map: Dict):
        self.lines = lines
        self.pipe_map = pipe_map
        for line_idx, line in enumerate(self.lines):
            for ch_idx, ch in enumerate(line):
                if ch == 'S':
                    self.start_pt = (ch_idx, line_idx)
                    for delta, allowed in zip([(0,1),(0,-1),(1,0),(-1,0)], [['J', '|', 'L'],['F','|','7'], ['J', '-','7'], ['L','-','F']]):
                        if self.lookup((ch_idx+delta[0], line_idx+delta[1])) in allowed:
                            self.pipe_map['S'].append(delta)
        
    def lookup(self, pos):
        ch_idx, line_idx = pos
        return self.lines[line_idx][ch_idx] if (0<=line_idx<len(self.lines)) and (0<=ch_idx<len(self.lines[line_idx])) else None

    def check_pipe_ends(self, ch_idx, line_idx):
        val = self.lines[line_idx][ch_idx]
        if val not in self.pipe_map:
            return [(None, None)]
                
        result = []
        for end_delta in self.pipe_map[val]:
            end_pos = (ch_idx + end_delta[0], line_idx + end_delta[1])
            end = self.lookup(end_pos)
            result.append( (end_pos, end))
        return result
            
    def build_graph(self):
        self.graph = {}
        for line_idx, line in enumerate(self.lines):
            for ch_idx, ch in enumerate(line):
                if ch not in self.pipe_map and ch != 'S':
                    continue
                
                for end_pos, end in self.check_pipe_ends(ch_idx, line_idx):
                    if end_pos is not None and end in self.pipe_map:
                        if (ch_idx, line_idx) not in self.graph:
                            self.graph[(ch_idx, line_idx)] = [end_pos]
                        else:
                            self.graph[(ch_idx, line_idx)].append(end_pos)       
        return
    
    def traverse_graph(self):
        point, distance = self.start_pt, 0
        points_to_explore = [(point, distance)]
        explored_points, explored_distances = [], {}
        while points_to_explore:
            point, distance = points_to_explore.pop(0)
            if point in explored_points:
                continue
            explored_points.append(point)
            explored_distances[point] = distance
            
            if point in self.graph:
                for end_pos in self.graph[point]:
                    if end_pos not in explored_points and end_pos in self.graph:
                        points_to_explore.append((end_pos, distance+1))
            
        return explored_distances
    

    def area_contained(self, explored_distances):
        tiles_contained = 0
        
        for line_idx, line in enumerate(lines):
            loop_cross_counter = 0
            
            for ch_idx, ch in enumerate(line):
                if (ch_idx, line_idx) in explored_distances:
                    if ch in '|JLS': loop_cross_counter += 1
                else:
                    tiles_contained += loop_cross_counter % 2
        return tiles_contained


    def print_visits(self, visit_dict):        
        print_lines = []
        for line_idx, line in enumerate(self.lines):
            line_str = ''
            for ch_idx, ch in enumerate(line):
                my_ch = 'X' if (ch_idx, line_idx) in visit_dict else '.'
                line_str += my_ch
            print_lines.append(line_str)
        
        for print_line in print_lines:
            print(print_line)
        return
                


if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day10.txt' 
    #filename = r'Yr2023\PuzzleData\Example.txt' 
    lines = get_lines(filename) 
    pipe_map = {'|':[(0,1),(0,-1)], '-':[(-1,0),(1,0)], 'L':[(0,-1),(1,0)], 'J':[(0,-1),(-1,0)], '7':[(0,1),(-1,0)], 'F':[(0,1),(1,0)], 'S':[]}  
    grid = Grid(lines, pipe_map)    
    grid.build_graph()    
    explored = grid.traverse_graph()
    part_one = max(explored.values())
    part_two = grid.area_contained(explored)

    #grid.print_visits(explored)

    print(f"Part One: {part_one}    Part Two:  {part_two}")
