from time import perf_counter_ns


def get_register(filename: str):
    register_list, register = [], 1
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() == "noop":
                register_list.append(register)
            else:
                register_list.append(register)
                register_list.append(register)
                register += int(line.strip().split(' ')[-1])
    return register_list


def calc_signal_strength(register_list, line_breaks):
    return sum( register_list[i-21] * (i-20) for i in line_breaks)


def print_screen(register_list, line_breaks):
    output_str = ""
    for idx, register in enumerate(register_list):
        if idx in line_breaks:
            output_str += '\n'
        output_str += "X" if abs(idx%40 - register) <= 1 else " "        
    print(output_str)

     

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_ten.txt"
    line_breaks = [40*i for i in range(1,7)]
    register_list = get_register(file_loc)   
    sum_sig_strength = calc_signal_strength(register_list, line_breaks)    
    print (f"Sum of signal strength (Part One): {sum_sig_strength}  (Part Two):")   
    print_screen(register_list, line_breaks)
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")


