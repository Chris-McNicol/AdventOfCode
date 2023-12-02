from time import perf_counter_ns
from tqdm import tqdm


def shift_em(orig_list, num_shifts=10, decrypt_key = 811589153):
    pair_list = list(enumerate(val * decrypt_key for val in orig_list))
    
    for pair in pair_list * num_shifts:
        start_idx = pair_list.index(pair)
        pair_list.pop(start_idx)
        new_idx = (start_idx+pair[1]) % len(pair_list)
        pair_list.insert( new_idx , pair)
       
    zero_pos = [end_idx for end_idx, (_, val) in enumerate(pair_list) if val == 0][0]
       
    sum_list = []
    for point in [1000, 2000, 3000]:
        new_point_index = (zero_pos + point) % len(pair_list)
        sum_list.append(pair_list[new_point_index][1])
    print("SUM LIST ", zero_pos,  sum_list)
    return sum(sum_list)
    


def apply_shifts(filename: str):
    cmd_lines= []
    with open(filename, 'r') as file:
        cmd_lines = file.readlines()
    
    orig_list = [int(x.strip()) for x in cmd_lines]
        
    part_one = shift_em(orig_list, num_shifts=1, decrypt_key=1)    
    part_two = shift_em(orig_list, num_shifts=10, decrypt_key=811589153)
    
    return part_one, part_two
  

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_twenty.txt"     
    #file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\example.txt"     
    
    part_one, part_two = apply_shifts(file_loc)
    
    print(f"(Part One): {part_one}     (Part Two): {part_two}")   
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")  
