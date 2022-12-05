use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;




fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_five.txt";
    let reverse: bool = false;
    let tops = calculate_tops_stacks(file_name, reverse);
    //let tops = calculate_tops_strings(file_loc, reverse));
    
    let duration = start.elapsed();
    println!("Top items : {:?}", tops);    
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}


fn initialise_stacks(stack_initialiser_q: &Vec<String> ) -> Vec<Vec<String>> {
    let mut stack_vec : Vec<Vec<String>> = Vec::new();
    let max_stack_idx_str: &str = stack_initialiser_q.last().unwrap().trim().split(" ").last().unwrap();
    let max_stack_idx : usize = max_stack_idx_str.parse::<usize>().unwrap();    

    for _vec_idx in 0..max_stack_idx as usize {
        stack_vec.push(Vec::new());
    }

    for row in stack_initialiser_q.iter().rev().skip(1) {
        let this_row: Vec<&str> = row.split("] ")        
                                        .collect();
                   
        let mut skipped_entries : usize = 0;
        for (idx, item) in this_row.iter().enumerate(){            
            if item.trim().is_empty() {continue;}
            let pre_suff : Vec<&str> = item.split("[").collect();
            skipped_entries += pre_suff[0].len()/4;
            let stack_idx = idx + skipped_entries as usize;
            stack_vec[stack_idx].push(pre_suff[1].to_string().replace("]",""));            
        }
    }
    return stack_vec;
}



fn shift_crates(stack_vec: &mut Vec<Vec<String>>, origin_idx: usize, dest_idx:usize,
                 num_crates: usize, reverse:bool) {
    let mut transfer_vec : Vec<String> = Vec::new();
    for _i in 0..num_crates {
        transfer_vec.push(stack_vec[origin_idx].pop().unwrap());        
    }

    if reverse {
        for element in transfer_vec.into_iter().rev() {
            stack_vec[dest_idx].push(element);
        }
    }
    else {
        for element in transfer_vec {
            stack_vec[dest_idx].push(element);
        }
    }
    
}


fn get_tops(stack_vec: Vec<Vec<String>>) -> String {
    let mut result: String = String::new();
    for stack in stack_vec {
        result.push_str(stack.last().unwrap());
    }
    return result;
}



fn calculate_tops_stacks(my_file_name: &str, reverse:bool) -> String {
    let mut initialising_stacks: bool = true;
    let mut stack_initialiser_q: Vec<String> = Vec::new();
    let mut stack_vec: Vec<Vec<String>> = Vec::new();
    
    if let Ok(lines) = read_lines(my_file_name) {
        for line in lines {
            if let Ok(ip) = line {                
                if initialising_stacks {
                    //println!("{}", ip);
                    if ip.is_empty() {
                        initialising_stacks = false;
                        stack_vec = initialise_stacks(&stack_initialiser_q);
                    }
                    else {
                        stack_initialiser_q.push(ip.clone());
                    }
                }

                else {

                    let command_vec : Vec<&str> = ip.split(' ').collect();
                    if command_vec[0] == "move" {
                        shift_crates(&mut stack_vec, command_vec[3].parse::<usize>().unwrap()-1,
                                    command_vec[5].parse::<usize>().unwrap()-1,
                                    command_vec[1].parse::<usize>().unwrap(),
                                    reverse);
                    }
                    //println!("COMMAND {:?}", command_vec);

                }             
            }
        }
    }

    //let tops : Vec<&str> = Vec::new();
    //return tops;

    /*
    println!("-------------------------------------");
    for element in &stack_vec {
        println!("{:?}", element.last());

    }
    println!("-------------------------------------");
    */ 

    //println!("{:?}", stack_vec);

    //return stack_initialiser_q;
    return get_tops(stack_vec);
}
