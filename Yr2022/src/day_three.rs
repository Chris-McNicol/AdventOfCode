use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;

use std::collections::HashSet;



fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_three.txt";
    let (tot_priority, tot_group_priority) = sum_priorities(file_name);
    //let other_fast = other_faster_way_maybe();
    let duration = start.elapsed();
    println!("Total Priority : {}, Total Group Priority : {}", tot_priority, tot_group_priority);    
    //println!("Other faster way {}", other_fast);
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}


fn get_common_item(rucksack: String) -> char {
    let set_one: HashSet<char> = rucksack[0..rucksack.len()/2].chars().collect() ;
    let set_two: HashSet<char> = rucksack[rucksack.len()/2..rucksack.len()].chars().collect() ;    
    let inter: HashSet<char> = set_one.intersection(&set_two).copied().collect();
    let elem =  inter.iter().next().unwrap().clone();
    return elem; 
}

fn get_common_badge(group_vec: &Vec<String>) -> char {
    let set_one: HashSet<char> = group_vec[0].chars().collect();
    let set_two: HashSet<char> = group_vec[1].chars().collect();
    let set_three: HashSet<char> = group_vec[2].chars().collect();
    let first_inter: HashSet<char> = set_one.intersection(&set_two).copied().collect();
    let second_inter: HashSet<char> = first_inter.intersection(&set_three).copied().collect();
    let elem =  second_inter.iter().next().unwrap().clone();
    return elem; 
}

fn get_priority(input_char : u32) -> u32 {
    match input_char {
        97..=122 => return input_char - 96,
        _ => return input_char - 38,
    }
}


fn sum_priorities(my_file_name: &str) -> (u32, u32) {
    let mut total_priority: u32 = 0;
    let mut total_group_priority: u32 = 0;
    let mut group_vec: Vec<String> = Vec::new();
    if let Ok(lines) = read_lines(my_file_name) {
        for line in lines {
            if let Ok(ip) = line {
                let other_line = ip.clone();
                total_priority += get_priority(get_common_item(ip) as u32);
                group_vec.push(other_line);
                if group_vec.len() == 3 {
                    total_group_priority += get_priority(get_common_badge(&group_vec) as u32);
                    group_vec.clear();
                }               
            }
        }
    }
    return (total_priority, total_group_priority)
}


fn other_faster_way_maybe() -> u32 {
    
    let faster_part_one : u32 = include_str!("C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_three.txt")
        .split("\n")
        .filter(|x| !x.is_empty())
        .map(|rucksack| {
            let set_one: HashSet<char> = rucksack[0..rucksack.len()/2].chars().collect() ;
            let set_two: HashSet<char> = rucksack[rucksack.len()/2..rucksack.len()].chars().collect() ;    
            let inter: HashSet<char> = set_one.intersection(&set_two).copied().collect();
            let elem = inter.iter().next().unwrap().clone() as u32;
            match elem {
                97..=122 => return elem - 96,
                _ => return elem - 38,
            }
        })
        .sum();

    return faster_part_one;
}