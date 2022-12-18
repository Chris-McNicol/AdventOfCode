from time import perf_counter_ns
from tqdm import tqdm
from dataclasses import dataclass
from typing import List, Dict, Tuple, DefaultDict, FrozenSet
import functools
import itertools

import numpy as np

import matplotlib.pyplot as plt



CACHE_DEPTH=10

@dataclass
class TetrisShape:
    #origin is bottom left
    origin: Tuple[int, int]
    width: int
    height: int
    arr: np.array

    def set_depth(self, start_depth):
        self.origin = (start_depth, 2)

    def wind_shift(self, board_arr, right):
        result_str = "WIND RIGHT " if right else "WIND LEFT"
        if right and self.origin[1]+self.width <= board_arr.shape[1]-1:
            if not self.collides(board_arr, xshift=+1, yshift=-1):
                #self.origin[0] += 1
                self.origin = (self.origin[0], self.origin[1] + 1)
                result_str += " succesful"
            else:
                result_str += " collided"
        elif right:
                result_str += " bounced"
        if not right and self.origin[1] > 0:
            if not self.collides(board_arr, xshift=-1, yshift=-1):
                #self.origin[0] -= 1
                self.origin = (self.origin[0], self.origin[1] - 1)
                result_str += " successful"
            else:
                result_str += " collided"
        elif not right:
                result_str += " bounced"
        return result_str

    def fall(self):
        self.origin = (self.origin[0] + 1, self.origin[1])

    def board_sub_arr_idx(self, board_arr):
        comp_arr_width = min(self.arr.shape[1], board_arr.shape[1] - self.origin[1])
        ymin, ymax = self.origin[0]-2, self.origin[0]+2
        #ymin, ymax = self.origin[0]-3+yshift, self.origin[0]+1+yshift
        #xmin, xmax = self.origin[0], self.origin[0]+comp_arr_width
        xmin, xmax = self.origin[1], self.origin[1]+self.width
        return ymin, ymax, xmin, xmax

    def shape_x_idx(self, board_arr):
        #shape_xmax = min(self.arr.shape[0], board_arr.shape[0]-self.origin[0])
        shape_xmax = self.origin[1] + self.width
        return shape_xmax

    def collides(self, board_arr, xshift=0, yshift=0):
        #board_width = board_arr.shape[0]
        #comp_arr_width = min(self.arr.shape[0], board_width - self.origin[0])
        #sub_arr = board_arr[self.origin[1]-3:self.origin[1]+2][self.origin[0]:self.origin[0]+4]
        #ymin, ymax = self.origin[1]-2, self.origin[1]+2
        #xmin, xmax = self.origin[0], self.origin[0]+comp_arr_width
        ymin, ymax, xmin, xmax = self.board_sub_arr_idx(board_arr)
        ymin, ymax = ymin+yshift, ymax+yshift
        xmin, xmax = xmin+xshift, xmax+xshift
        #shape_xmax = self.shape_x_idx(board_arr)
        board_sub_arr = board_arr[ymin:ymax,xmin:xmax]
        
        #shape_sub_arr = self.arr[:, 0:shape_xmax]
        shape_sub_arr = self.arr[:, 0:self.width]

        #print("ORIGIN", self.origin, ymin, ymax, xmin, xmax, shape_xmax)
        #print("BOARD ARR", board_sub_arr, "->", board_sub_arr.shape)
        #print("SHAPE ARR", shape_sub_arr, "->", shape_sub_arr.shape)
        #print("-------------------------")
        """
        #sub_arr = board_arr[8087][0]
        
        print("BOARD ARR", board_arr[self.origin[1]][:])
        
        
        print("-------------------------")
        print("-------------------------")
        print("-------------------------")
        print("SHAPE ARR ", self.arr)
        print("-------------------------")
        print("-------------------------")
        print("-------------------------")
        print("-------------------------")
        """

        collide = np.logical_and(shape_sub_arr, board_sub_arr).sum() > 0
        #if collide:
        #    print(shape_sub_arr)
        #    print("------------------------")
        #    print(board_sub_arr)
        return collide


class Long(TetrisShape):
    def __init__(self):
        self.width, self.height = 4, 1
        self.arr = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[1,1,1,1]])

class Tall(TetrisShape):
    def __init__(self):
        self.width, self.height = 1, 4
        self.arr = np.array([[1,0,0,0],[1,0,0,0],[1,0,0,0],[1,0,0,0]])

class Cross(TetrisShape):
    def __init__(self):
        self.width, self.height = 3, 3
        self.arr = np.array([[0,0,0,0],[0,1,0,0],[1,1,1,0],[0,1,0,0]])

class Corner(TetrisShape):
    def __init__(self):
        self.width, self.height = 3, 3
        self.arr = np.array([[0,0,0,0],[0,0,1,0],[0,0,1,0],[1,1,1,0]])

class Square(TetrisShape):
    def __init__(self):
        self.width, self.height = 2, 2
        self.arr = np.array([[0,0,0,0],[0,0,0,0],[1,1,0,0],[1,1,0,0]])




class TetrisBoard:
    def __init__(self, winds:List[bool], board_width:int = 7, board_depth: int = 8088):
        self.arr =  np.zeros(shape=(board_depth, board_width))
        #with np.nditer(self.arr, op_flags=['readwrite']) as it:
        #    for idx, x in enumerate(it):
        #        x[...] = idx

        #set floor
        self.arr[board_depth-1] = np.ones(shape=(board_width))
                
        self.top_line: int = board_depth-2
        #self.winds = itertools.cycle(winds)
        self.winds = winds
        self.wind_idx = 0
        #self.shapes = itertools.cycle([Long(), Cross(), Corner(), Tall(), Square()])
        self.shapes = [Long(), Cross(), Corner(), Tall(), Square()]
        self.shape_idx = 0

        #print("Initialised", self.shapes)
        
    @property
    def hash_wind(self):
        overlap = CACHE_DEPTH - (len(self.winds) - 1 - self.wind_idx)
        if overlap >= 0:
            result = self.winds[self.wind_idx:].extend(self.winds[0:overlap])
        else:
            result = self.winds[self.wind_idx: self.wind_idx+CACHE_DEPTH]
        result_hash = 0
        for ele_idx, ele in enumerate(result):
            val = 1 if ele else 0
            result_hash = result_hash + (val << ele_idx)
        self.wind_idx = self.wind_idx + 1 if self.wind_idx < len(self.winds)-1 else 0
        return result_hash

    @property
    def wind(self):
        result = self.winds[self.wind_idx]
        self.wind_idx = self.wind_idx + 1 if self.wind_idx < len(self.winds)-1 else 0
        return result

    @property
    def shape(self):
        result = self.shapes[self.shape_idx]
        self.shape_idx = self.shape_idx + 1 if self.shape_idx < len(self.shapes)-1 else 0
        return result

    def shape_stop(self, shape):
        ymin, ymax, xmin, xmax = shape.board_sub_arr_idx(self.arr)
        #shape_xmin, shape_xmax = shape.origin[0] , self.arr.shape[0]-shape.origin
        shape_xmax = shape.shape_x_idx(self.arr)
        self.arr[ymin-1:ymax-1,xmin:xmax] = np.logical_or(self.arr[ymin-1:ymax-1,xmin:xmax],
                                                         shape.arr[:, 0:shape.width ])

        #self.arr[shape.origin[1]-4:shape.origin[1],
        #        shape.origin[0]:shape.origin[0]+shape.width+1] = shape.arr
        old_top_line = self.top_line
        self.top_line = min(self.top_line, shape.origin[0] - shape.height)
        return old_top_line - self.top_line



    def shape_stop_fast(self, shape):
        ymin, ymax, xmin, xmax = shape.board_sub_arr_idx(self.arr)
        
        #shape_xmax = shape.shape_x_idx(self.arr)
        self.arr[ymin-1:ymax-1,xmin:xmax] = np.logical_or(self.arr[ymin-1:ymax-1,xmin:xmax],
                                                         shape.arr[:, 0:shape.width ])

        new_bottom = self.arr.shape[0]
        for x_idx in range(0, self.arr.shape[1]):
            new_bottom = min(new_bottom, (self.arr[:, x_idx] != 0).argmax(axis=0))
        shift = self.arr.shape[0] - new_bottom
        self.arr = np.roll(self.arr, shift, axis=0)
        #old_top_line = self.top_line
        #self.top_line = min(self.top_line, shape.origin[0] - shape.height)
        self.top_line = min(self.top_line, shape.origin[0] - shape.height) + shift
        #return old_top_line - self.top_line
        return shift

    def add_shape_plot(self, shape_number=0):
        
        #shape = next(self.shapes)
        shape = self.shape[self.shape_idx]
        shape.set_depth(self.top_line - 3)
        not_collided, turn_idx = True, 0
        
        while (not_collided):
            #self.plot(shape, shape_idx, turn_idx, 'MOVE')
            turn_idx += 1
            r_str = shape.wind_shift(right = self.wind, board_arr=self.arr)
            #self.plot(shape, shape_idx, turn_idx, r_str)
            turn_idx += 1            
            if shape.collides(self.arr):
                not_collided = False
            else:
                shape.fall()
        
        shift = self.shape_stop(shape)
        self.plot(shape, shape_number, turn_idx, 'STOP ' + str(shift) )
        return shift

    def add_shape(self, shape): # shape_number=0):
        #hash_arr = tuple(tuple(row) for row in self.arr.astype(int))
        #hash_wind = self.hash_wind(self.wind_idx)
        #print(hash_arr)
        
        #shape = next(self.shapes)
        #shape = self.shape[self.shape_idx]
        shape.set_depth(self.top_line - 3)
        not_collided, turn_idx = True, 0
        
        while (not_collided):
            
            r_str = shape.wind_shift(right = self.wind, board_arr=self.arr)
            
            if shape.collides(self.arr):
                not_collided = False
            else:
                shape.fall()
        
        shift = self.shape_stop(shape)
        
        return tuple(tuple(row) for row in self.arr.astype(int)), shift





    def shift_arr(self, shift=50):
        #self.arr[self.arr.shape[0]//2:] = self.arr[:self.arr.shape[0]//2]
        #self.arr[:self.arr.shape[0]//2] = np.zeros(shape=(self.arr.shape[0]//2, self.arr.shape[1]))
        #return self.arr.shape[0]//2
        self.arr = np.roll(self.arr, shift, axis=0)
        self.top_line += shift

    def play(self, num_shapes: int = 2022, plot=False):
        
        
        shifted = []
        for i in tqdm(range(0, num_shapes)):
            plot  = True if 990<i<1005 else False
            #shift = self.add_shape_plot(i, plot)
            shift = self.add_shape(i, plot)
            if shift > 0:
                #print(shift)
                #shifted += shift
                shifted.append(shift)
                if i > 10:
                    self.shift_arr(shift)
            
        print(self.arr.shape[0], self.top_line)
        print(shifted)
        print(sum(shifted))
        return self.arr.shape[0] - self.top_line -2


        
    def play_fast(self, num_shapes: int = 2022):
        
        state_cache = {}
        state = tuple(tuple(row) for row in self.arr.astype(int))
        shifter = 0
        
        for i in tqdm(range(0, num_shapes)):
            
            wind_hash = self.hash_wind
            shape = self.shape
            shape_idx = self.shape_idx
            
            if (shape_idx, wind_hash, state) in state_cache:
                state, shift = state_cache[(shape_idx, wind_hash, state)]

            else:
                state, shift = self.add_shape(shape)
                state_cache[(shape_idx, wind_hash, state)] = state, shift
            
            shifter += shift
            
        print("SHIFTER ", shifter)
        return shifter

    def plot(self, shape, shape_idx, turn_idx, title='BLANK'):
        fig,ax = plt.subplots(figsize=(10,8))
        #print(self.arr.sum(), self.)
        #print(np.sum(self.arr < 0))
        plot_arr = np.copy(self.arr)
        ymin, ymax, xmin, xmax = shape.board_sub_arr_idx(plot_arr)
        #shape_xmin, shape_xmax = shape.origin[0] , self.arr.shape[0]-shape.origin
        #shape_xmax = shape.shape_x_idx(plot_arr)
        plot_arr[ymin-1:ymax-1,xmin:xmax] = plot_arr[ymin-1:ymax-1,xmin:xmax] + \
                                                    (-1) * shape.arr[:, 0:shape.width ]
        ax.imshow(plot_arr[-100:,:])
        ax.set_title(title)
        dir = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\vis\tetris"
        out_img_name = f"{dir}_{shape_idx}_{turn_idx}.png"
        fig.savefig(out_img_name)

        






def play_tetris(filename: str):
    cmd_lines= []
    with open(filename, 'r') as file:
        cmd_lines = file.readlines()

    example_line = ">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"        

    #wind_list = [char == '>' for char in cmd_lines[0].strip()]
    wind_list = [char == '>' for char in example_line]
    #for char in cmd_lines[0].strip():

    debug = True
    do_plots = False
    #num_shapes = 2022
    num_shapes = 1_000_000_000_000

    if debug:
        num_shapes = 5
        do_plots = True


    board = TetrisBoard(winds=wind_list, board_depth=10)
        
    #part_one = board.play(num_shapes=num_shapes, plot=do_plots)
    part_one = board.play_fast(num_shapes=num_shapes)
    
    return part_one, None


  

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_seventeen.txt"     
    
    part_one, part_two = play_tetris(file_loc)
    
    print(f"(Part One): {part_one}     (Part Two): {part_two}")   
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")  
