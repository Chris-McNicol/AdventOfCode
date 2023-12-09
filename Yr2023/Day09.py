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


@dataclass
class ValSeq:
    seq: List[int]

    @classmethod
    def from_line(cls, line):
        seq = [int(i) for i in line.split(' ')]        
        return ValSeq(seq)
    
    @staticmethod
    def get_diff_seq(seq):
        return [two - one for one,two in zip(seq[:-1], seq[1:])]
    
    
    def extrapolate(self):
        temp_seq, temp_seq_cache = self.seq, []        
        while any([i != 0 for i in temp_seq]):
            temp_seq_cache.append(temp_seq)
            temp_seq = self.get_diff_seq(temp_seq)

        back_extrap_val, forward_extrap_val = 0, 0
        for extrap_seq in reversed(temp_seq_cache):
            forward_extrap_val = extrap_seq[-1] + forward_extrap_val
            back_extrap_val =  extrap_seq[0] - back_extrap_val

        return back_extrap_val, forward_extrap_val


@dataclass
class Oasis:
    seqs: List[ValSeq]

    @classmethod
    def from_line_arr(cls, line_arr):
        val_seqs = [ValSeq.from_line(line) for line in line_arr]
        return Oasis(val_seqs)
   
    def sum_extrapolations(self):
        extrapolations = [seq.extrapolate() for seq in self.seqs]
        return tuple(map(sum, zip(*extrapolations)))
        

if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day09.txt' 
    #filename = r'Yr2023\PuzzleData\Example.txt' 
    lines = get_lines(filename)   
    oasis = Oasis.from_line_arr(lines)
    part_one, part_two = oasis.sum_extrapolations()
    print(f"Part One: {part_one}    Part Two:  {part_two}")
