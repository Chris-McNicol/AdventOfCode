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
class Node:
    id: str
    left: str
    right: str

    @classmethod
    def from_line(cls, line):
        split_line = line.split(' ')
        return Node(split_line[0].strip(), split_line[2][1:-1], split_line[3][:-1])


@dataclass
class NodeMap:
    instructions: str
    nodes : Dict

    @classmethod
    def from_line_arr(cls, lines):
        instructs = lines[0]
        node_list = [Node.from_line(line) for line in lines[2:]]
        nodes = {node.id:node for node in node_list}
        return NodeMap(instructs, nodes)
    
    def follow_instructions(self):
        counter = 0
        current_node = self.nodes['AAA']
        while current_node.id != 'ZZZ':
            next_node_str = self.instructions[counter % len(self.instructions)]
            next_node_id = current_node.left if next_node_str == 'L' else current_node.right
            current_node = self.nodes[next_node_id]
            counter += 1
        return counter
       
    def follow_instructions_ghost(self):        
        current_nodes = [node for node_name, node in self.nodes.items() if node.id[-1] == 'A']
        counter_list = []
        for current_node in tqdm.tqdm(current_nodes):
            counter = 0
            while current_node.id[-1] != 'Z':
                next_node_str = self.instructions[counter % len(self.instructions)]
                next_node_id = current_node.left if next_node_str == 'L' else current_node.right
                current_node = self.nodes[next_node_id]
                counter += 1
            counter_list.append( counter)
        return reduce(math.lcm, counter_list)


if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day08.txt' 
    lines = get_lines(filename)
    nodemap = NodeMap.from_line_arr(lines)    
    part_one = nodemap.follow_instructions()
    part_two = nodemap.follow_instructions_ghost()    
    print(f"Part One: {part_one}    Part Two:  {part_two}")
