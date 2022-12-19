from time import perf_counter_ns
from tqdm import tqdm
from queue import PriorityQueue
import functools


def check_resources(blue, resources):
    
    ore_able =  resources[0] >= blue[0]
    clay_able =  resources[0] >= blue[1]
    obs_able = resources[0] >= blue[2][0] and resources[1] >= blue[2][1]
    geode_able = resources[0] >= blue[3][0] and resources[2] >= blue[3][1]
    return ore_able, clay_able, obs_able, geode_able

def projected_resources(resources, robots, total_mins):
    return (resources[0] + robots[0]*total_mins,
            resources[1] + robots[1]*total_mins,
            resources[2] + robots[2]*total_mins,
            resources[3] + robots[3]*total_mins)

def max_resource_requirements(blue, total_mins):
    return ( total_mins* max([blue[0], blue[1], blue[2][0], blue[3][0]]),
             total_mins* blue[2][1],
             total_mins* blue[3][1] )
        


@functools.cache
def check_blueprint_dfs(blue, resources = (0, 0, 0, 0), robots = (1, 0, 0, 0), total_mins=24):
    if total_mins <= 0 :
        return resources[-1]

    potential_resources, potential_robots  = [], []
    ore_able, clay_able, obs_able, geode_able = check_resources(blue, resources)    
    proj_resources = projected_resources(resources, robots, total_mins)
    max_reqs = max_resource_requirements(blue, total_mins)

    if not geode_able:# and not (obs_able and total_mins>=2):
        potential_resources.append((resources[0] + robots[0],
                                    resources[1] + robots[1],
                                    resources[2] + robots[2],
                                    resources[3] + robots[3]))
        potential_robots.append((robots[0], robots[1], robots[2], robots[3]))
    
    if ore_able and not obs_able and not geode_able and proj_resources[0] <= max_reqs[0]: #and not clay_able:
        potential_resources.append((resources[0] + robots[0] - blue[0],
                                    resources[1] + robots[1],
                                    resources[2] + robots[2],
                                    resources[3] + robots[3]))
        potential_robots.append((robots[0] + 1, robots[1], robots[2], robots[3]))

    if clay_able and not obs_able and not geode_able and proj_resources[1] <= max_reqs[1]:
        potential_resources.append((resources[0] + robots[0] - blue[1],
                                    resources[1] + robots[1],
                                    resources[2] + robots[2],
                                    resources[3] + robots[3]))
        potential_robots.append((robots[0], robots[1] + 1, robots[2], robots[3]))
        
    if obs_able and not geode_able and proj_resources[2] <= max_reqs[2]:# and total_mins >=2:
        potential_resources.append((resources[0] + robots[0] - blue[2][0],
                                    resources[1] + robots[1] - blue[2][1],
                                    resources[2] + robots[2],
                                    resources[3] + robots[3]))
        potential_robots.append((robots[0], robots[1], robots[2] + 1, robots[3]))

    if geode_able:
        potential_resources.append((resources[0] + robots[0] - blue[3][0],
                                    resources[1] + robots[1],
                                    resources[2] + robots[2] - blue[3][1],
                                    resources[3] + robots[3]))
        potential_robots.append((robots[0], robots[1], robots[2], robots[3] + 1))

    if len(potential_resources) == 0 or len(potential_robots) == 0 :
        return resources[-1]
    best_geode = max([check_blueprint_dfs(blue, res, rob, total_mins-1) for res,rob in zip(potential_resources, potential_robots)])
    return best_geode


def priority(state):
    (_, mined, _, _) = state
    return (1000*mined[3] + 100*mined[2] + 10*mined[1] + mined[0])


@functools.cache
def check_blueprint_bfs(blue, resources = (0, 0, 0, 0), robots = (1, 0, 0, 0), total_mins=24,
                        max_queue_length = 5000):
    
    #queue = PriorityQueue()    
    mined = (0,0,0,0)
    queue = list()
    queue.append((resources, mined, robots, total_mins))
    
    max_geodes = 0    
    prune_depth = total_mins + 1
    visited = set()
    while queue:        
        state = queue.pop(0)
        if state in visited:
            continue
        visited.add(state)
        
        resources, mined, robots, total_mins = state
        new_mined = tuple([mined[i] + robots[i] for i in range(4)])
      
        if total_mins <= 0:
            max_geodes = max(max_geodes, mined[3])            
            continue

        if total_mins < prune_depth:
            queue.sort(key=priority, reverse=True)
            queue = queue[:max_queue_length]
            prune_depth = total_mins

        ore_able, clay_able, obs_able, geode_able = check_resources(blue, resources)    

        if not geode_able:# and not (obs_able and total_mins>=2):
            poss_state =  ((resources[0] + robots[0],
                            resources[1] + robots[1],
                            resources[2] + robots[2],
                            resources[3] + robots[3]),
                            new_mined,
                            (robots[0], robots[1], robots[2], robots[3]),
                            total_mins-1)
            queue.append(poss_state)
        
        if ore_able:# and not obs_able and not geode_able and proj_resources[0] <= max_reqs[0]: #and not clay_able:
            poss_state = ((resources[0] + robots[0] - blue[0],
                            resources[1] + robots[1],
                            resources[2] + robots[2],
                            resources[3] + robots[3]),
                            new_mined,
                            (robots[0] + 1, robots[1], robots[2], robots[3]),
                            total_mins-1)
            queue.append(poss_state)

        if clay_able:# and not obs_able and not geode_able and proj_resources[1] <= max_reqs[1]:
            poss_state = ((resources[0] + robots[0] - blue[1],
                            resources[1] + robots[1],
                            resources[2] + robots[2],
                            resources[3] + robots[3]),
                            new_mined,
                            (robots[0], robots[1] + 1, robots[2], robots[3]),
                            total_mins-1)
            queue.append(poss_state)
            
        if obs_able:# and not geode_able and proj_resources[2] <= max_reqs[2]:# and total_mins >=2:
            poss_state = ((resources[0] + robots[0] - blue[2][0],
                            resources[1] + robots[1] - blue[2][1],
                            resources[2] + robots[2],
                            resources[3] + robots[3]),
                            new_mined,
                            (robots[0], robots[1], robots[2] + 1, robots[3]),
                            total_mins-1)
            queue.append(poss_state)

        if geode_able:
            poss_state = ((resources[0] + robots[0] - blue[3][0],
                            resources[1] + robots[1],
                            resources[2] + robots[2] - blue[3][1],
                            resources[3] + robots[3]),
                            new_mined,
                            (robots[0], robots[1], robots[2], robots[3] + 1),
                            total_mins-1)
            queue.append(poss_state)
            
    return max_geodes



def evaluate_blueprints(filename: str):
    cmd_lines= []
    with open(filename, 'r') as file:
        cmd_lines = file.readlines()
    blueprint_list= []
    for line in cmd_lines:
        split_line = line.split(' ')
        blueprint_list.append( (int(split_line[6]), int(split_line[12]),
                             (int(split_line[18]),int(split_line[21])),
                              (int(split_line[27]),int(split_line[30])) ))

    part_one = 0
    for blue_idx, blue in enumerate(blueprint_list):
        max_geode_val = check_blueprint_bfs(blue, max_queue_length=5000)
        part_one += (blue_idx + 1)*max_geode_val

    part_two = 1
    for blue_idx_two, blue_two in enumerate(blueprint_list[:3]):
        max_geode_val = check_blueprint_bfs(blue_two, total_mins = 32, max_queue_length=10000)
        part_two *= max_geode_val

    return part_one, part_two
  

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_nineteen.txt"     
    #file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\example.txt"     
    
    part_one, part_two = evaluate_blueprints(file_loc)
    
    print(f"(Part One): {part_one}     (Part Two): {part_two}")   
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")  
