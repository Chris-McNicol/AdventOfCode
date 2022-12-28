from time import perf_counter_ns

SNAFU_MAP ={'=':-2, '-':-1, '0':0, '1':1, '2':2}
SNAFU_REMAINDER_MAP ={3:'=', 4:'-', 0:'0', 1:'1', 2:'2'}


def snafu_to_decimal(snafu_str):
    rev = reversed(snafu_str)
    result = 0
    for char_idx, char in enumerate(rev):
        result += SNAFU_MAP[char] * (5**char_idx)
    return result


def decimal_to_snafu(dec):
    result, n = "", dec
    while n != 0:
        remainder = n % 5
        result = SNAFU_REMAINDER_MAP[remainder] + result
        n = (n+2) // 5
    return result

        
def snafu_it(filename: str):    
    with open(filename, 'r') as file:
        cmd_lines = file.readlines()    
    snafu_lines = []
    for line in cmd_lines:
        snafu_lines.append(snafu_to_decimal(line.strip()))

    part_one = decimal_to_snafu(sum(snafu_lines))       
    part_two = None
    return part_one, part_two
  

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_twentyfive.txt"
    #file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\example.txt"
        
    part_one, part_two = snafu_it(file_loc)
    
    print(f"(Part One): {part_one}     (Part Two): {part_two}")   
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")  
