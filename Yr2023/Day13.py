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


@dataclass
class Mirror:
    frame: np.ndarray
    
    @classmethod
    def from_line_arr(cls, line_arr):
        temp_arr = []
        for line in line_arr:
            temp_arr.append([1 if ch == '#' else 0 for ch in line])
        return Mirror(np.array(temp_arr))
    
    def is_reflection(self, idx, col:bool = False, smudge:bool = False):
        arr = self.frame.T if col else self.frame
        smudge_factor = 1 if smudge else 0
        min_idx = idx - min(idx, arr.shape[0] - idx)
        max_idx = idx + min(idx, arr.shape[0] - idx)
        return np.sum( arr[min_idx:idx] != arr[idx:max_idx][::-1]) == smudge_factor

    def get_candidates(self, col:bool = False, smudge:bool = False):
        frame = self.frame.T if col else self.frame
        candidates = np.where(np.all(np.diff(frame, axis=0) == 0, axis=1))[0] + 1
        if smudge:
            smudge_cands = np.where(np.sum(np.diff(frame, axis=0) != 0, axis=1) == 1)[0] + 1
            candidates = np.concatenate([candidates, smudge_cands])
        return candidates

    def get_symmetric_cols(self, smudge:bool=False):        
        candidate_cols = self.get_candidates(True, smudge)        
        return [col for col in candidate_cols if self.is_reflection(col, True, smudge)]
    
    def get_symmetric_rows(self, smudge:bool=False):        
        candidate_rows = self.get_candidates(False, smudge)
        return [row for row in candidate_rows if self.is_reflection(row, False, smudge)]
   
    def summarize(self, smudge:bool = False):
        return sum(self.get_symmetric_cols(smudge)) + (100 * sum(self.get_symmetric_rows(smudge)))


@dataclass
class HallOfMirrors:
    mirrors: List[Mirror]

    @classmethod
    def from_input(cls, lines):
        temp_lines, mirror_list = [], []
        for line_idx, line in enumerate(lines):
            if line.strip() == '':
                mirror_list.append(Mirror.from_line_arr(temp_lines))
                temp_lines = []
            else:
                temp_lines.append(line)
        mirror_list.append(Mirror.from_line_arr(temp_lines))    
        return HallOfMirrors(mirror_list)
    
    def summarize(self, smudge:bool = False):
        return sum([mirror.summarize(smudge) for mirror in tqdm.tqdm(self.mirrors)])


if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day13.txt' 
    #filename = r'Yr2023\PuzzleData\Example.txt' 
    lines = get_lines(filename) 
    hall = HallOfMirrors.from_input(lines)
    part_one = hall.summarize()
    part_two = hall.summarize(smudge=True)

    print(f"Part One: {part_one}    Part Two:  {part_two}")
