from time import perf_counter_ns


def head_instruction(rope, dir_char):
    char_map = {'U':(0,1), 'D':(0,-1), 'L':(-1,0), 'R':(1,0)}
    rope[0] = ( rope[0][0] + char_map[dir_char][0],
                 rope[0][1] + char_map[dir_char][1])


def tail_follow(rope, idx):
    delta_x, delta_y = rope[idx][0]-rope[idx+1][0], rope[idx][1]-rope[idx+1][1]
    norm_delta_x = delta_x/abs(delta_x) if delta_x != 0 else 0
    norm_delta_y = delta_y/abs(delta_y) if delta_y != 0 else 0
    if delta_x == 0 and abs(delta_y) > 1:
        rope[idx+1] = (rope[idx+1][0], rope[idx+1][1] + norm_delta_y)
    elif delta_y == 0 and abs(delta_x) > 1:
        rope[idx+1] = (rope[idx+1][0] + norm_delta_x, rope[idx+1][1])
    elif abs(delta_x) > 1 or abs(delta_y) > 1:
        rope[idx+1] = (rope[idx+1][0] + norm_delta_x, rope[idx+1][1] + norm_delta_y)


def update_rope(rope):
    for idx, knot in enumerate(rope[:-1]):
        tail_follow(rope, idx)
   

def simulate_rope(filename: str, num_knots: int = 10):
    tail_pos_history = []
    rope = [(0,0) for _ in range(num_knots)]
    with open(filename, 'r') as file:
        for line in file:
            dir_char, num_steps_str = line.strip().split(' ')
            for _step in range(int(num_steps_str)):
                head_instruction(rope, dir_char)
                update_rope(rope)
                tail_pos_history.append(rope[-1])        
    return len(set(tail_pos_history))

     

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_nine.txt"
    
    first_part = simulate_rope(file_loc, num_knots=2)
    second_part = simulate_rope(file_loc, num_knots=10)    
    print (f"Unique Tail Positions (Part One): {first_part}  (Part Two): {second_part}")    
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")


