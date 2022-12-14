use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use std::collections::HashSet;


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_fourteen.txt";
    let (part_one, part_two) = simulate_sand(file_name);
    let duration = start.elapsed();    
    println!("Part One: {}  Part Two: {}", part_one, part_two);
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn simulate_sand(my_file_name: &str) -> (usize, usize) {
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();
    let line_vec: Vec<String> = buf_lines.map(|l| l.expect("Fail to parse")).collect();

    let (mut blocked, bottom_depth) = line_vec.iter().map(|l| l.split(" -> ")
                        .flat_map(|coords| coords.split_once(',')
                        .and_then(|(x,y)| Some((
                            x.parse::<usize>().ok()?,
                            y.parse::<usize>().ok()?,
                        ))))
                        .collect::<Vec<_>>())
                        .fold((HashSet::new(), 0), |(rock,butt) , p | p.windows(2)
                        .flat_map(|wind| TryInto::<[_; 2]>::try_into(wind).ok())
                        .fold( (rock,butt) , |(mut rocks, mut bottom_depth), [(a,b),(c,d)]| {
                            for y in b.min(d)..=b.max(d) {
                                for x in a.min(c)..=a.max(c) {
                                    rocks.extend(std::iter::once((x,y)))
                                }
                                bottom_depth = bottom_depth.max(y)
                            }
                            (rocks, bottom_depth)
                        }));
    
    let sand_start_pos: (usize, usize) = (500, 0);    
    let mut counter : usize = 0;
    let mut touch_floor: bool = false;
    let mut part_one: usize = 0;    

    while !blocked.contains(&sand_start_pos) && counter <= 50000 {
        let mut sand_pos = sand_start_pos;
        counter += 1;
        loop {            
            let mut at_rest : bool = true;
            if sand_pos.1 >= bottom_depth+1 {
                if !touch_floor { 
                    part_one = counter;
                    touch_floor = true; 
                    }
                blocked.insert(sand_pos);
                break;
            }            
            let below = (sand_pos.0, sand_pos.1+1);
            let dwnlft = (sand_pos.0 - 1, sand_pos.1+1);
            let dwnrght = (sand_pos.0 + 1, sand_pos.1+1);

            for dir in vec![below, dwnlft, dwnrght] {
                if !blocked.contains(&dir) {
                    sand_pos = dir;
                    at_rest=false;
                    break;
                }
            }
            if at_rest {
                blocked.insert(sand_pos);
                break ;
            }        
        }
    }
    let part_two = counter;
    
    return (part_one,part_two)
}
