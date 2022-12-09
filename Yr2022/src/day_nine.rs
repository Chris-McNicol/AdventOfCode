use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;
use std::collections::HashSet;

type RopeVec = Vec<(i32,i32)>;
type RopeSet = HashSet<(i32,i32)>;


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_nine.txt";
    let first_part = simulate_rope(file_name, 2);
    let second_part = simulate_rope(file_name, 10);    
    let duration = start.elapsed();
    println!("Part One: {}    Part Two : {}", first_part, second_part);
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}


fn head_instruction(rope: &mut RopeVec, dir_char: &str){
    match dir_char {
        "U" => rope[0].1 += 1,
        "D" => rope[0].1 -= 1,
        "L" => rope[0].0 -= 1,
         _  => rope[0].0 += 1,
    }
}


fn tail_follow(rope: &mut RopeVec, idx: usize) {
    let delta_x = rope[idx].0-rope[idx+1].0;
    let delta_y =  rope[idx].1-rope[idx+1].1;
    let norm_delta_x = if delta_x != 0 {delta_x/delta_x.abs() } else {0};
    let norm_delta_y = if delta_y != 0 {delta_y/delta_y.abs()} else {0};
    if delta_x == 0 && delta_y.abs() > 1{
        rope[idx+1].1 += norm_delta_y; }
    else if delta_y == 0 && delta_x.abs() > 1{
        rope[idx+1].0 += norm_delta_x; }
    else if delta_x.abs() > 1 || delta_y.abs() > 1{
        rope[idx+1] = (rope[idx+1].0 + norm_delta_x, rope[idx+1].1 + norm_delta_y); }
}


fn update_rope(rope: &mut RopeVec) {
        for knot_idx in 0..rope.len()-1 {
        tail_follow(rope, knot_idx);
    }
}


fn simulate_rope(my_file_name: &str, num_knots: usize) -> usize {    
    let mut rope : RopeVec = Vec::new();
    for _i in 0..num_knots {
        rope.push((0,0));
    }
    let mut rope_tail_history : RopeSet = HashSet::new();
    if let Ok(lines) = read_lines(my_file_name) {
        for line in lines {
            if let Ok(ip) = line {
                let instructions : Vec<&str> = ip.split(' ').collect();
                let num_steps: u8 = instructions[1].parse::<u8>().unwrap();
                for _step in 0..num_steps {
                    head_instruction(&mut rope, instructions[0]);
                    update_rope(&mut rope);
                    rope_tail_history.insert(rope.last().unwrap().clone());         
                }
            }
        }
    }    
    return rope_tail_history.len();
}

