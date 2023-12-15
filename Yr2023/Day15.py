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
class Box:
    id: int
    lenses: List[Tuple[str, int]]

    def remove_lens(self, instruction):
        for lens in self.lenses:
            if lens[0] == instruction:
                self.lenses.remove(lens)
        return
    
    def update_lens(self, instruction, focal_length):
        already_in_box = False
        for lens_idx, lens in enumerate(self.lenses):
            if lens[0] == instruction:
                already_in_box = True
                self.lenses[lens_idx] = (instruction, int(focal_length))
        if not already_in_box:
            self.lenses.append((instruction, int(focal_length)))
        return
    
    @property
    def focussing_power(self):
        return (self.id+1) * sum([(idx+1)*lens[1] for idx, lens in enumerate(self.lenses)])
    
    def __str__(self):
        return f"Box {self.id}:" + ' '.join([f"[{instr, le}]" for instr, le in self.lenses])



@dataclass
class Manual:
    steps: List[str]
    box_list: List[Box]

    @classmethod
    def from_lines(cls, lines):
        return Manual([sub_str.strip() for sub_str in lines[0].split(',')], [Box(id, []) for id in range(256)])

    @staticmethod
    def hash_ch(start_hash, ch):
        return ( (start_hash + ord(ch))*17  % 256)
        
    def hash_str(self, in_str):
        hash = 0
        for ch in in_str:
            hash = self.hash_ch(hash, ch)
        return hash
    
    def hash_all(self):
        return sum([self.hash_str(step) for step in self.steps])
    
    def fill_boxes(self):        
        for step in self.steps:
            if step[-1] == '-':
                instruction = step[:-1]
                box_idx = self.hash_str(instruction)
                self.box_list[box_idx].remove_lens(instruction)

            else:
                instruction, focal_length = step.split('=')
                box_idx = self.hash_str(instruction)
                self.box_list[box_idx].update_lens(instruction, focal_length)
            
            #print(f'After "{step}":')
            #self.print_boxes()
            #print("")
        return
    
    def total_focussing_power(self):
        return sum([box.focussing_power for box in self.box_list])

    def print_boxes(self):
        for box in self.box_list:
            if len(box.lenses) > 0 :
                print(box)
            

if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day15.txt'
    #filename = r'Yr2023\PuzzleData\Example.txt' 
    lines = get_lines(filename) 
    man = Manual.from_lines(lines)    
    part_one = man.hash_all()
    man.fill_boxes()
    part_two = man.total_focussing_power()
    print(f"Part One: {part_one}    Part Two:  {part_two}")
