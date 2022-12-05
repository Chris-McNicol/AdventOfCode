from time import perf_counter_ns


def calculate_total_priority(filename):
    contain_counter = 0
    overlap_counter = 0
    with open(filename, 'r') as file:
        for line in file:
            elf_one, elf_two = line.split(',')
            elf_one_lo, elf_one_hi = [int(x) for x in elf_one.split('-')]
            elf_two_lo, elf_two_hi = [int(y) for y in elf_two.split('-')]
            overlap_len = min(elf_one_hi,elf_two_hi) - max(elf_one_lo, elf_two_lo)

            if overlap_len >=0:
                overlap_counter += 1
                if (overlap_len == elf_one_hi-elf_one_lo) or (overlap_len== elf_two_hi-elf_two_lo): 
                    contain_counter += 1
            
    return contain_counter, overlap_counter


if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_four.txt"
    print(calculate_total_priority(file_loc))
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")
