from time import perf_counter_ns


def add_visible_char(row_str, current_cycle, register_val):
    row_idx = current_cycle-1
    while (row_idx > 39):
        row_idx -= 40
    append_char = "#" if abs(row_idx - register_val) <= 1 else "."
    return row_str + append_char


def calc_signal_strength(filename: str, line_breaks):
    sig_strength = {k-20:0 for k in line_breaks}
    current_cycle, register_val, screen_row = 1, 1, ""

    with open(filename, 'r') as file:
        for line in file:
            screen_row = add_visible_char(screen_row, current_cycle, register_val)
            if current_cycle in sig_strength.keys():
                sig_strength[current_cycle] = current_cycle * register_val
            line_list = line.strip().split(' ')
            if line_list[0].strip() == "noop":
                current_cycle += 1
                continue
            ##ELSE
            if current_cycle + 1 in sig_strength.keys():
                sig_strength[current_cycle+1] = (current_cycle+1) * register_val
            screen_row = add_visible_char(screen_row, current_cycle+1, register_val)
            current_cycle += 2
            register_val += int(line_list[1])

    sum_sig_strength = sum([v for k,v in sig_strength.items()])
    
    for brk_idx, brk in enumerate(line_breaks[:-1]):
        print(screen_row[brk: line_breaks[brk_idx+1]])
    return sum_sig_strength

     

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_ten.txt"
    line_breaks = [40*i for i in range(0,7)]
        
    sum_sig_strength = calc_signal_strength(file_loc, line_breaks)
    
    print (f"Sum of signal strength (Part One): {sum_sig_strength}  (Part Two): ^^^^ ")    
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")


