from time import perf_counter_ns

from queue import LifoQueue



########## LOGIC USING STACKS

def put_stack_from_line(stack_list, input_line):
    for char_idx, char in enumerate(input_line):
        if char not in [' ', '[',']', '\n']:
            stack_list[(char_idx - 1)//4].put(char)

def initialise_stacks(stack_initialiser_q):
    stack_list = []
    for character in stack_initialiser_q.get():
        if character.isdigit():
            stack_list.append(LifoQueue())
    while not stack_initialiser_q.empty():
        put_stack_from_line(stack_list, stack_initialiser_q.get())
    return stack_list


def shift_single_crate(stack_list, origin_idx, dest_idx):
    stack_list[dest_idx].put(stack_list[origin_idx].get())


def shift_multi_crates(stack_list, origin_idx, dest_idx, num_crates):
    for i in range(0,num_crates):
        shift_single_crate(stack_list, origin_idx, dest_idx)


def shift_multi_crates_no_reverse(stack_list, origin_idx, dest_idx, num_crates):
    transfer_list = []
    for i in range(0,num_crates):
        transfer_list.append(stack_list[origin_idx].get())
    for item in reversed(transfer_list):
        stack_list[dest_idx].put(item)


def calculate_tops_stacks(filename, reverse=False):
    stack_initialiser_q = LifoQueue()
    initialising_stacks = True
    stack_list = []    
    with open(filename, 'r') as file:        
        for line in file:
            if initialising_stacks:
                if line.strip() == "":
                    initialising_stacks = False
                    stack_list = initialise_stacks(stack_initialiser_q)
                else:
                    stack_initialiser_q.put(line)
            
            else:
                line_break = [int(x) for x in line.strip().split(' ') if x.isdigit()]
                if reverse:
                    shift_multi_crates(stack_list, line_break[1]-1, line_break[2]-1, line_break[0])
                else:
                    shift_multi_crates_no_reverse(stack_list, line_break[1]-1, line_break[2]-1, line_break[0])

    result_list = []
    for stack in stack_list:
        result_list.append(stack.get())            
    return result_list



########## LOGIC USING STRINGS



def initialise_strings(string_initialiser_list):
    max_stack_idx = int(string_initialiser_list[-1].strip()[-1])
    result_string_list = ["" for x in range(0, max_stack_idx)]
    for line in reversed(string_initialiser_list[0:-1]):
        for i in range(0, max_stack_idx):
            char_idx = i*4 + 1
            if line[char_idx] != ' ':
                result_string_list[i] += line[char_idx]
    return result_string_list
            

def transfer_strings(string_list, origin_idx, dest_idx, num_crates, reverse=False):
    string_list[origin_idx], to_transfer = string_list[origin_idx][0:-num_crates], string_list[origin_idx][-num_crates:]
    transfer_list = to_transfer[::-1] if reverse else to_transfer
    string_list[dest_idx] += transfer_list


def calculate_tops_strings(filename, reverse=False):
    initialising_stacks = True
    string_initialiser_list = []
    string_list = []
    with open(filename, 'r') as file:        
        for line in file:
            if initialising_stacks:
                if line.strip() == "":
                    initialising_stacks = False
                    string_list = initialise_strings(string_initialiser_list)
                else:
                    string_initialiser_list.append(line)
            else:
                line_break = [int(x) for x in line.strip().split(' ') if x.isdigit()]              
                transfer_strings(string_list, line_break[1]-1, line_break[2]-1, line_break[0], reverse)
    return [each_string[-1] for each_string in string_list]



if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_five.txt"
    reverse = False
    #print(calculate_tops_stacks(file_loc, reverse))    
    print(calculate_tops_strings(file_loc, reverse))    

    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")
