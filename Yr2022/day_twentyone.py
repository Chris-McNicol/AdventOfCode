from time import perf_counter_ns
from tqdm import tqdm
import ast

def build_dict(monkey_list, part_two=False, humn_guess=0):
    monkey_dict = {}
    for monkey in monkey_list:
        if part_two and monkey[0] == 'humn:':
            monkey_dict['humn'] = humn_guess
        elif monkey[-1].strip().isnumeric():
            monkey_dict[monkey[0][:-1]] = int(monkey[-1])
    
    info_updated = True
    while info_updated:
        info_updated = False
        for monkey in monkey_list:
            if len(monkey) == 2 or monkey[0][:-1] in monkey_dict:
                continue
            if monkey[1] in monkey_dict and monkey[3] in monkey_dict:
                if part_two and monkey[0] == 'root:':
                    monkey_dict['root'] = monkey_dict[monkey[1]] - monkey_dict[monkey[3]]
                elif monkey[2] == '*':
                    monkey_dict[monkey[0][:-1]] = monkey_dict[monkey[1]] * monkey_dict[monkey[3]]
                elif monkey[2] == '/':
                    monkey_dict[monkey[0][:-1]] = monkey_dict[monkey[1]] / monkey_dict[monkey[3]]
                elif monkey[2] == '+':
                    monkey_dict[monkey[0][:-1]] = monkey_dict[monkey[1]] + monkey_dict[monkey[3]]
                elif monkey[2] == '-':
                    monkey_dict[monkey[0][:-1]] = monkey_dict[monkey[1]] - monkey_dict[monkey[3]]
                else:
                    raise ValueError("NOT AN OPERATION IN + - * /")
                info_updated = True
    return monkey_dict

def test_val(cmd_lines, test_val):
    monkey_dict = build_dict(cmd_lines, True, test_val)
    return monkey_dict['root']

def same_sign(val1, val2):
    return val1 * val2 > 0

def find_humn_val(cmd_lines, low_guess=0, high_guess=10_000_000_000_000):    
    low_val = test_val(cmd_lines, low_guess)
    high_val = test_val(cmd_lines, high_guess)
    med_guess = (high_guess+low_guess)//2
    med_val = test_val(cmd_lines, med_guess)
    while (med_val != 0):        
        if same_sign(low_val, med_val):
            low_guess = med_guess
        if same_sign(high_val, med_val):
            high_guess = med_guess
        
        low_val = test_val(cmd_lines, low_guess)
        high_val = test_val(cmd_lines, high_guess)
        med_val = test_val(cmd_lines, med_guess)
        if high_val == low_val:
            break
        med_guess = med_guess - med_val*(high_guess-low_guess)/(high_val-low_val)
    
    return int(med_guess)
    

def understand_monkeys(filename: str):    
    with open(filename, 'r') as file:
        raw_cmd_lines = file.readlines()
    
    cmd_lines = []
    for line in raw_cmd_lines:
        cmd_lines.append(line.strip().split(' '))

    monkey_dict = build_dict(cmd_lines)   
    part_one = int(monkey_dict['root'])
    part_two = find_humn_val(cmd_lines)
    
    return part_one, part_two
  

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_twentyone.txt"     
    #file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\example.txt"     
    
    part_one, part_two = understand_monkeys(file_loc)
    
    print(f"(Part One): {part_one}     (Part Two): {part_two}")   
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")  
