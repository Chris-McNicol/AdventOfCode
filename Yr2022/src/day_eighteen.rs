use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use std::collections::{HashSet, VecDeque};


type Pos = (i8,i8,i8);

struct BoundBox {
    xlim: (i8, i8),
    ylim: (i8, i8),
    zlim: (i8, i8),
}

impl BoundBox {
    fn update_x(&mut self, x_val: i8) {
        self.xlim.0 = std::cmp::min(self.xlim.0, x_val-10);
        self.xlim.1 = std::cmp::max(self.xlim.1, x_val+10);}
    fn update_y(&mut self, y_val: i8) {
        self.ylim.0 = std::cmp::min(self.ylim.0, y_val-10);
        self.ylim.1 = std::cmp::max(self.ylim.1, y_val+10);}
    fn update_z(&mut self, z_val: i8) {
        self.zlim.0 = std::cmp::min(self.zlim.0, z_val-10);
        self.zlim.1 = std::cmp::max(self.zlim.1, z_val+10);}

    fn out_of_bounds(&self, pos: &Pos) -> bool {
        let out_x = pos.0 > self.xlim.1 || pos.0 < self.xlim.0;
        let out_y = pos.1 > self.ylim.1 || pos.1 < self.ylim.0;
        let out_z = pos.2 > self.zlim.1 || pos.2 < self.zlim.0;
        return out_x || out_y || out_z;
    }
}


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_eighteen.txt";
    //let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\example.txt";
    let (part_one, part_two) = find_obsidian(file_name);
    let duration = start.elapsed();    
    println!("Part One: {}  Part Two: {}", part_one, part_two);
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn in_contact(pos_one: &Pos, pos_two: &Pos) -> bool {
    let delta_x = pos_one.0 as i8 - pos_two.0 as i8;
    let delta_y = pos_one.1 as i8 - pos_two.1 as i8;
    let delta_z = pos_one.2 as i8 - pos_two.2 as i8;
    return delta_x.abs() + delta_y.abs() + delta_z.abs() == 1;
}


fn calc_surface_area(input_cube_set : &HashSet<Pos>) -> usize {
    let mut search_cube_vec: Vec<Pos> = input_cube_set.iter().cloned().collect();
    let mut overlaps: usize = 0;
    for _i in 0..search_cube_vec.len() {
        let check_pos = search_cube_vec.pop().expect("Should be an element");
        overlaps += input_cube_set.iter().filter(|&p| in_contact(p, &check_pos)).count();
    }
    let total_cube_area = 6*input_cube_set.len();
    let surface_area = total_cube_area - (overlaps);
    return surface_area;
}


fn get_adjacent(pos: Pos) -> Vec<Pos> {
    let mut result : Vec<Pos> = Vec::new();
    result.push( (pos.0+1, pos.1, pos.2 ));
    result.push( (pos.0-1, pos.1, pos.2 ));
    result.push( (pos.0, pos.1+1, pos.2 ));
    result.push( (pos.0, pos.1-1, pos.2 ));
    result.push( (pos.0, pos.1, pos.2 +1));
    result.push( (pos.0, pos.1, pos.2 -1 ));
    return result;
}


fn calc_outer_area(input_cube_set: &HashSet<Pos>, bounds: &BoundBox) -> usize {
    let start_pos: Pos = (bounds.xlim.0,bounds.ylim.0,bounds.zlim.0);
    let mut filled_set : HashSet<Pos> = HashSet::new();
    let mut queue = VecDeque::new();
    queue.push_back(start_pos);
    while let Some(pos) = queue.pop_front() {
        if !filled_set.contains(&pos) {
            filled_set.insert(pos);
            for adj in get_adjacent(pos) {
                if !bounds.out_of_bounds(&adj) && !input_cube_set.contains(&adj) && !filled_set.contains(&adj) {
                    queue.push_back(adj);
                }
            }
        }
    }
    
    let mut search_cube_vec: Vec<Pos> = input_cube_set.iter().cloned().collect();
    let mut outer_area: usize = 0;
    for _i in 0..search_cube_vec.len() {
        let check_pos = search_cube_vec.pop().expect("Should be an element");
        for adj in get_adjacent(check_pos) {
            if filled_set.contains(&adj) || bounds.out_of_bounds(&adj) {outer_area += 1;}
        }
    }
    return outer_area;
}


fn find_obsidian(my_file_name: &str) -> (usize, usize) {
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();
    let line_vec: Vec<String> = buf_lines.map(|l| l.expect("Fail to parse")).collect();   
    let mut cube_set : HashSet<Pos> = HashSet::new();
    let mut bounds : BoundBox = BoundBox{xlim:(i8::MAX,0),ylim:(i8::MAX,0),zlim:(i8::MAX,0)};

    for line in line_vec {
        let ele_vec: Vec<i8> = line.trim().split(',').map(|s| s.parse::<i8>().unwrap()).collect();
        bounds.update_x(ele_vec[0]);
        bounds.update_y(ele_vec[1]);
        bounds.update_z(ele_vec[2]);
        cube_set.insert( (ele_vec[0], ele_vec[1], ele_vec[2]));
    }

    let part_one = calc_surface_area(&cube_set);
    let part_two = calc_outer_area(&cube_set, &bounds);

    return (part_one, part_two);
}


