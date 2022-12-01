from time import perf_counter


def get_elves_calories(filename):
    elf_cal_list = []
    current_calorie_counter = 0
    with open(filename, 'r') as file:
        for line in file:
            if not line.strip().isdigit():
                elf_cal_list.append(current_calorie_counter)
                current_calorie_counter = 0
            else:
                current_calorie_counter += int(line.strip())

    return elf_cal_list


def get_max_sum(filename, num_of_maxs):
    elf_cal_list = get_elves_calories(filename)
    elf_cal_list.sort(reverse=True)
    print(elf_cal_list[0:num_of_maxs])
    return sum(elf_cal_list[0:num_of_maxs])



if __name__ == "__main__":
    time_start = perf_counter()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\2022\Day_One\puzzle_input_one.txt"
    print(get_max_sum(file_loc, 3))
    print(f"Elapsed time : {(perf_counter() - time_start)*1000000:.1f} microseconds")
