use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use std::collections::HashSet;
use itertools::Itertools;


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_fifteen.txt";
    let (part_one, part_two) = search_beacons(file_name);
    let duration = start.elapsed();    
    println!("Part One: {}  Part Two: {}", part_one, part_two);
    println!("Time taken to execute: {} seconds", duration.as_secs());    
}

type Pos = (i64,i64);

struct Sensor {
    own_pos: Pos,
    nrst_b: Pos,
    taxi: i64,
}


impl Sensor {
    pub fn set_taxicab_distance(&mut self) {
        let delta_x = self.nrst_b.0-self.own_pos.0;
        let delta_y = self.nrst_b.1-self.own_pos.1;
        self.taxi = delta_x.abs() + delta_y.abs();
    }

    pub fn in_range(&self, test_pos: Pos) -> bool {
        let delta_x = test_pos.0 - self.own_pos.0;
        let delta_y = test_pos.1 - self.own_pos.1;
        return (delta_x.abs() + delta_y.abs()) <= self.taxi;
    }

    pub fn annulus(&self) -> HashSet<Pos> {
        let mut result : HashSet<Pos> = HashSet::new();
        for dx in 0..=self.taxi+1 {
            let dy = self.taxi + 1 - dx;
            result.insert( (self.own_pos.0+dx, self.own_pos.1+dy));
            // Don't need to include these
            //result.insert( (self.own_pos.0-dx, self.own_pos.1+dy));
            //result.insert( (self.own_pos.0+dx, self.own_pos.1-dy));
            result.insert( (self.own_pos.0-dx, self.own_pos.1-dy));
        }
        return result;
    }

    pub fn get_conj_coord(&self, coord: i64, is_min: bool, is_y : bool) -> i64 {        
        let dist = if is_y {self.own_pos.1 - coord} else { self.own_pos.0 - coord};
        let conj_dist = if is_min {dist.abs() - self.taxi as i64} else {self.taxi as i64 - dist.abs()};
        let result = if is_y {self.own_pos.0 + conj_dist} else {self.own_pos.1 + conj_dist};
        return result;
    }
}


struct SensorList {
    sensors: Vec<Sensor>,
}

impl SensorList {
    pub fn prep_taxi(&mut self) {
        self.sensors.iter_mut().for_each(|s| s.set_taxicab_distance());
    }

    pub fn is_sensor_in_range(&self, test_pos: Pos) -> bool {
        return self.sensors.iter().any(|s| s.in_range(test_pos)) ;
    }

    pub fn is_beacon(&self, test_pos: Pos) -> bool {
        return self.sensors.iter().any(|s| s.nrst_b == test_pos) ;
    }

    pub fn annulus_set(&self) -> HashSet<Pos> {
        let mut result : HashSet<Pos> = HashSet::new();
        let annulus_vec: Vec<HashSet<Pos>> = self.sensors.iter().map(|s| s.annulus() ).collect();
        for (annul_one, annul_two) in annulus_vec.iter().tuple_combinations() {
            result.extend(annul_one.intersection(&annul_two));
        }
        return result;
    }

    pub fn check_row(&self, row_idx: i64, speed_mode:bool) -> usize{
        let min_x: i64 = self.sensors.iter().map(|s| s.get_conj_coord(row_idx, true, true)).min().unwrap();
        let max_x: i64 = self.sensors.iter().map(|s| s.get_conj_coord(row_idx, false, true)).max().unwrap();
        if speed_mode {
            return (max_x - min_x) as usize;
        }
        let mut in_range_counter: usize = 0;
        for x in min_x..=max_x {
            if self.is_sensor_in_range((x, row_idx)) && !self.is_beacon((x, row_idx)) {
                in_range_counter += 1;
            }
        }
        return in_range_counter;
    }

    pub fn search_space(&self, big: i64) -> Option<i64> {
        let (min_x, max_x) : Pos = (0, big);
        let (min_y, max_y) : Pos = (0, big);
        let annulus_set : HashSet<Pos> = self.annulus_set();
        for pos in annulus_set {
            if (min_x..=max_x).contains(&pos.0) && (min_y..=max_y).contains(&pos.1) {
                if !self.is_sensor_in_range(pos) {
                    return Some( pos.0*big + pos.1 );
                }
            }
        }
        return None;
    }
}


fn search_beacons(my_file_name: &str) -> (usize, i64) {
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();
    let line_vec: Vec<String> = buf_lines.map(|l| l.expect("Fail to parse")).collect();

    let mut sensor_list : SensorList = SensorList {sensors: Vec::new()};
    for line in line_vec {
        let split_line: Vec<&str> = line.trim().split(&[',','=',':']).collect();
        let sens_x: i64 = split_line[1].parse::<i64>().unwrap();
        let sens_y: i64 = split_line[3].parse::<i64>().unwrap();
        let b_x: i64 = split_line[split_line.len() - 3].parse::<i64>().unwrap();
        let b_y: i64 = split_line[split_line.len() - 1].parse::<i64>().unwrap();
        sensor_list.sensors.push( Sensor { own_pos:(sens_x, sens_y), nrst_b:(b_x, b_y), taxi:0});
    }

    sensor_list.prep_taxi();
    let row_idx: i64 = 2000000;
    let part_one = sensor_list.check_row(row_idx, true);
    let mut part_two : i64 = 0 ;
    let part_two_result = sensor_list.search_space(4000000);
    match part_two_result {
        Some(val) => part_two = val,
        None => println!("Couldn't find a solution!"),
    }    
    return (part_one,part_two)
}
