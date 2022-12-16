from time import perf_counter_ns
from tqdm import tqdm
from dataclasses import dataclass
from typing import List, Dict, Tuple, DefaultDict, FrozenSet
import functools
import itertools

from collections import defaultdict


@dataclass
class Valve:
    name: str
    is_open: bool
    flow_rate: int
    edges: List[str]


@dataclass
class Graph:
    nodes: Dict[str, Valve]
    comp_nodes: DefaultDict[Tuple[Valve,Valve], int]

    # Floyd-warshall
    def compress_nodes(self):
        for k,i,j in itertools.product(self.nodes, self.nodes, self.nodes):
            self.comp_nodes[i,j] = min(self.comp_nodes[i,j], self.comp_nodes[i,k] + self.comp_nodes[k,j])
        self.fs = frozenset(name for name, valve in self.nodes.items() if valve.flow_rate!=0)


    def find_max(self, ele=False):
        self.flows = {key:valve.flow_rate for key,valve in self.nodes.items()}
        
        @functools.cache
        def search(time, pos, vs, ele=False):
            return max([ self.flows[v] * (time-self.comp_nodes[pos,v]-1) +
                search(time - self.comp_nodes[pos,v]-1, v, vs-{v}, ele)
                for v in vs if self.comp_nodes[pos,v]< time] +
                [search(26,'AA',vs,False) if ele else 0])

        return search(26, 'AA', self.fs, ele) if ele else search(30, 'AA', self.fs)




def minimise_pressure(filename: str):
    cmd_lines= []
    with open(filename, 'r') as file:
        cmd_lines = file.readlines()

    graph = Graph({}, defaultdict(lambda:1000))
    for line in cmd_lines:
        split_line = line.strip().replace('=',' ').replace(';',' ').replace(',','').split(' ') 
        valve_list = split_line[11:]
        valve_name = split_line[1]
        flow_rate = split_line[5]
        
        graph.nodes[valve_name] = Valve(valve_name, False, int(flow_rate), valve_list)
        for v in valve_list:
            graph.comp_nodes[valve_name, v] = 1

    graph.compress_nodes()
    part_one = graph.find_max()
    part_two = graph.find_max(ele=True)
    return part_one, part_two


  

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_sixteen.txt"     
    
    part_one, part_two = minimise_pressure(file_loc)
    
    print(f"(Part One): {part_one}     (Part Two): {part_two}")   
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")  
