use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_ten.txt";
    let line_breaks = vec![0, 40, 80, 120, 160, 200];
    let sum_signal_strength = calc_signal_strength(file_name, &line_breaks);
    
    let duration = start.elapsed();
    println!("Part One: {}", sum_signal_strength);
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}

fn add_visible_char(row_str: &mut String, current_cycle: i32, register_val: i32 ) {
    let mut row_idx = current_cycle-1;
    while row_idx > 39 { row_idx -= 40;}
    let append_char : char = if (row_idx - register_val).abs() <= 1 {'#'} else {'.'};
    row_str.push(append_char);
}


fn calc_signal_strength(my_file_name: &str, line_breaks: &Vec<i32>) -> i32 {    
    let mut sig_strengths : Vec<i32> = Vec::new();
    let mut current_cycle : i32 = 1;
    let mut register_val : i32 = 1;
    let mut screen_row : String = String::from("");
    
    if let Ok(lines) = read_lines(my_file_name) {
        for line in lines {
            if let Ok(ip) = line {
                add_visible_char(&mut screen_row, current_cycle, register_val);
                
                if line_breaks.contains( &(current_cycle+20) ) {
                    sig_strengths.push(current_cycle * register_val);
                }
                let line_vec: Vec<&str> = ip.split(' ').collect();
                if line_vec[0].trim() == "noop" {
                    current_cycle += 1;
                    continue;
                }
                if line_breaks.contains( &(current_cycle+21) ) {
                    sig_strengths.push(current_cycle * register_val);
                }
                add_visible_char(&mut screen_row, current_cycle+1, register_val);
                current_cycle += 2;
                register_val += line_vec[1].parse::<i32>().unwrap();
            }
        }
    }
    let sum_sig_strength = sig_strengths.iter().sum();           
    for brk_idx in 0..line_breaks.len()-1 {
        let upper = line_breaks[brk_idx+1] as usize;
        let lower = line_breaks[brk_idx] as usize;
        println!("{}", &screen_row[lower..upper]);
    }
    println!("{}", &screen_row[*line_breaks.last().unwrap() as usize ..]);

    return sum_sig_strength;
}

