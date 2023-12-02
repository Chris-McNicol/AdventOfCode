import re

def get_lines(file):
    with open(file, 'r') as in_file:
        result_lines =  in_file.readlines()
    return result_lines


digit_map = {r'one':1, r'two':2, r'three':3, r'four':4, r'five':5,
             r'six':6, r'seven':7, r'eight':8, r'nine':9, r'\d{1}':None}
digit_regex_str = '(?=(' + '|'.join(list(digit_map.keys())) + '))'

def digit_from_match(match):
    return int(match.group(1)) if match.group(1).isdigit() else digit_map[match.group(1)]

def parse_lines(raw_lines, part_two=False):
    digit_list = []
    for line in raw_lines:
        if part_two:
            digits = [digit_from_match(match) for match in re.finditer(digit_regex_str, line)]
        else:
            digits = [i for i in line if i.isdigit()]
        digit_list.append(10*int(digits[0]) + int(digits[-1]))
    return digit_list


if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day01.txt'
    part_one = sum(parse_lines(get_lines(filename)))
    part_two = sum(parse_lines(get_lines(filename), part_two = True))    
    print(f"Part One: {part_one}    Part Two:  {part_two}")