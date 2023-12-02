use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use std::collections::HashMap;


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_twentyfive.txt";
    let part_one = snafu_it(file_name);
    println!("Part One: {}", part_one);
    let duration = start.elapsed();    
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn snafu_to_decimal(snafu_str: &String, snaf_map: &HashMap<char,i64>) -> i64 {
    let mut result : i64 = 0;
    for (char_idx, ch) in snafu_str.chars().rev().enumerate() {
        result += snaf_map[&ch] * (5_i64.pow(char_idx as u32));
    }
    return result;
}


fn decimal_to_snafu(dec: i64, snaf_rem_map: &HashMap<i64, char>) -> String {
    let mut result: String = "".to_string();
    let mut n : i64 = dec;
    while n != 0 {
        let remainder = n % 5;
        result.push(snaf_rem_map[&remainder]);
        n = (n+2)/5;
    }
    return result.chars().rev().collect();
}


fn snafu_it(my_file_name: &str) -> String {    
    let snafu_map : HashMap<char, i64> = HashMap::from([('=',-2), ('-',-1), ('0',0), ('1',1), ('2',2)]);
    let snafu_remainder_map : HashMap<i64, char> = HashMap::from([(3,'='), (4,'-'), (0,'0'), (1,'1'), (2,'2')]);
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();
    let line_vec: Vec<String> = buf_lines.map(|l| l.expect("Fail to parse")).collect();
    let sum : i64 = line_vec.iter().map(|s| snafu_to_decimal(s, &snafu_map)).sum();
    return decimal_to_snafu(sum, &snafu_remainder_map);
}

