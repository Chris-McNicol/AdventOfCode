use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_ten.txt";
    let line_breaks = (1..7).map(|x| x*40).collect();
    let register_vec = get_register(file_name);
    let sum_signal_strength = calc_signal_strength(&register_vec, &line_breaks);
    let duration = start.elapsed();
    println!("Part One: {}         Part Two:", sum_signal_strength);
    print_screen(&register_vec, &line_breaks);
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}


fn calc_signal_strength(register_vec : &Vec<i32>, line_breaks: &Vec<i32>) -> i32 {
    return line_breaks.iter().map(|&x| register_vec[x as usize -21]* (x-20)).sum();
}


fn print_screen(register_vec: &Vec<i32>, line_breaks: &Vec<i32>) {
    let mut output_str = String::from("");
    for (idx, register) in register_vec.iter().enumerate() {
        if line_breaks.contains(&(idx as i32)) {
            output_str.push('\n');
        }
        output_str += if ((idx as i32)%40 - register).abs() <=1 {"X"} else {" "};
    }
    println!("{}", output_str);
}


fn get_register(my_file_name: &str) -> Vec<i32> {    
    let mut register_val : i32 = 1;
    let mut register_vec : Vec<i32> = Vec::new();
    
    if let Ok(lines) = read_lines(my_file_name) {
        for line in lines {
            if let Ok(ip) = line {
                if ip.trim() == "noop" {
                    register_vec.push(register_val);
                }
                else {
                    register_vec.push(register_val);
                    register_vec.push(register_val);
                    register_val += ip.trim().split(' ').last().expect("Reason").parse::<i32>().unwrap();
                }
            }
        }
    }
    return register_vec;
}

