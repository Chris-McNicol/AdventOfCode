
from time import perf_counter_ns


def file_system_build(filename):
    file_system, current_path = {}, ['']
    with open(filename, 'r') as file:        
        for line in file:
            if line.strip() == "$ cd /":
                current_path = ['']
            elif line.strip() == "$ cd ..":
                current_path.pop()
            elif line.strip()[0:5] == "$ cd ":
                current_path.append(line.strip()[5:])
                file_system['/'.join(current_path)] = 0
            elif line.strip()[0].isdigit():
                size, name = line.strip().split(' ')
                file_system['/'.join(current_path) + '/' + name] = int(size)
    return file_system


def dir_size(file_system, dir_path):
    return sum([v for k,v in file_system.items() if dir_path in k])


def dir_size_dict(file_system):
    size_dict = {}
    for key in file_system.keys():
        if key not in size_dict:
            dir_path = '/'.join(key.split('/')[:-1])
            size_dict[dir_path] =  dir_size(file_system, dir_path)
            
    return size_dict


def total_under_val(size_dict, val):
    return sum([v for k,v in size_dict.items() if v <= val])


def min_over_val(size_dict, val):
    return min([v for k,v in size_dict.items() if v >= val])


def unused_space(file_system, total_disk_space):    
    counter = sum([v for k,v in file_system.items()])
    return total_disk_space - counter



if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_seven.txt"
    file_system = file_system_build(file_loc)
    size_dict = dir_size_dict(file_system)

    total_disk_space = 70000000
    space_required = 30000000
 
    print(total_under_val(size_dict, val=100000))  
    
    free_space = unused_space(file_system,total_disk_space)
    #print("Free space: ", free_space)
    #print("Need to free: ", space_required - free_space)
    print(min_over_val(size_dict, space_required-free_space))
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")
