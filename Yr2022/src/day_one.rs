use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;
use std::env;


fn main() {
    let args: Vec<String> = env::args().collect();
    let mut num_max_vals: usize = 1;
    if args.len() == 2 {
        num_max_vals = args[1].parse::<usize>().unwrap();
    }
    
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_one.txt";
    let max_val = max_elves_calories(file_name, num_max_vals);
    let duration = start.elapsed();
    println!("Maximum elf calories: {}", max_val);    
    println!("Time taken to execute: {} microseconds", duration.as_micros());   
}


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}


fn max_elves_calories(my_file_name: &str, num_max_vals: usize) -> i32 {
    let mut elves_calories_vec = sum_elves_calories(my_file_name);
    elves_calories_vec.sort();
    if num_max_vals < 1 || num_max_vals > elves_calories_vec.len() {
        panic!("Requested {} number of maximums but should be between 1 and the number of elves.", num_max_vals);
    }
    let lower_index : usize = elves_calories_vec.len()-num_max_vals;

    let maxi: i32 = elves_calories_vec[lower_index..].iter().sum();
    return maxi;
}


fn sum_elves_calories(my_file_name: &str) -> Vec<i32> {
    let mut elves_calories_vec =  Vec::new();
    let mut current_calorie_count: i32 = 0;
    if let Ok(lines) = read_lines(my_file_name) {
        for line in lines {
            if let Ok(ip) = line {
                if ip == "" {
                    elves_calories_vec.push(current_calorie_count);
                    current_calorie_count = 0;
                }
                else {
                    current_calorie_count += ip.parse::<i32>().unwrap();
                }                
            }
        }
    }
    return elves_calories_vec;
}
