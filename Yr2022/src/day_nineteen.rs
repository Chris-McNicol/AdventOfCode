use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use std::collections::{HashSet, VecDeque};
use std::cmp;

type Quad = (usize, usize, usize, usize);
type BluePrint = (usize, usize, (usize,usize), (usize,usize));
type State = (Quad, Quad, Quad, usize);


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_nineteen.txt";
    //let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\example.txt";
    let (part_one, part_two) = mine_geodes(file_name);
    let duration = start.elapsed();    
    println!("Part One: {}  Part Two: {}", part_one, part_two);
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn check_resources(blue : &BluePrint, resources: &Quad) -> (bool, bool, bool, bool) {
    let ore_able = resources.0 >= blue.0;
    let clay_able = resources.0 >= blue.1;
    let obs_able = resources.0 >= blue.2.0 && resources.1 >= blue.2.1;
    let geode_able = resources.0 >= blue.3.0 && resources.2 >= blue.3.1;
    return (ore_able, clay_able, obs_able, geode_able);
}


fn check_blueprint_bfs(blue: &BluePrint, arg_total_mins:usize, max_queue_length:usize) -> usize {
    let mut mined : Quad = (0,0,0,0);
    let mut queue : VecDeque<State> = VecDeque::new();
    let mut total_mins: usize = arg_total_mins;
    let mut resources: Quad = (0, 0, 0, 0);
    let mut robots: Quad = (1, 0, 0, 0);
    queue.push_back( (resources, mined, robots, total_mins) );   

    let mut max_geodes : usize = 0;
    let mut prune_depth: usize = total_mins + 1;
    let mut visited: HashSet<State> = HashSet::new();    
    
    while let Some(state) = queue.pop_front()  {
        if visited.contains(&state) {continue;}
        
        (resources, mined, robots, total_mins) = state;
        visited.insert(state);

        let new_mined: Quad = (mined.0+robots.0, mined.1+robots.1, mined.2+robots.2, mined.3+robots.3);
        let new_resources: Quad = (resources.0+robots.0, resources.1+robots.1, resources.2+robots.2,resources.3+robots.3);

        if total_mins <= 0 {
            max_geodes = cmp::max(max_geodes, mined.3);
            continue;
        }

        if total_mins < prune_depth && queue.len() > max_queue_length{
            queue.make_contiguous().sort_by_key(|k| cmp::Reverse(k.1.0 + 10*(k.1.1) + 100*(k.1.2) + 1000*(k.1.3)));
            queue.drain(max_queue_length..);
            prune_depth = total_mins;
        }

        let (ore_able, clay_able, obs_able, geode_able) = check_resources(&blue, &resources);
        if !geode_able {
            queue.push_back( (new_resources, new_mined, robots, total_mins-1));
        }
        if ore_able {
            queue.push_back( ( (new_resources.0-blue.0, new_resources.1, new_resources.2, new_resources.3),
                         new_mined, (robots.0+1, robots.1, robots.2, robots.3), total_mins - 1));
        }
        if clay_able {
            queue.push_back( ( (new_resources.0-blue.1, new_resources.1, new_resources.2, new_resources.3),
                         new_mined, (robots.0, robots.1+1, robots.2, robots.3), total_mins - 1));
        }
        if obs_able {
            queue.push_back( ( (new_resources.0-blue.2.0, new_resources.1 - blue.2.1, new_resources.2, new_resources.3),
                         new_mined, (robots.0, robots.1, robots.2+1, robots.3), total_mins - 1));
        }
        if geode_able {
            queue.push_back( ( (new_resources.0-blue.3.0, new_resources.1, new_resources.2-blue.3.1, new_resources.3),
                         new_mined, (robots.0, robots.1, robots.2, robots.3+1), total_mins - 1));
        }
    }
    return max_geodes;
}


fn mine_geodes(my_file_name: &str) -> (usize, usize) {
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();
    let line_vec: Vec<String> = buf_lines.map(|l| l.expect("Fail to parse")).collect();   
    let mut blueprint_vec : Vec<BluePrint> = Vec::new();

    for line in line_vec {
        let ele_vec: Vec<&str> = line.trim().split(' ').collect();
        let blue: BluePrint = (ele_vec[6].parse::<usize>().unwrap(),
                               ele_vec[12].parse::<usize>().unwrap(),
                               (ele_vec[18].parse::<usize>().unwrap(),
                               ele_vec[21].parse::<usize>().unwrap()),
                               (ele_vec[27].parse::<usize>().unwrap(),
                               ele_vec[30].parse::<usize>().unwrap()));
        blueprint_vec.push(blue);
    }

    let mut part_one = 0;
    for (blue_idx, blue) in blueprint_vec.iter().enumerate() {
        let max_geode_val = check_blueprint_bfs(&blue, 24, 3000);
        part_one += (blue_idx +1) * max_geode_val;
    }    

    let mut part_two = 1;
    for blue_idx in 0..3 {
        let max_geode_val = check_blueprint_bfs(&blueprint_vec[blue_idx], 32, 20000);
        part_two *= max_geode_val;
    }    
    
    return (part_one, part_two);
}



