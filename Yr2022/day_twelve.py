from time import perf_counter_ns
import numpy as np
from tqdm import tqdm
import dijkstar


def load_landscape(filename: str):
    cmd_lines = []
    arr = []    
    with open(filename, 'r') as file:
        cmd_lines = file.readlines()
    for line in cmd_lines:
        arr_row = [ord(x) - 96 for x in line.strip()]
        arr.append(arr_row)
    
    arr = np.array(arr)
    start_pos = np.argwhere(arr == -13)[0]
    target_pos = np.argwhere(arr == -27)[0]
    arr[start_pos[0]][start_pos[1]] = 1
    arr[target_pos[0]][target_pos[1]] = 26

    graph = dijkstar.Graph()
    down_graph = dijkstar.Graph()  
    for idx, val in np.ndenumerate(arr):  
        up_idx, dwn_idx = (idx[0]-1, idx[1]), (idx[0]+1, idx[1])
        lft_idx, rt_idx = (idx[0], idx[1]-1), (idx[0], idx[1]+1)
        for tst in [up_idx, dwn_idx, lft_idx, rt_idx]:
            try:
                if arr[tst] <= val + 1:
                    graph.add_edge(idx, tst, 1)
                    down_graph.add_edge(tst, idx, 1)
            except IndexError:
                pass
       
    path = dijkstar.find_path(graph, (start_pos[0],start_pos[1]), (target_pos[0], target_pos[1]))
    print("Total Cost (Part One)", path.total_cost)    

    min_counter = 1e6
    for idx, val in tqdm(np.ndenumerate(arr)):
        if arr[idx] == 1 and idx[1] == 0: # only need to check the left most positions
            try:
                test_path = dijkstar.find_path(graph, idx, (target_pos[0], target_pos[1]))
                min_counter = min(min_counter, test_path.total_cost)
            except dijkstar.algorithm.NoPathError:
                pass
    print("Part 2 solution: ", min_counter)
    
    return arr, start_pos, target_pos
     

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_twelve.txt"  
    landscape = load_landscape(file_loc)   
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")
    