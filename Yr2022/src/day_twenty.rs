use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_twenty.txt";
    //let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\example.txt";
    let (part_one, part_two) = apply_shifts(file_name);
    println!("Part One: {}  Part Two:  {}", part_one, part_two);
    let duration = start.elapsed();    
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}



fn shift_em(orig_vec: &Vec<i64>, num_shifts: usize, decrypt_key: i64) -> i64 {
    let mut pair_vec: Vec< (usize, i64) > = Vec::new();

    for (idx, val) in orig_vec.iter().enumerate() {
        pair_vec.push( (idx, val*decrypt_key));
    }   
    for _rep in 0..num_shifts {
        for pair_idx in 0..pair_vec.len() {
            let start_idx = pair_vec.iter().position(|&p| p.0 == pair_idx).unwrap();
            let pair = pair_vec[start_idx].clone();
            pair_vec.remove(start_idx);
            let new_idx = (start_idx as i64 + pair.1).rem_euclid(pair_vec.len() as i64) as usize;
            pair_vec.insert(new_idx, pair);
        }
    }

    let zero_pos = pair_vec.iter().position(|p| p.1 == 0).unwrap();    
    let check_pos: Vec<usize> = vec![1000, 2000, 3000];
    return check_pos.iter().map(|pos| {
        let new_pos_index = (zero_pos + pos).rem_euclid(pair_vec.len());
        pair_vec[new_pos_index].1
    } ).sum();
}


fn apply_shifts(my_file_name: &str) -> (i64, i64){        
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();
    let line_vec: Vec<String> = buf_lines.map(|l| l.expect("Fail to parse")).collect();
    let orig_vec: Vec<i64> = line_vec.iter().map(|l| l.trim().parse::<i64>().unwrap() ).collect();

    let part_one = shift_em(&orig_vec, 1, 1);
    let part_two = shift_em(&orig_vec, 10, 811589153);
    
    return (part_one, part_two);
}


