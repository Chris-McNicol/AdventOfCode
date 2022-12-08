from time import perf_counter_ns

def is_distinct(char_idx, line, length):
    return char_idx >= length and len(set(line[char_idx:char_idx+length])) == length


def find_starts(filename):
    packet_start, msg_start = None, None
    with open(filename, 'r') as file:        
        line = file.readline()
        for char_idx, _ in enumerate(line):
            if is_distinct(char_idx, line, 4) and packet_start is None:
                packet_start = char_idx + 4
            if is_distinct(char_idx, line, 14) and msg_start is None:
                msg_start = char_idx + 14
                break                     
    return packet_start, msg_start


if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_six.txt"
    print(find_starts(file_loc))  
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")
