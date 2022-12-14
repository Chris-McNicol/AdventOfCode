from time import perf_counter_ns
import numpy as np


def add_rock_pair(one, two, rock_arr):
    delta_y, delta_x = two[0]-one[0], two[1]-one[1]
    dx = 0 if delta_x == 0 else delta_x//abs(delta_x)
    dy = 0 if delta_y == 0 else delta_y//abs(delta_y)
    inter = one
    while (inter != two):
        rock_arr[inter] = 1
        inter = (inter[0]+dy, inter[1]+dx)
    rock_arr[two] = 1


def add_sand_unit(rock_arr):
    sand_point, part_one, part_two = (0, 500), False, False
    while not part_one and not part_two:
        below = (sand_point[0]+1, sand_point[1])
        dwn_left = (sand_point[0]+1, sand_point[1]-1)
        dwn_right = (sand_point[0]+1, sand_point[1]+1)
        if rock_arr[below] == 0:
            sand_point = below
        elif rock_arr[dwn_left] == 0:
            sand_point = dwn_left
        elif rock_arr[dwn_right] == 0:
            sand_point = dwn_right
        else:
            rock_arr[sand_point] = -1
            part_one = (sand_point[0] == rock_arr.shape[0]-2)
            part_two = (sand_point == (0, 500))
            break       
    return part_one, part_two


def darude(rock_arr):
    counter, counter_list = 0, []
    one_finished, two_finished = False,False
    while not one_finished or not two_finished:
        part_one, part_two = add_sand_unit(rock_arr)        
        one_finished = one_finished | part_one
        two_finished = two_finished | part_two
        if one_finished:
            counter_list.append(counter)
        counter += 1
    one_count = min(counter_list)
    two_count = max(counter_list)+1
    return one_count, two_count
        

def build_rocks(filename: str):
    cmd_lines, rock_lists = [], []   
    with open(filename, 'r') as file:
        cmd_lines = file.readlines()

    max_y = 0
    for line in cmd_lines:
        pairs = line.split(' -> ')
        this_list = []
        for pair in pairs:
            y = int(pair.split(',')[1])
            x = int(pair.split(',')[0])
            max_y = max(y, max_y)
            this_list.append((y,x))
        rock_lists.append(this_list)
    
    rock_arr = np.zeros(shape=(max_y + 3, 1000))
    for rock_list in rock_lists:
        for idx in range(0, len(rock_list)-1):
            add_rock_pair(rock_list[idx], rock_list[idx+1], rock_arr)

    for col_idx in range(0, rock_arr.shape[1]):
        rock_arr[rock_arr.shape[0]-1][col_idx] = 1
    return rock_arr


if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_fourteen.txt" 
    
    rock_arr = build_rocks(file_loc, True)
    part_one, part_two = darude(rock_arr)
    print(f"(Part One): {part_one}     (Part Two): {part_two}")   
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")  
