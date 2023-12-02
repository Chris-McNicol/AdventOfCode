use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use std::collections::{HashSet, HashMap};

type Pos = (i32,i32);



fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_twentythree.txt";
    //let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\example.txt";
    let (part_one, part_two) = path_find(file_name);
    println!("Part One: {}  Part Two:  {}", part_one, part_two);
    let duration = start.elapsed();    
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}

struct AdjDir {
    bits: u8,
    dx: i32,
    dy: i32,
}

struct Arena {
    occupied: HashSet<Pos>,
    adjs: Vec<AdjDir>,
}

impl Arena {
    fn get_adjacents(&self, pos: Pos) -> u8 {
        let mut bits: u8 = 0;
        for (idx, (dx,dy)) in vec![(1,1), (0,1), (-1,1), (1,0), (-1,0), (1,-1), (0,-1), (-1,-1)].iter().enumerate() {
            if self.occupied.contains(&(pos.0 + dx, pos.1 + dy)) {
                bits = bits | (1<<idx);
            }
        }
        return bits;
    }

    fn proposals(&self, pos: Pos, turn_idx: usize) -> Option<Pos> {
        let adj = self.get_adjacents(pos);
        if adj == 0 { return None; }
        for i in 0..4 {
            let adj_dir = &self.adjs[ (turn_idx+i)% self.adjs.len() ];
            if adj_dir.bits & adj == 0 { return Some((pos.0+adj_dir.dx, pos.1+adj_dir.dy));}
        }
        return None;
    }

    fn calc_move(&mut self, turn_idx: usize) -> bool {
        let mut move_dict : HashMap<Pos, Option<Pos>> = HashMap::new();
        let mut next_occupied : HashSet<Pos> = HashSet::new();
        let mut has_updated: bool = false;
        for current in &self.occupied {
            move_dict.insert(*current, self.proposals(*current, turn_idx));
        }

        for (current, next) in move_dict.iter() {
            if next.is_none() {next_occupied.insert(*current);}
            else {
                let next_count = move_dict.values().filter(|v| 
                    match v {
                        Some(entry) => *entry == next.unwrap(),
                        _ => false,
                    }
                ).count();           
                
                if next_count > 1 {
                    next_occupied.insert(*current);
                }
                else {
                    next_occupied.insert(next.unwrap());
                    has_updated = true;
                }
            }
        }
        
        self.occupied = next_occupied;
        return has_updated;
    }

    fn get_empty(&self) -> i32 {
        let min_x = self.occupied.iter().map(|p| p.0).min().unwrap();
        let max_x = self.occupied.iter().map(|p| p.0).max().unwrap()+1;
        let min_y = self.occupied.iter().map(|p| p.1).min().unwrap();
        let max_y = self.occupied.iter().map(|p| p.1).max().unwrap()+1;
        return (max_y-min_y)*(max_x-min_x) - self.occupied.len() as i32;
    }

    fn print_arena(&self) {
        let min_x = self.occupied.iter().map(|p| p.0).min().unwrap();
        let max_x = self.occupied.iter().map(|p| p.0).max().unwrap();
        let min_y = self.occupied.iter().map(|p| p.1).min().unwrap();
        let max_y = self.occupied.iter().map(|p| p.1).max().unwrap();
        let mut out_str = String::new();
        for y in min_y..=max_y{
            for x in min_x..=max_x {
                if self.occupied.contains(&(x,y)) {
                    out_str.push('#');
                }
                else {
                    out_str.push('.');
                }
            }
            out_str.push('\n');
        }
        println!("{}", out_str);
    }
}



fn path_find(my_file_name: &str) -> (i32, usize){        
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();
    let line_vec: Vec<String> = buf_lines.map(|l| l.expect("Fail to parse")).collect();

    let mut occupied : HashSet<Pos> = HashSet::new();
    for (line_idx, line) in line_vec.iter().enumerate() {
        for char_idx in 0..line.len() {
            if line.chars().nth(char_idx) == Some('#') {
                occupied.insert( (char_idx as i32, line_idx as i32) );
            }
        }
    }
    let up_bits = 0b11100000;
    let down_bits = 0b00000111;
    let left_bits = 0b10010100;
    let right_bits = 0b00101001;
    let adjs = vec![AdjDir{bits:up_bits, dx:0, dy:-1},
                AdjDir{bits:down_bits, dx:0, dy:1},
                AdjDir{bits:left_bits, dx:-1, dy:0},
                AdjDir{bits:right_bits, dx:1, dy:0}];
    let mut arena = Arena{occupied:occupied, adjs:adjs };

    let mut has_updated: bool = true;
    let mut turn_idx: usize = 0;
    let mut part_one = 0;

    if false {
        arena.print_arena();
    }

    while has_updated {
        if turn_idx == 10 {part_one = arena.get_empty();}       
        has_updated = arena.calc_move(turn_idx);
        turn_idx += 1;
    }
    let part_two = turn_idx;  
    
    
    return (part_one, part_two);
}


