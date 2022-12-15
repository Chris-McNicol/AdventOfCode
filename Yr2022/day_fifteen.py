from time import perf_counter_ns
import numpy as np
from dataclasses import dataclass
from typing import Tuple, List
import itertools
from tqdm import tqdm


class Sensor:
    def __init__(self, own_pos: Tuple[int, int], nrst_b: Tuple[int, int]):
        self.own_pos = own_pos
        self.nrst_b = nrst_b
        self.taxi = self.taxicab_distance


    @property
    def taxicab_distance(self):
        delta_x, delta_y = self.nrst_b[0]-self.own_pos[0], self.nrst_b[1]-self.own_pos[1]
        return abs(delta_x) + abs(delta_y)


    def in_range(self, test_pos):
        delta_x, delta_y = test_pos[0]-self.own_pos[0], test_pos[1]-self.own_pos[1]
        return abs(delta_x) + abs(delta_y) <= self.taxi


    def annulus(self):
        result = set()
        for dx in range(0, self.taxi+2):
            dy = self.taxi + 1 - dx
            result.add((self.own_pos[0]+dx, self.own_pos[1]+dy))
            ### Don't need to generate these as can just check NE and SW sectors
            #result.add((self.own_pos[0]-dx, self.own_pos[1]+dy))
            #result.add((self.own_pos[0]+dx, self.own_pos[1]-dy))
            result.add((self.own_pos[0]-dx, self.own_pos[1]-dy))
        return result
    

    def get_conjugate_coord(self, coord, is_min=True, is_y=True):
        dist = self.own_pos[1] - coord if is_y else self.own_pos[0] - coord
        conj_dist = abs(dist)-self.taxi if is_min else self.taxi - abs(dist)
        return self.own_pos[0] + conj_dist if is_y else self.own_pos[1] + conj_dist


@dataclass
class SensorList:
    sensors: List[Sensor]

    def is_sensor_in_range(self, test_pos):
        for sensor in self.sensors:
            if sensor.in_range(test_pos):
                return True
        return False


    def is_beacon(self, test_pos):
        for sensor in self.sensors:
            if test_pos == sensor.nrst_b:
                return True
        return False


    def annulus_set(self):
        result = set()
        result_list = []
        for sensor in tqdm(self.sensors):
            result_list.append(sensor.annulus())        
        for pair in tqdm(list(itertools.combinations(result_list, 2))):
            onions = pair[0].intersection(pair[1])
            result = result.union(onions)
        return result
          

    def check_row(self, row_idx, speed_mode=True):
        min_x = min([sens.get_conjugate_coord(row_idx) for sens in self.sensors if abs(sens.own_pos[1]-row_idx) <= sens.taxi ])
        max_x = max([sens.get_conjugate_coord(row_idx, is_min=False) for sens in self.sensors if abs(sens.own_pos[1]-row_idx) <= sens.taxi  ])
        if speed_mode:
            return max_x - min_x
        in_range_counter = 0
        for x in tqdm(range(min_x, max_x+1)):
            if self.is_sensor_in_range((x, row_idx)) and not self.is_beacon((x, row_idx)):
                in_range_counter += 1
        return in_range_counter


    def search_space(self, big):         
        min_x, max_x = 0, big
        min_y, max_y = 0, big 
        for (x,y) in tqdm(self.annulus_set()):
            if min_x<=x<=max_x and min_y<=y<=max_y:
                if not self.is_sensor_in_range((x,y)):
                    return x*big + y                    
        return None
        

def find_beacons(filename: str):
    cmd_lines= []
    with open(filename, 'r') as file:
        cmd_lines = file.readlines()

    sensor_list = SensorList([])
    for line in cmd_lines:
        split_line = line.strip().replace('=',',').replace(':',',').split(',')
        sens_x, sens_y = int(split_line[1]), int(split_line[3])
        b_x, b_y = int(split_line[-3]), int(split_line[-1])
        sensor_list.sensors.append( Sensor((sens_x, sens_y), (b_x,b_y)))

    row_idx = 2_000_000
    part_one = sensor_list.check_row(row_idx, speed_mode=True)   
    part_two = sensor_list.search_space(big = 4_000_000)
    return part_one, part_two
  

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_fifteen.txt"     
    part_one, part_two = find_beacons(file_loc)
    print(f"(Part One): {part_one}     (Part Two): {part_two}")   
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1e9:.0f} seconds")  
