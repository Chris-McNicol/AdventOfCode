from time import perf_counter_ns
from typing import List

def get_common_item(input_rucksack: str):
    first, second = input_rucksack[:len(input_rucksack)//2], input_rucksack[len(input_rucksack)//2:]
    return ''.join( set(first).intersection(set(second)) )

def get_common_item_group(input_list : List):
    first, second, third = input_list[0], input_list[1], input_list[2]
    return ''.join( set(first).intersection(set(second)).intersection(set(third)) )

def get_priority(input_char: str):
    ord_shift = 38 if input_char.isupper() else 96
    return ord(input_char) - ord_shift

def calculate_total_priority(filename):
    priority_counter = 0
    badge_priority_counter = 0 
    group_list = []
    with open(filename, 'r') as file:
        for line in file:
            priority_counter += get_priority(get_common_item(line))
            group_list.append(line.strip())
            if len(group_list) == 3:
                badge_priority_counter += get_priority(get_common_item_group(group_list))
                group_list = []                      
    return priority_counter, badge_priority_counter


if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_three.txt"
    print(calculate_total_priority(file_loc))
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")
