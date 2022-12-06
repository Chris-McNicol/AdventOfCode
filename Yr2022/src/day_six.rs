use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;




fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_six.txt";
    let (packet_indx, msg_indx) = find_indxs(file_name); 
    let duration = start.elapsed();
    println!("Packet start: {}    Message start: {}", packet_indx, msg_indx);    
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}



fn unique(s: &str) -> Option<(usize,char)> {
      s.chars().enumerate().find_map(|(i, c)| {
        s.chars()
            .enumerate()
            .skip(i + 1)
            .find(|(_, other)| c == *other)
    })
}

fn is_slice_unique(s: &str, char_idx: usize, length: usize) -> bool {
    let result = unique(&s[char_idx..char_idx+length]);
    match result {
        Some((_,_)) => return false,
        _ => return true,
    }
}

fn find_indxs(my_file_name: &str) -> (usize, usize) {
    let mut packet_idx = 0;
    let mut msg_idx = 0;
   
    if let Ok(lines) = read_lines(my_file_name) {
        for line in lines {
            if let Ok(ip) = line {
                let test_line = ip.clone();           
                for (char_idx, _) in ip.chars().enumerate() {
                    if is_slice_unique(&test_line, char_idx, 4) && packet_idx == 0 {
                        packet_idx = char_idx + 4;
                    }
                    if is_slice_unique(&test_line, char_idx, 14) && msg_idx == 0 {
                        msg_idx = char_idx + 14;
                        break;
                    }
                }
            }
        }
    }
    return (packet_idx, msg_idx);
}
