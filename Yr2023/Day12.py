from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
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

@lru_cache(maxsize=None)
def count_matching_configs(poss_list, config_list, current_contiguous_springs):
    if len(poss_list) == 0:
        both_zeros = (len(config_list) == 0) and (current_contiguous_springs == 0)        
        remainders_match = current_contiguous_springs == config_list[0] if len(config_list) == 1 else False        
        return both_zeros or remainders_match
    
    matches = 0
    possibilities = ['#', '.'] if poss_list[0] == '?' else poss_list[0]
    for poss in possibilities:
        if poss == '#':  #Still in contiguous group of springs
            matches += count_matching_configs(poss_list[1:], config_list, current_contiguous_springs + 1)
        elif current_contiguous_springs and config_list and config_list[0] == current_contiguous_springs: # Finished building contiguous group of springs
            matches += count_matching_configs(poss_list[1:], config_list[1:], 0)
        elif current_contiguous_springs == 0:   # Do nothing except move on to remaining possiblities
            matches += count_matching_configs(poss_list[1:], config_list, 0)
    return matches


@dataclass
class SpringConfig:
    def __init__(self, poss_list, config_list):
        self.poss_list = poss_list
        self.config_list = config_list

    @classmethod
    def from_line(cls, line):
        poss_str, config_list_str = line.split(' ')
        config_list = tuple([int(ch) for ch in config_list_str.split(',')])
        return SpringConfig(poss_str, config_list)
    
    def matching_configs(self, num_folds=1):
        return count_matching_configs("?".join([self.poss_list] * num_folds), self.config_list * num_folds, 0)


@dataclass
class SpringField:
    spring_cfgs: List[SpringConfig]

    @classmethod
    def from_line_arr(cls, line_arr):
        return SpringField([SpringConfig.from_line(line) for line in line_arr])
    
    def total_num_configs(self, num_folds=1):
        return sum([spring.matching_configs(num_folds=num_folds) for spring in tqdm.tqdm(self.spring_cfgs)])



if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day12.txt' 
    #filename = r'Yr2023\PuzzleData\Example.txt' 
    lines = get_lines(filename) 
    springfield = SpringField.from_line_arr(lines)

    part_one = springfield.total_num_configs(num_folds=1)    
    part_two = springfield.total_num_configs(num_folds=5)   
    print(f"Part One: {part_one}    Part Two:  {part_two}")
