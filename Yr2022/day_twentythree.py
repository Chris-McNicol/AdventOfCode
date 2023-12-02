from time import perf_counter_ns
from tqdm import tqdm

from itertools import groupby
from operator import countOf
from typing import Tuple, Set, List, Dict

from dataclasses import dataclass

UPBITS = 0b11100000
DOWNBITS = 0b00000111
LEFTBITS = 0b10010100
RIGHTBITS = 0b00101001

@dataclass
class Arena:
    occupied: Set[Tuple[int,int]]
    adjs = [[UPBITS,(0,-1)], [DOWNBITS,(0,1)], [LEFTBITS,(-1,0)], [RIGHTBITS,(1,0)]]
    def get_adjacents(self, pos):
        delta_x, delta_y = [1, 0, -1], [1, 0, -1]
        idx, bits = 0, 0
        for dy in delta_y:
            for dx in delta_x:
                if dx ==  0 and dy == 0:
                    continue
                if (pos[0] + dx, pos[1] + dy) in self.occupied:
                    bits = bits | (1 << idx)
                idx += 1

        return bits
    
    def proposals(self, pos, turn_idx):
        adj = self.get_adjacents(pos)
        if adj == 0:            
            return None
        for _i in range(0,4):
            side_bits = self.adjs[ (turn_idx+_i) % len(self.adjs)][0]
            side_dir = self.adjs[ (turn_idx+_i) % len(self.adjs)][1]
            side_clear = adj & side_bits == 0
            if side_clear:
                return (pos[0]+side_dir[0], pos[1]+side_dir[1])
        return None

    def calc_move(self, turn_idx):
        move_dict = {}
        next_occupied = set()
        for current in self.occupied:
            move_dict[current] = self.proposals(current, turn_idx)
      
        for current, next in move_dict.items():
            
            if next is None or countOf(move_dict.values(), next) > 1:
                next_occupied.add(current)
            else:
                next_occupied.add(next)
        has_updated = self.occupied != next_occupied
        self.occupied = next_occupied
        return has_updated
    
    def get_empty(self):
        xs, ys = [pos[0] for pos in self.occupied], [pos[1] for pos in self.occupied]
        min_x, max_x = min(xs), max(xs)+1
        min_y, max_y = min(ys), max(ys)+1
        total_area = (max_y-min_y)* (max_x - min_x)    
        
        return total_area - len(self.occupied)
        

    def print_arena(self):
        xs, ys = [pos[0] for pos in self.occupied], [pos[1] for pos in self.occupied]
        min_x, max_x = min(xs + [0]), max(xs + [4])
        min_y, max_y = min(ys + [0]), max(ys + [5])
        out_str = ""
        for y in range(min_y, max_y+1):
            for x in range(min_x, max_x+1):
                out_str += "#" if (x,y) in self.occupied else "."
            out_str += "\n"
        print(out_str)


        
def pathfind(filename: str):    
    with open(filename, 'r') as file:
        cmd_lines = file.readlines()
    
    occupied = set()
    for line_idx, line in enumerate(cmd_lines):
        for char_idx, char in enumerate(line):
            if char == '#':
                occupied.add( (char_idx, line_idx ))

    arena = Arena(occupied=occupied)
    #arena.print_arena()
    for i in range(0, 10):        
        arena.calc_move(i)        
       
    
    part_one = arena.get_empty()
    part_two, has_updated = 0, True
    arena_two = Arena(occupied=occupied)
    while has_updated:
        
        has_updated = arena_two.calc_move(part_two)
        part_two += 1     

    return part_one, part_two
  

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_twentythree.txt"
    #file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\example.txt"
    #file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\other_example.txt"
    
    part_one, part_two = pathfind(file_loc)
    
    print(f"(Part One): {part_one}     (Part Two): {part_two}")   
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")  
