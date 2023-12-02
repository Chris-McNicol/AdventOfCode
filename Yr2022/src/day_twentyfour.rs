use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use std::collections::{HashSet, HashMap};
use std::hash::Hash;
use std::cmp;

type Pos = (i32,i32);
type BlockMap = HashMap<usize, HashSet<Pos>>;


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_twentyfour.txt";
    //let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\example.txt";
    let (part_one, part_two) = path_find(file_name);
    println!("Part One: {}  Part Two:  {}", part_one, part_two);
    let duration = start.elapsed();    
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


#[derive(Copy, Clone, Eq, PartialEq, Hash)]
struct State {
    pos: Pos,
    time: usize,
    stage_one: bool,
    stage_two: bool,
}

fn search_for_best_path(blocked: &BlockMap, max_x: i32, max_y: i32) -> (usize,usize) {
    let start_pos: Pos = (0,-1);
    let end_pos: Pos = (max_x-1, max_y);
    let mut queue: Vec<State> = Vec::new();
    queue.push(State {pos: start_pos, time:0, stage_one:false, stage_two:false} );

    let mut state_cache: HashSet<State> = HashSet::new();
    let mut best_one: usize = usize::MAX;
    let mut best_two: usize = usize::MAX;

    while let Some( state ) = queue.pop() {
        let mut stg_one = state.stage_one;
        let mut stg_two = state.stage_two;

        if state.time > 1000 || state_cache.contains(&state) {
            continue;
        }

        state_cache.insert(state);
        if state.pos == start_pos && stg_one { stg_two = true; }

        if state.pos == end_pos { 
            stg_one = true;
            best_one = cmp::min(best_one, state.time);
            if stg_two { best_two = cmp::min(best_two, state.time); }        
        }

        let left = (state.pos.0-1, state.pos.1);
        let right = (state.pos.0+1, state.pos.1);
        let up = (state.pos.0, state.pos.1-1);
        let down = (state.pos.0, state.pos.1+1);
        for dir in vec![left, right, up, down, state.pos] {
            if ((0..=max_x-1).contains(&dir.0) && (0..=max_y-1).contains(&dir.1)) || dir == start_pos || dir == end_pos {
                let mod_time: usize = (state.time+1)%(max_x as usize * max_y as usize) ;
                if !blocked[&mod_time].contains(&dir) {
                    queue.push(State {pos:dir,time:state.time+1, stage_one:stg_one, stage_two:stg_two});
                }
            }
        }
    }
    return (best_one, best_two);
}


fn print_blocked(blocked: &BlockMap, time: usize, max_x: i32, max_y: i32) {
    let mut top_line: String = String::new();
    let mut bottom_line: String = String::new();
    let mut row_list: Vec<String> = Vec::new();
    let mut val_list: Vec<(i32,i32)> = Vec::new();
    top_line.push('#');
    top_line.push('.');
    for _i in 0..max_x {
        top_line.push('#');
        bottom_line.push('#');
    }
    bottom_line.push('.');
    bottom_line.push('#');
    for y in 0..max_y {
        let mut row_str = String::new();
        row_str.push('#');
        for x in 0..max_x {
            if blocked[&time].contains(&(x,y)) {
                row_str.push('X');
                val_list.push((x,y));
            }
            else {
                row_str.push('.');
            }          
        }
        row_str.push('#');
        row_list.push(row_str.clone());
    }
    println!("{}", top_line);
    for row in row_list {
        println!("{}", row);
    }
    println!("{}", bottom_line);
    println!("{:?}", val_list);
}

      
fn add_to_blocked(pos: Pos, ch: char, blocked: &mut BlockMap, max_x: i32, max_y:i32) {
    let max_lim = (max_x*max_y) as usize;
    for i in 0..=max_lim {
        match ch {
            '<' => {blocked.get_mut(&i).map(|v| v.insert( ((pos.0 - i as i32).rem_euclid(max_x), pos.1)));},
            '>' => {blocked.get_mut(&i).map(|v| v.insert( ((pos.0 + i as i32).rem_euclid(max_x), pos.1)));},
            'v' => {blocked.get_mut(&i).map(|v| v.insert( (pos.0, (pos.1 + i as i32).rem_euclid(max_y))));},
            '^' => {blocked.get_mut(&i).map(|v| v.insert( (pos.0, (pos.1- i as i32).rem_euclid(max_y))));},
            _ => {},
        }
    }
}


fn path_find(my_file_name: &str) -> (usize, usize){        
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();
    let line_vec: Vec<String> = buf_lines.map(|l| l.expect("Fail to parse")).collect();
    let max_y = (line_vec.len() - 2) as i32;
    let max_x = (line_vec[0].len() - 2) as i32;
    let mut blocked : BlockMap = HashMap::new();
    let max_lim = (max_x*max_y) as usize;
    for i in 0..=max_lim {
        blocked.insert( i, HashSet::new());
    }

    for line_idx in 1..(max_y+2) {
        for ch_idx in 1..(max_x+2) {
            let pos = (ch_idx-1, line_idx-1);
            if let Some(ch) = line_vec[line_idx as usize ].chars().nth(ch_idx as usize) {
                add_to_blocked(pos, ch, &mut blocked, max_x, max_y);
            }
        }        
    }

    let do_print_blocked = false;
    if do_print_blocked {
        for i in 0..18 { print_blocked(&blocked, i, max_x, max_y);}
    }
    
    let (part_one, part_two) = search_for_best_path(&blocked, max_x, max_y);
    return (part_one, part_two);
}


