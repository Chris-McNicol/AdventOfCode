
from time import perf_counter_ns

import numpy as np



def make_array(filename: str):
    with open(filename, 'r') as file:
        arr = [list(line.strip()) for line in file]
    return np.array(arr)


def is_element_visible(arr, row_idx, col_idx):
    if row_idx in [0, arr.shape[0]-1] or col_idx in [0, arr.shape[1]-1]:
        return True
    visible = False
    left, right = arr[col_idx, 0:row_idx], arr[col_idx, row_idx+1:]
    up, down = arr[0:col_idx, row_idx], arr[col_idx+1:, row_idx]
    for direction in [left,right,up,down]:
        visible = visible or max(direction) < arr[col_idx, row_idx]
    return visible

def count_visible(arr):
    counter = 0
    for row_idx, col_idx in np.ndindex(arr.shape):
        if is_element_visible(arr, row_idx, col_idx):
            counter += 1
    return counter


def scenic_score(arr, row_idx, col_idx):
    if row_idx in [0, arr.shape[0]-1] or col_idx in [0, arr.shape[1]-1]:
        return 0

    left, right = arr[col_idx, 0:row_idx], arr[col_idx, row_idx+1:]
    up, down = arr[0:col_idx, row_idx], arr[col_idx+1:, row_idx]
    my_tree = arr[col_idx, row_idx]
    scenic_score = 1
    for dir_idx, direction in enumerate([left, right, up , down]):
        found_blocker = False
        iter_list = direction if dir_idx not in [0,2] else reversed(direction)
        for tree_idx, tree in enumerate(iter_list):
            if tree >= my_tree:
                scenic_score *= (tree_idx+1)
                found_blocker = True
                break
        if not found_blocker:
            scenic_score *= len(direction)

    return scenic_score

def max_scenic_score(arr):
    result = 0
    for row_idx, col_idx in np.ndindex(arr.shape):
        result = max(result, scenic_score(arr, row_idx, col_idx))    
    return result

     

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_eight.txt"
    
    arr = make_array(file_loc)
    vis_count = count_visible(arr)
    max_scenic_score = max_scenic_score(arr)
    print (f"Visible Trees : {vis_count} out of : {arr.size}")
    print (f"Maximum Scenic Score: {max_scenic_score}")
    
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")

