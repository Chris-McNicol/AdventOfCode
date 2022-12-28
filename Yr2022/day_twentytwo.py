from time import perf_counter_ns
from tqdm import tqdm

from itertools import groupby
from enum import IntEnum
from typing import Tuple, Set, List, Dict

from dataclasses import dataclass

DIRECTION = {0:(1,0), 1:(0,1), 2:(-1,0), 3:(0,-1)}


class Side(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

@dataclass
class CubeFace:
    name: str
    xlims: Tuple[int, int]
    ylims: Tuple[int, int]
    right_target: Tuple[str, Side, bool]
    down_target: Tuple[str, Side, bool]
    left_target: Tuple[str, Side, bool]
    up_target: Tuple[str, Side, bool]

    @property
    def right_edge(self):
        return [(self.xlims[1], y) for y in range(self.ylims[0], self.ylims[1]+1) ]

    @property
    def left_edge(self):
        return [(self.xlims[0], y) for y in range(self.ylims[0], self.ylims[1]+1) ]

    @property
    def up_edge(self):
        return [(x, self.ylims[0]) for x in range(self.xlims[0], self.xlims[1]+1) ]

    @property
    def down_edge(self):
        return [(x, self.ylims[1]) for x in range(self.xlims[0], self.xlims[1]+1) ]
    
    def get_edge(self, side: Side):
        side_map = {Side.RIGHT: self.right_edge, Side.DOWN: self.down_edge, Side.LEFT: self.left_edge, Side.UP:self.up_edge}
        return side_map[side]

    def is_on_face(self, pos):
        x,y = pos
        if y > self.ylims[1]:
            return False, Side.DOWN
        if y < self.ylims[0]:
            return False, Side.UP
        if x > self.xlims[1]:
            return False, Side.RIGHT
        if x < self.xlims[0]:
            return False, Side.LEFT
        else:
            return True, None
        


@dataclass
class Cube:
    faces: Dict

    def make_map(self, face_set, target):
        target_name, target_side, reverse = target
        edge = self.faces[target_name].get_edge(target_side)
        edge = reversed(edge) if reverse else edge
        return {k:v for k,v in zip(face_set, edge)}


    def build_mappings(self):
        for face_key, face in self.faces.items():
            face.right_map = self.make_map(face.right_edge, face.right_target)
            face.down_map = self.make_map(face.down_edge, face.down_target)
            face.left_map = self.make_map(face.left_edge, face.left_target)
            face.up_map = self.make_map(face.up_edge, face.up_target)
            
    def get_map(self, face_name: str, off_dir: Side):
        if off_dir == Side.RIGHT:
            return self.faces[face_name].right_map, self.faces[face_name].right_target[1]
        if off_dir == Side.DOWN:
            return self.faces[face_name].down_map, self.faces[face_name].down_target[1]
        if off_dir == Side.LEFT:
            return self.faces[face_name].left_map, self.faces[face_name].left_target[1]
        if off_dir == Side.UP:
            return self.faces[face_name].up_map, self.faces[face_name].up_target[1]
        else:
            raise ValueError("UNEXPECTED SIDE GIVEN")

    def get_face(self, pos):
        for face_name, face in self.faces.items():
            if face.xlims[0]<=pos[0]<=face.xlims[1] and face.ylims[0]<=pos[1]<=face.ylims[1]:
                return face_name

    def get_dir_shift(self, off_dir: Side, on_dir: Side):
        if off_dir == on_dir:
            return 2
        if abs(off_dir - on_dir) == 2:
            return 0
        if on_dir - off_dir in [1, -3]: # normal , Up-to-right transition
            return 3
        else:      # on_dir - off_dir in [-1, 3] normal, right-to-up transition
            return 1


@dataclass
class Turtle:
    crse_idx: int
    pos : Tuple[int,int]
    free: Set[Tuple[int,int]]
    blocked: Set[Tuple[int,int]]
    x_lims: List[Tuple[int, int]]
    y_lims: List[Tuple[int, int]]
    is_cube: bool
    cube: Cube
    current_face: str

    def turn_right(self):
        self.crse_idx = 0 if self.crse_idx == 3 else self.crse_idx + 1
    
    def turn_left(self):
        self.crse_idx = 3 if self.crse_idx == 0 else self.crse_idx - 1

    def wrap_lims_linear(self, val, x_mode=True):        
        lims = self.x_lims[self.pos[1]] if x_mode else self.y_lims[self.pos[0]]
        if val < lims[0]:
            return lims[-1]
        elif val > lims[1]:
            return lims[0]
        else:
            return val

    
    def next_pos(self):
        dir = DIRECTION[self.crse_idx]
        new_x, new_y = self.pos[0] + dir[0], self.pos[1] + dir[1]
        wrap_new_x, wrap_new_y = self.wrap_lims_linear(new_x, True), self.wrap_lims_linear(new_y, False)
        if (wrap_new_x, wrap_new_y) in self.blocked:            
            return
        else:
            self.pos = (wrap_new_x, wrap_new_y)
            

    def next_pos_cube(self):
        dir = DIRECTION[self.crse_idx]
        new_x, new_y = self.pos[0] + dir[0], self.pos[1] + dir[1]
        on_face, off_dir = self.cube.faces[self.current_face].is_on_face( (new_x, new_y))
        if on_face:
            wrap_new_x, wrap_new_y = self.wrap_lims_linear(new_x, True), self.wrap_lims_linear(new_y, False)
        else:
            map, on_side = self.cube.get_map(self.current_face, off_dir)
            wrap_new_x, wrap_new_y = map[self.pos]

        if (wrap_new_x, wrap_new_y) in self.blocked:
            return
        else:
            self.pos = (wrap_new_x, wrap_new_y)
            
            if not on_face:
                self.current_face = self.cube.get_face(self.pos)                
                num_turns = self.cube.get_dir_shift(off_dir, on_side)
                for _i in range(0, num_turns):
                    self.turn_right()
            

    def follow_instructions(self, instructions):
        for ins in instructions:
            if ins == 'R':
                self.turn_right()
            elif ins == 'L':
                self.turn_left()
            else:
                steps = int(ins)
                for i in range(0, steps):
                    self.next_pos_cube() if self.is_cube else self.next_pos()
        password = 1000*(self.pos[1]+1) + 4*(self.pos[0]+1) + self.crse_idx 
        return password
        




def pathfind(filename: str):    
    with open(filename, 'r') as file:
        cmd_lines = file.readlines()
    
    free, blocked = set(), set()
    max_x, max_y = 0,0
    x_lims, y_lims = [], [] 
    for line_idx, line in enumerate(cmd_lines):
        max_y = max(max_y, line_idx)
        if line.strip() == "":
            break
        valid_x_pos = []
        for char_idx, char in enumerate(line[:-1]):
            max_x = max(max_x, char_idx)
            if char == '.':
                free.add((char_idx, line_idx))
                valid_x_pos.append(char_idx)
            elif char == '#':
                blocked.add((char_idx, line_idx))
                valid_x_pos.append(char_idx)
        x_lims.append( (min(valid_x_pos), max(valid_x_pos)))
    
    for x in range(0, max_x+1):
        valid_y_pos = []
        for y in range(0, len(cmd_lines)):
            if (x,y) in free or (x,y) in blocked:
                valid_y_pos.append(y)
            
        y_lims.append( (min(valid_y_pos), max(valid_y_pos)) )


    instructions = [''.join(s) for _,s in groupby(cmd_lines[-1].strip(), str.isalpha)]
    
    turtle_one = Turtle(0, (x_lims[0][0], 0), free, blocked, x_lims, y_lims, False,None, None )  
    part_one = turtle_one.follow_instructions(instructions)

    ####### RIGHT, DOWN, LEFT, UP

    A = CubeFace('A', (50, 99), (0, 49),    ('B',Side.LEFT,False), ('C',Side.UP,False), ('D',Side.LEFT, True), ('F', Side.LEFT, False))
    B = CubeFace('B', (100, 149), (0, 49),  ('E',Side.RIGHT, True), ('C',Side.RIGHT, False), ('A',Side.RIGHT, False), ('F',Side.DOWN, False))
    C = CubeFace('C', (50, 99), (50, 99),   ('B',Side.DOWN, False), ('E',Side.UP, False), ('D',Side.UP, False), ('A',Side.DOWN, False))
    D = CubeFace('D', (0, 49), (100, 149),  ('E',Side.LEFT, False), ('F',Side.UP, False), ('A',Side.LEFT, True), ('C',Side.LEFT, False))
    E = CubeFace('E', (50, 99), (100, 149), ('B',Side.RIGHT, True), ('F',Side.RIGHT, False), ('D',Side.RIGHT, False), ('C',Side.DOWN, False))
    F = CubeFace('F', (0, 49 ), (150, 199),  ('E',Side.DOWN, False), ('B',Side.UP, False), ('A',Side.UP, False), ('D',Side.DOWN, False))

    #A = CubeFace('A', (8,11), (0, 3),    ('F',Side.RIGHT,True), ('D',Side.UP,False), ('C',Side.UP, False), ('B', Side.UP, True))
    #B = CubeFace('B', (0,3), (4, 7),  ('C',Side.LEFT, False), ('E',Side.DOWN, True), ('F',Side.DOWN, True), ('A',Side.UP, True))
    #C = CubeFace('C', (4, 7), (4, 7),   ('D',Side.LEFT, False), ('E',Side.LEFT, True), ('B',Side.RIGHT, False), ('A',Side.LEFT, False))
    #D = CubeFace('D', (8, 11), (4, 7),  ('F',Side.UP, True), ('E',Side.UP, False), ('C',Side.RIGHT, False), ('A',Side.DOWN, False))
    #E = CubeFace('E', (8, 11), (8, 11), ('F',Side.LEFT, False), ('B',Side.DOWN, True), ('C',Side.DOWN, True), ('D',Side.DOWN, False))
    #F = CubeFace('F', (12, 15 ), (8, 11),  ('A',Side.RIGHT, True), ('B',Side.LEFT, True), ('E',Side.RIGHT, False), ('D',Side.RIGHT, True))

    cube = Cube({'A': A, 'B':B, 'C':C, 'D':D, 'E':E, 'F':F})
    cube.build_mappings()
    turtle_two = Turtle(0, (x_lims[0][0], 0), free, blocked, x_lims, y_lims, True,cube, 'A' )    
    part_two = turtle_two.follow_instructions(instructions)  
    
    return part_one, part_two
  

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_twentytwo.txt"     
    #file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\example.txt"     
    
    part_one, part_two = pathfind(file_loc)
    
    print(f"(Part One): {part_one}     (Part Two): {part_two}")   
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")  
