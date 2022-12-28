from time import perf_counter_ns


def search_for_best_path(blocked, max_x, max_y):
    queue, start_point, end_point = [], (0,-1), (max_x-1, max_y)
    init_state = (start_point,0, False, False)
    queue.append(init_state)
    state_cache = {}
    best_time_part_one, best_time_part_two = None, None
    
    while queue:
        state = queue.pop(0)        
        pos, time, stage_one, stage_two = state        
        if time > 1000 or state in state_cache:
            continue
        state_cache[state] = None
        if pos == start_point and stage_one:
            stage_two = True
        if pos == end_point:
            stage_one = True
            if stage_two:
                best_time_part_two = time if best_time_part_two is None else min(best_time_part_two, time)
            best_time_part_one = time if best_time_part_one is None else min(best_time_part_one, time)
        
        left, right = (pos[0]-1, pos[1]), (pos[0]+1, pos[1])
        up, down = (pos[0], pos[1]-1), (pos[0], pos[1]+1)
        for dir in [left, right, up, down, pos]:
            if (0<=dir[0]<=max_x-1 and 0<=dir[1]<=max_y-1) or dir in [start_point, end_point]:
                if dir not in blocked[(time+1) % (max_x*max_y)]:
                    queue.append((dir, time+1, stage_one, stage_two))
    return best_time_part_one, best_time_part_two
        

def wrap_val(val, max_val):
    if 0 <= val <= max_val -1:
        return val
    if val < 0:
        return (val)%max_val
    return val % (max_val)


def print_board(blocked, time, max_x, max_y):
    top_line = "#." + "#"*(max_x)
    bottom_line = "#"*(max_x) + ".#"
    val_list, row_list = "", []
    for y in range(0, max_y):
        row_str = "#"
        for x in range(0, max_x):
            if (x,y) in blocked[time]:
                row_str += "X"
                val_list += " (" + str(x) + "," + str(y) + ")"
            else:
                row_str += "."
        row_list.append(row_str+"#")
    print(top_line)
    for row in row_list:
        print(row)
    print(bottom_line)
    print(val_list)
        
        
def pathfind(filename: str):    
    with open(filename, 'r') as file:
        cmd_lines = file.readlines()
    
    left,right,up,down =  set(), set(), set(), set()
    blocked = {}
    max_x, max_y = 0,0
    for line_idx, line in enumerate(cmd_lines):
        max_y = max(max_y, line_idx-1)
        for char_idx, char in enumerate(line.strip()):
            max_x = max(max_x, char_idx-1)
            if char == '>':
                right.add( (char_idx-1, line_idx-1 ))
            if char == 'v':
                down.add( (char_idx-1, line_idx-1 ))
            if char == '^':
                up.add( (char_idx-1, line_idx-1 ))
            if char == '<':
                left.add( (char_idx-1, line_idx-1))

    for i in range(0, (max_x)*(max_y)):
        blocked_this_turn = set()
        for pos_l in left:
            new_pos = (wrap_val(pos_l[0] - i, max_x), pos_l[1])
            blocked_this_turn.add(new_pos)        
        for pos_r in right:            
            new_pos = (wrap_val(pos_r[0] + i, max_x), pos_r[1])
            blocked_this_turn.add(new_pos)
        for pos_u in up:            
            new_pos = (pos_u[0], wrap_val(pos_u[1] - i, max_y))
            blocked_this_turn.add(new_pos)
        for pos_d in down:            
            new_pos = (pos_d[0], wrap_val(pos_d[1] + i, max_y))
            blocked_this_turn.add(new_pos)
        
        blocked[i] = blocked_this_turn
        
    part_one, part_two = search_for_best_path(blocked, max_x, max_y)

    return part_one, part_two
  

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_twentyfour.txt"
    #file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\example.txt"
        
    part_one, part_two = pathfind(file_loc)
    
    print(f"(Part One): {part_one}     (Part Two): {part_two}")   
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")  
