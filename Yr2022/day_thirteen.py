from time import perf_counter_ns
import ast
import functools


def custom_compare(one, two):
    one_is_int = isinstance(one,int)
    two_is_int = isinstance(two,int)
    if one_is_int and two_is_int:        
        return ((one < two), (one == two))

    elif not one_is_int and not two_is_int:
        for one_val, two_val in zip(one, two):
            right, equal =  custom_compare(one_val, two_val)
            if equal:
                continue
            else:
                return (right, equal)
        return ((len(one) < len(two)), (len(one) == len(two)))
    
    else:
        new_one = [one] if one_is_int else one
        new_two = [two] if two_is_int else two
        return custom_compare(new_one, new_two)


def comparator(left, right):
    good, equal = custom_compare(left,right)
    if equal:
        return 0
    return -1 if good else 1


def parse(line:str):
    line = line.strip()
    if line.isnumeric():
            return int(line)
    if line != "":
        if line[0] == '[':
            line = line[1:]
        if line[-1] == ']':
            line = line[:-1]       
        line_list = line.split(',')
        print(line_list)
        for idx in range(0, len(line_list)):
            line_list[idx] = parse(line_list[idx])
        return line_list
    else:
        return line

def dumb_parse(line:str):
    this_list = []
    print("Parsing ", line)
    line_iter = iter(line)
    checking_new = False
    #for char_idx, char in enumerate(line):
    #for char_idx, char in enumerate(line_iter):
    for char_idx in range(0, len(line)):
        print("            ", this_list)
        #if char == '[':
        if line[char_idx] == '[':
            recursive_list = dumb_parse( line[char_idx+1:] )
            this_list.append(recursive_list)
            char_idx += len(recursive_list)
            checking_new = True
            #while (char != ']') :
            #    next(line_iter, None)
        #elif char.isnumeric() and not checking_new:
        #    this_list.append(int(char))
        elif line[char_idx].isnumeric() and not checking_new:
            this_list.append(int(line[char_idx]))
            
        #elif char == ']' and not checking_new:
        elif line[char_idx] == ']' and not checking_new:
            return this_list
    return this_list



def parse_eval(line:str):
    line_list = ast.literal_eval(line)
    return line_list


def load_pairs(filename: str):
    cmd_lines, pair_list = [], [],
    sum_good_pair_indices = 0
    
    with open(filename, 'r') as file:
        cmd_lines = file.readlines()
    #for line_idx in range(0, len(cmd_lines), 3):
    for line_idx in range(0, 4, 3):
        #first = parse_eval(cmd_lines[line_idx])
        #second = parse_eval(cmd_lines[line_idx+1])
        first = dumb_parse(cmd_lines[line_idx].strip()[1:-1])
        second = dumb_parse(cmd_lines[line_idx+1].strip()[1:-1])

        pair_list.append(first)
        pair_list.append(second)

        print(first)
        print(second)

        good_order, equal = custom_compare(first, second)
        pair_idx = (line_idx // 3) + 1    
        sum_good_pair_indices += pair_idx if good_order else 0
    
    div_packet_one, div_packet_two = [[2]], [[6]]
    pair_list.append(div_packet_one)
    pair_list.append(div_packet_two)

    sorted_pair_list = sorted(pair_list, key=functools.cmp_to_key(comparator))
    
    divider_packets = 1
    for element_idx, element in enumerate(sorted_pair_list):
        if element in [div_packet_one, div_packet_two]:
            divider_packets *= (element_idx+1)  

    return sum_good_pair_indices, divider_packets
     

if __name__ == "__main__":
    time_start = perf_counter_ns()
    #file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_thirteen.txt" 
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\example.txt" 
    sum_good_pair_indices, divider_packets = load_pairs(file_loc)
    print(f"Sum of good pair indices (Part One): {sum_good_pair_indices}")
    print(f"Product of divider packet indices  (Part Two): {divider_packets}")
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")
    
