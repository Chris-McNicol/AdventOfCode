use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;

use std::cmp;



fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_four.txt";
    let (num_overlaps, num_contained) = check_overlaps(file_name);
    let duration = start.elapsed();
    println!("Number Overlaps : {}, Number contained : {}", num_overlaps, num_contained);    
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}


fn check_overlaps(my_file_name: &str) -> (i32, i32) {
    let mut num_overlaps: i32 = 0;
    let mut num_contained: i32 = 0;
    if let Ok(lines) = read_lines(my_file_name) {
        for line in lines {
            if let Ok(ip) = line {                
                let p : Vec<i32> = ip.split(&[',', '-'][..])
                                    .map(|x| x.parse::<i32>().unwrap())
                                    .collect();

                let (elf_one_lo, elf_one_hi, elf_two_lo, elf_two_hi) = (p[0],p[1],p[2],p[3]);
                let overlap_len = cmp::min(elf_one_hi, elf_two_hi) - cmp::max(elf_one_lo,elf_two_lo);               

                if overlap_len >= 0 {
                    num_overlaps += 1;
                    if (overlap_len == elf_one_hi-elf_one_lo) || (overlap_len== elf_two_hi-elf_two_lo){
                        num_contained += 1;
                    }
                }
            }
        }
    }
    return (num_overlaps, num_contained)
}
