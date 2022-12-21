use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use std::collections::HashMap;


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_twentyone.txt";
    //let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\example.txt";
    let (part_one, part_two) = understand_monkeys(file_name);
    let duration = start.elapsed();    
    println!("Part One: {}  Part Two: {}", part_one, part_two);
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn build_monkey_dict(monkey_list: &Vec<Vec<String>>, part_two: bool, humn_guess: f64) -> HashMap<String, f64> {
    let mut monkey_dict: HashMap<String, f64> = HashMap::new();    
    for monkey in monkey_list {
        if part_two && monkey[0] == "humn".to_string() {
            monkey_dict.insert(monkey[0].clone(), humn_guess);
        }
        else if monkey.len() == 3 {
            monkey_dict.insert(monkey[0].clone(), monkey[2].parse::<f64>().unwrap());
        }
    }

    let mut info_updated: bool = true;
    while info_updated {
        info_updated = false;
        for monkey in monkey_list {
            if monkey_dict.contains_key(&monkey[0]) {
                continue;
            }

            if monkey_dict.contains_key(&monkey[2]) && monkey_dict.contains_key(&monkey[4]) {
                if part_two && monkey[0] == "root".to_string() {
                    monkey_dict.insert(monkey[0].clone(), monkey_dict[&monkey[2]] - monkey_dict[&monkey[4]]);
                }
                else if monkey[3] == "*" {
                    monkey_dict.insert(monkey[0].clone(), monkey_dict[&monkey[2]] * monkey_dict[&monkey[4]]);
                }
                else if monkey[3] == "/" {
                    monkey_dict.insert(monkey[0].clone(), monkey_dict[&monkey[2]] / monkey_dict[&monkey[4]]);
                }
                else if monkey[3] == "-" {
                    monkey_dict.insert(monkey[0].clone(), monkey_dict[&monkey[2]] - monkey_dict[&monkey[4]]);
                }
                else if monkey[3] == "+" {
                    monkey_dict.insert(monkey[0].clone(), monkey_dict[&monkey[2]] + monkey_dict[&monkey[4]]);
                }
                else { unreachable!(); }
                info_updated = true;
            }
        }
    }
    return monkey_dict;
}


fn test_val(input: &Vec<Vec<String>>, test_val: f64) -> f64 {
    let monkey_dict = build_monkey_dict(input, true, test_val);
    return *monkey_dict.get(&"root".to_string()).unwrap();
}

fn same_sign(val1: f64, val2: f64) -> bool {
    return val1*val2 > 0.0;
}

fn find_humn_val(input: &Vec<Vec<String>>, mut low_guess: f64, mut high_guess: f64) -> f64 {
    let mut low_val = test_val(input, low_guess);
    let mut high_val = test_val(input, high_guess);
    let mut med_guess = (high_guess + low_guess) / 2.0;
    let mut med_val = test_val(input, med_guess);

    while med_val.abs() > 1e-6  {
        if same_sign(low_val, med_val) {       low_guess  = med_guess;   }
        else if same_sign(high_val, med_val) { high_guess = med_guess;  }
        med_guess = (high_guess + low_guess) / 2.0;
        low_val = test_val(input, low_guess);
        high_val = test_val(input, high_guess);
        med_val = test_val(input, med_guess);
    }
    return med_guess;
}


fn understand_monkeys(my_file_name: &str) -> (f64, f64) {
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();
    let line_vec: Vec<String> = buf_lines.map(|l| l.expect("Fail to parse")).collect();   
    let input : Vec<Vec<String>> = line_vec.iter().map(|s| 
        s.trim().split(&[':',' '][..]).map( |substr| 
            substr.to_string() )
            .collect())
            .collect();   
    
    let part_one_dict = build_monkey_dict(&input, false, 0.0);
    let part_one = part_one_dict.get(&"root".to_string()).unwrap().clone();
       
    let part_two = find_humn_val(&input, 0.0, 10000000000000.0);
        
    return (part_one, part_two);
}
