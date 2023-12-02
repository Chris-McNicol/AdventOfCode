use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use std::collections::{HashSet, HashMap};

use itertools::Itertools;
use std::cmp;


type Pos = (i32,i32);




fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_twentytwo.txt";    //let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\example.txt";
    let (part_one, part_two) = path_find(file_name);
    println!("Part One: {}  Part Two:  {}", part_one, part_two);
    let duration = start.elapsed();    
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}

fn direction(dir_idx : i32) -> (i32, i32) {
    match dir_idx {
        0 => (1,0),
        1 => (0,1),
        2 => (-1,0),
        3 => (0,-1),
        _ => (0,0),
    }
}

#[derive(Eq, PartialEq, Clone, Copy)]
enum Side {
    RIGHT = 0,
    DOWN = 1,
    LEFT = 2,
    UP = 3,
}

struct CubeFace {
    name: String,
    xlims: (i32, i32),
    ylims: (i32, i32),
    right_target: (String, Side, bool),
    down_target: (String, Side, bool),
    left_target: (String, Side, bool),
    up_target: (String, Side, bool),
    right_map: HashMap<Pos, Pos>,
    down_map: HashMap<Pos, Pos>,
    left_map: HashMap<Pos, Pos>,
    up_map: HashMap<Pos, Pos>,
}

impl CubeFace {
    fn right_edge(&self) -> Vec<Pos> {
        let mut result : Vec<Pos> = Vec::new();
        for y in self.ylims.0..=self.ylims.1 { result.push( (self.xlims.1, y)); }
        return result;
    }
    fn left_edge(&self) -> Vec<Pos> {
        let mut result : Vec<Pos> = Vec::new();
        for y in self.ylims.0..=self.ylims.1 { result.push( (self.xlims.0, y)); }
        return result;
    }
    fn up_edge(&self) -> Vec<Pos> {
        let mut result : Vec<Pos> = Vec::new();
        for x in self.xlims.0..=self.xlims.1 { result.push( (x, self.ylims.0)); }
        return result;
    }
    fn down_edge(&self) -> Vec<Pos> {
        let mut result : Vec<Pos> = Vec::new();
        for x in self.xlims.0..=self.xlims.1 { result.push( (x, self.ylims.1)); }
        return result;
    }
    fn get_edge(&self, side: Side) -> Vec<Pos> {
        match side {
            Side::RIGHT => return self.right_edge(),
            Side::LEFT => return self.left_edge(),
            Side::UP => return self.up_edge(),
            Side::DOWN => return self.down_edge(),
        }
    }
    fn is_on_face(&self, pos: Pos) -> (bool, Side) {
        if pos.1 > self.ylims.1 {return (false, Side::DOWN);}
        if pos.1 < self.ylims.0 {return (false, Side::UP);}
        if pos.0 > self.xlims.1 {return (false, Side::RIGHT);}
        if pos.0 < self.xlims.0 {return (false, Side::LEFT);}
        return (true, Side::UP);
    }

    //fn make_map(&mut self, edge: Vec<Pos>, target: (String, Side, bool)) -> HashMap<Pos,Pos> {
    fn make_map(&mut self, side: Side) ->HashMap<Pos,Pos> {
        let (mut edge, mut rev) = (self.right_edge(), self.right_target.2);
        match side {
            Side::LEFT => {edge = self.left_edge(); rev=self.left_target.2;},
            Side::UP => {edge = self.up_edge(); rev=self.up_target.2;},
            Side::DOWN => {edge = self.down_edge(); rev=self.down_target.2;},
            _ => {},
        }
        let mut map : HashMap<Pos, Pos> = HashMap::new();
        //let edge = self.faces[&target.0].get_edge(target.1);
        //let edge_iter = if target.2 {edge.iter().rev()} else {edge.iter()};
        //if target.2 {
        if rev {
            for (idx, v) in edge.iter().rev().enumerate() {
                map.insert( edge[idx], *v );
            } 
        }
        else {
            for (idx, v) in edge.iter().enumerate() {
                map.insert( edge[idx], *v );
            }
        }
        return map;
    }
    /*
    fn make_right_map(&mut self) {
        self.right_map = self.make_map(self.right_edge(), self.right_target);
    }
    fn make_up_map(&mut self) {
        self.up_map = self.make_map(self.up_edge(), self.up_target);
    }
    fn make_down_map(&mut self) {
        self.down_map = self.make_map(self.down_edge(), self.down_target);
    }
    fn make_left_map(&mut self) {
        self.left_map = self.make_map(self.left_edge(), self.left_target);
    }
    */
}



struct Cube {
    faces: HashMap<String, CubeFace>,
}

impl Cube {


    fn build_mappings(&mut self) {
        for (_face_key, face) in self.faces.iter_mut() {
            //face.right_map = self.make_map(face.right_edge(), face.right_target.clone());
            //face.down_map = self.make_map(face.down_edge(), face.down_target.clone());
            //face.left_map = self.make_map(face.left_edge(), face.left_target.clone());
            //face.up_map = self.make_map(face.up_edge(), face.up_target.clone());
            //face.make_right_map();
            //face.make_up_map();
            //face.make_left_map();
            //face.make_down_map();
            let side_vec = vec![Side::RIGHT, Side::DOWN, Side::LEFT, Side::UP];
            for side in side_vec {
                face.make_map(side);
            }
        }
    }

    fn get_map(&self, face_name: &String, off_dir: Side) -> (HashMap<Pos, Pos>, Side) {
        let face = &self.faces[face_name];
        match off_dir {
            Side::RIGHT => (face.right_map.clone(), face.right_target.1),
            Side::DOWN => (face.down_map.clone(), face.down_target.1),
            Side::LEFT => (face.left_map.clone(), face.left_target.1),
            Side::UP => (face.up_map.clone(), face.up_target.1),
        }
    }

    fn get_face(&self, pos: Pos) -> String {
        for (face_name, face) in &self.faces {
            if face.is_on_face(pos).0 {
                return face_name.to_string();
            }
        }
        unreachable!();
    }

    fn get_dir_shift(&self, off_dir: Side, on_dir: Side) -> i32 {
        if off_dir as i32 == on_dir as i32 { return 2; }
        if (off_dir as i32 - on_dir as i32).abs() == 2 { return 0; }
        if (on_dir as i32 - off_dir as i32) == 1 || (on_dir as i32 - off_dir as i32) == -3 { return 3;}
        else {return 1;}
    }
}


struct Turtle {
    crse_idx: i32,
    pos : Pos,
    free: HashSet<Pos>,
    blocked: HashSet<Pos>,
    xlims: Vec<Pos>,
    ylims: Vec<Pos>,
    is_cube: bool,
    cube: Cube,
    current_face: String,
}


impl Turtle {
    fn turn_right(&mut self) { self.crse_idx = if self.crse_idx ==3 {0} else{self.crse_idx + 1};}
    fn turn_left(&mut self) { self.crse_idx = if self.crse_idx == 0 {3} else {self.crse_idx -1};}

    fn wrap_lims_linear(&mut self, val: i32, x_mode:bool) -> i32 {
        let lims: (i32, i32) = if x_mode {self.xlims[self.pos.1 as usize]} else {self.ylims[self.pos.0 as usize]};
        if val < lims.0 {return lims.1}
        if val > lims.1 {return lims.0}
        return val; 
    }

    fn next_pos(&mut self) {
        let dir = direction(self.crse_idx);
        let wrap_new_x = self.wrap_lims_linear(self.pos.0 + dir.0, true);
        let wrap_new_y = self.wrap_lims_linear(self.pos.1 + dir.1, false);
        if !self.blocked.contains(&(wrap_new_x, wrap_new_y)) {
            self.pos = (wrap_new_x, wrap_new_y);
        }
    }

    fn next_pos_cube(&mut self) {
        let dir = direction(self.crse_idx);
        let (new_x, new_y) = (self.pos.0 + dir.0, self.pos.1 + dir.1);
        let (on_face, off_dir) = self.cube.faces[&self.current_face].is_on_face( (new_x, new_y) );
        
        let mut wrap_new_x = self.wrap_lims_linear(new_x, true);
        let mut wrap_new_y = self.wrap_lims_linear(new_y, false);
        let mut on_side = Side::RIGHT;
        
        if !on_face {
            let map = self.cube.get_map(&self.current_face, off_dir);
            on_side = map.1;
            (wrap_new_x, wrap_new_y) = map.0[&self.pos];
        }

        if self.blocked.contains(&(wrap_new_x, wrap_new_y)){return;}
        self.pos = (wrap_new_x, wrap_new_y);

        if !on_face {
            self.current_face = self.cube.get_face(self.pos);
            let num_turns = self.cube.get_dir_shift(off_dir, on_side);
            for _i in 0..num_turns {self.turn_right();}
        }
    }

    fn follow_instructions(&mut self, instructions: Vec<String>) -> i32 {
        for ins in instructions {
            match ins.as_str() {
                "R" => self.turn_right(),
                "L" => self.turn_left(),
                _ => { 
                    let steps = ins.parse::<i32>().unwrap();
                    for _i in 0..steps {
                        if self.is_cube { self.next_pos_cube();}
                        else { self.next_pos(); }
                    }
                }
            }
        }
        return 1000*(self.pos.1+1) + 4*(self.pos.0+1) + self.crse_idx;        
    }
}



fn path_find(my_file_name: &str) -> (i32, i32){        
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();
    let line_vec: Vec<String> = buf_lines.map(|l| l.expect("Fail to parse")).collect();

    let (mut max_x, mut max_y) = (0,0);
    let mut free: HashSet<Pos> = HashSet::new();
    let mut blocked: HashSet<Pos> = HashSet::new();
    let mut x_lims: Vec<Pos> = Vec::new();
    let mut y_lims: Vec<Pos> = Vec::new();

    for (line_idx, line) in line_vec.iter().enumerate() {
        max_y = cmp::max(max_y, line_idx);
        if line.trim() == "" {break;}
        let mut valid_x_pos: Vec<i32> = Vec::new();

        for (char_idx, ch) in line.chars().enumerate() {
            if char_idx >= line.len()-1 {continue;}

            max_x = cmp::max(max_x, char_idx);
            if ch == '.' {
                free.insert( (char_idx as i32, line_idx as i32));
                valid_x_pos.push(char_idx as i32);
            }
            else if ch == '#' {
                blocked.insert( (char_idx as i32, line_idx as i32) );
                valid_x_pos.push(char_idx as i32);
            }
        }
        x_lims.push( (valid_x_pos.iter().min().unwrap().clone(), valid_x_pos.iter().max().unwrap().clone() ) );
    }

    for x in 0..=max_x {
        let mut valid_y_pos : Vec<i32> = Vec::new();
        for y in 0..line_vec.len() {
            if free.contains(&(x as i32,y as i32)) || blocked.contains(&(x as i32,y as i32)) {
                valid_y_pos.push(y as i32);
            }
        }
        y_lims.push( ( valid_y_pos.iter().min().unwrap().clone(), valid_y_pos.iter().max().unwrap().clone() ));
    }

    let instruction_string = line_vec.last().clone().unwrap();
    let instructions: Vec<String> = instruction_string.chars()
                                        .group_by(|&x| x.is_alphabetic())
                                        .into_iter()
                                        .map(|(_, r)| r.collect() )
                                        .collect();

    //println!("{:?}",instructions);


    
    //let mut part_one = 0;

    let a = CubeFace{name:"A".to_string(), xlims:(50, 99), ylims:(0, 49),    right_target:("B".to_string(),Side::LEFT,false),
                         down_target:("C".to_string(),Side::UP,false), left_target:("D".to_string(),Side::LEFT, true), up_target:("F".to_string(), Side::LEFT, false),
                        right_map:HashMap::new(), down_map:HashMap::new(), left_map:HashMap::new(), up_map:HashMap::new()};
    let b = CubeFace{name:"B".to_string(), xlims:(100, 149), ylims:(0, 49),  right_target:("E".to_string(),Side::RIGHT, true),
                         down_target:("C".to_string(),Side::RIGHT, false), left_target:("A".to_string(),Side::RIGHT, false), up_target:("F".to_string(),Side::DOWN, false),
                        right_map:HashMap::new(), down_map:HashMap::new(), left_map:HashMap::new(), up_map:HashMap::new()};
    let c = CubeFace{name:"C".to_string(), xlims:(50, 99), ylims:(50, 99),   right_target:("B".to_string(),Side::DOWN, false),
                         down_target:("E".to_string(),Side::UP, false), left_target:("D".to_string(),Side::UP, false), up_target:("A".to_string(),Side::DOWN, false),
                        right_map:HashMap::new(), down_map:HashMap::new(), left_map:HashMap::new(), up_map:HashMap::new()};
    let d = CubeFace{name:"D".to_string(), xlims:(0, 49), ylims:(100, 149),  right_target:("E".to_string(),Side::LEFT, false),
                         down_target:("F".to_string(),Side::UP, false), left_target:("A".to_string(),Side::LEFT, true), up_target:("C".to_string(),Side::LEFT, false),
                        right_map:HashMap::new(), down_map:HashMap::new(), left_map:HashMap::new(), up_map:HashMap::new()};
    let e = CubeFace{name:"E".to_string(), xlims:(50, 99), ylims:(100, 149), right_target:("B".to_string(),Side::RIGHT, true),
                         down_target:("F".to_string(),Side::RIGHT, false), left_target:("D".to_string(),Side::RIGHT, false), up_target:("C".to_string(),Side::DOWN, false),
                        right_map:HashMap::new(), down_map:HashMap::new(), left_map:HashMap::new(), up_map:HashMap::new()};
    let f = CubeFace{name:"F".to_string(), xlims:(0, 49 ), ylims:(150, 199),  right_target:("E".to_string(),Side::DOWN, false),
                         down_target:("B".to_string(),Side::UP, false), left_target:("A".to_string(),Side::UP, false), up_target:("D".to_string(),Side::DOWN, false),
                        right_map:HashMap::new(), down_map:HashMap::new(), left_map:HashMap::new(), up_map:HashMap::new()};
    

    let mut face_map : HashMap<String, CubeFace> = HashMap::new();
    face_map.insert("A".to_string(), a);
    face_map.insert("B".to_string(), b);
    face_map.insert("C".to_string(), c);
    face_map.insert("D".to_string(), d);
    face_map.insert("E".to_string(), e);
    face_map.insert("F".to_string(), f);

    let dummy_cube = Cube{faces:HashMap::new()};
    let mut cube = Cube{faces:face_map};
    cube.build_mappings();

    let start_pos = (x_lims[0].0, 0);

    let mut turtle_one = Turtle{crse_idx:0, pos:start_pos, free:free.clone(), blocked:blocked.clone(), xlims:x_lims.clone(), ylims:y_lims.clone(), is_cube:false, cube:dummy_cube, current_face:String::from("A") };  
    let part_one = turtle_one.follow_instructions(instructions.clone());

    //let mut turtle_two = Turtle{crse_idx:0, pos:start_pos.clone(), free:free.clone(), blocked:blocked.clone(), xlims:x_lims.clone(), ylims:y_lims.clone(), is_cube:true, cube:cube, current_face:String::from("A") };  
    //let part_two = turtle_two.follow_instructions(instructions.clone());
    let part_two = 0;





    
    
    return (part_one, part_two);
}




