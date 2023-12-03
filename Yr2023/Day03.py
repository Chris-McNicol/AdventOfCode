from dataclasses import dataclass
from typing import List

def get_lines(file):
    with open(file, 'r') as in_file:
        result_lines =  in_file.readlines()
    result_lines = [line.strip() for line in result_lines]
    return result_lines

def find_numbers(lines):
    found_nums = []
    for line_idx, line in enumerate(lines):
        num_str, num_start, num_end = '', 0, 0
        for char_idx, char in enumerate(line):
            if char.isdigit():
                if num_str == '':
                    num_start = char_idx
                num_str += char
            elif num_str != '':
                num_end = char_idx - 1
                found_nums.append((num_str, line_idx, num_start, num_end))
                num_str, num_start, num_end = '', 0, 0
        if num_str != '':
            found_nums.append((num_str, line_idx, num_start, len(line)-1))
          

    return found_nums

def contains_symbol(in_str):
    for i_char in in_str:
        if i_char != '.' and not i_char.isdigit():
            return True
    return False

def check_num(lines, num):
    num_str, line_idx, start, end = num   
    found_symbol = False
    if line_idx > 1:
        found_symbol |= contains_symbol(lines[line_idx-1][max(start-1, 0):min(end+2, len(lines[line_idx-1]))])
    if line_idx < len(lines) - 2:
        found_symbol |= contains_symbol(lines[line_idx+1][max(start-1,0):min(end+2, len(lines[line_idx+1]))])
    if start > 0:
        found_symbol |= contains_symbol(lines[line_idx][start-1])
    if end < len(lines[line_idx]) - 2:
        found_symbol |= contains_symbol(lines[line_idx][end+1])
    return found_symbol


def check_nearby_nums(found_nums, line_idx, char_idx):
    nearby_nums = []
    for num_str, num_line, num_start, num_end in found_nums:
        if abs(num_line-line_idx) < 2 and char_idx >= num_start-1 and char_idx <= num_end + 1:
            nearby_nums.append(int(num_str))
    if len(nearby_nums) == 2:
        return nearby_nums[0] * nearby_nums[1]
    return 0

def check_gears(lines, found_nums):
    gear_ratio = 0
    for line_idx, line in enumerate(lines):        
        for char_idx, char in enumerate(line):
            if char == '*':
                gear_ratio += check_nearby_nums(found_nums, line_idx, char_idx)
    return gear_ratio



if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day03.txt' 
    lines = get_lines(filename)    
    found_nums = find_numbers(lines) 
    part_one = sum([int(num[0]) for num in found_nums if check_num(lines, num)])
    part_two = check_gears(lines, found_nums)
    print(f"Part One: {part_one}    Part Two:  {part_two}")