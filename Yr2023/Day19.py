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
class Part:
    x:int
    m:int
    a:int
    s:int
    
    @classmethod
    def from_part_str(cls, part_str):
        attr_list = part_str[1:-1].split(',')
        return Part(int(attr_list[0][2:]), int(attr_list[1][2:]), int(attr_list[2][2:]), int(attr_list[3][2:]))
    
    def __str__(self):
        return f"{self.x} {self.m} {self.a} {self.s}"
    
    def check(self, condition):
        if isinstance(condition, str): return condition
        ch, comp, val, result = condition
        if comp == '<':
            return result if getattr(self,ch) < val else None
        else:
            return result if getattr(self,ch) > val else None
        
    @property
    def rating(self):
        return self.x+self.m+self.a+self.s


@dataclass
class Workflow:
    id_str: str
    rule_str: str
    conditions: List[List[str]]

    @staticmethod
    def parse_condition_string(cond):
        split_colon = cond.split(':')
        if len(split_colon) == 1:
            return cond[:-1]
        ch, comp, val, result = split_colon[0][0], split_colon[0][1], split_colon[0][2:], split_colon[-1]
        return (ch, comp, int(val), result)

    @classmethod
    def from_workflow_str(cls, line):
        bracket_split = line.split('{')
        conditions = [cls.parse_condition_string(cond) for cond in bracket_split[-1].split(',')]
        return Workflow(bracket_split[0], line, conditions)

    def outcome(self, part: Part):
        for cond in self.conditions:
            result = part.check(cond)
            if result is not None:
                return result
        return result
           
    def check_intervals(self, condition, intervals):
        if isinstance(condition, str):
            if condition == 'R': return condition, [], None
            if condition == 'A': return condition, intervals, None
            return condition, intervals, None
        ch, comp, val, result = condition
        ch_idx = 'xmas'.index(ch)
        lo, hi = intervals[ch_idx]

        if lo < val and hi > val:
            pass_intervals, fail_intervals = intervals.copy(), intervals.copy()            
            pass_intervals[ch_idx] = (lo, val-1) if comp == '<' else (val+1, hi)            
            fail_intervals[ch_idx] = (val, hi) if comp == '<' else (lo, val)            
            return result, pass_intervals, fail_intervals
        
        if (lo < val and hi < val ):
            raise ValueError("I'm surprised I never go here - is it just lucky puzzle input?")
            return result, intervals, None if comp == '<' else None, None, intervals
        
        if (lo > val and hi > val ):
            raise ValueError("I'm surprised I never go here - is it just lucky puzzle input?")
            return result, intervals, None if comp == '>' else None, None, intervals        
        raise ValueError("ISHOULDN@TGET HERE")
    
    def check_interval_all_conditions(self, interval):
        return_list = []
        for cond in self.conditions:
            pass_result, pass_intervals, fail_intervals = self.check_intervals(cond, interval)
            return_list.append( (pass_result, pass_intervals) )
            interval = fail_intervals
        return return_list


@dataclass
class PartSorter:
    workflows : Dict
    parts : List[Part]

    @classmethod
    def from_lines(cls, lines):
        start_parts = False
        w_s, p_s = {}, []
        for line in lines:
            if line == '': start_parts = True; continue
            if start_parts: p_s.append(Part.from_part_str(line))
            else:
                id_str = line.split('{')[0]
                w_s[id_str] = Workflow.from_workflow_str(line)
        return PartSorter(w_s, p_s)
    
    def accept_part(self, part):
        workflow = self.workflows['in']
        result = workflow.outcome(part)        
        while result not in ['R', 'A']:            
            workflow = self.workflows[result]
            result = workflow.outcome(part)
        return result == 'A'

    def count_accepted_parts(self):
        return sum([part.rating for part in self.parts if self.accept_part(part)])
    
    def find_accepted_ranges(self):
        search_states, success_intervals = [('in', [(1, 4000), (1, 4000), (1, 4000), (1, 4000)])], []
        while search_states:            
            name, interval = search_states.pop()            
            if name == 'R': continue
            if name == 'A': success_intervals.append(interval); continue            
            search_states.extend(self.workflows[name].check_interval_all_conditions(interval))
        return sum ( [reduce(lambda x,y : x*y, [(lim[1]-lim[0] + 1) for lim in succ_interval]) for succ_interval in success_intervals] )


if __name__ == "__main__":
    #filename = r'Yr2023\PuzzleData\Day19.txt'
    filename = r'Yr2023\PuzzleData\Example.txt'
    lines = get_lines(filename)    

    sorter = PartSorter.from_lines(lines)

    part_one = sorter.count_accepted_parts()
    part_two = sorter.find_accepted_ranges()
    
    print(f"Part One: {part_one}    Part Two:  {part_two}")
