use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use std::collections::HashMap;


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_seventeen.txt";
    let (part_one, part_two) = solve_tetris(file_name);
    let duration = start.elapsed();    
    println!("Part One: {}  Part Two: {}", part_one, part_two);
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}



const NUM_SHAPES: usize = 5;
const SHAPE_HEIGHT: usize = 4;
const SHAPE_WIDTH: [usize; NUM_SHAPES] = [4,3,3,1,2];
const SHAPE_DATA: [[u8; SHAPE_HEIGHT]; NUM_SHAPES] = [
    [0b1111,0b0000,0b0000,0b0000], //Tall
    [0b0010, 0b0111, 0b0010, 0b0000], // Cross
	[0b0111, 0b0100, 0b0100, 0b0000],	// 
	[0b0001, 0b0001, 0b0001, 0b0001],	// Long
	[0b0011, 0b0011, 0b0000, 0b0000], // Square
];
const BOARD_WIDTH: usize = 7;
const BOARD_DEPTH: usize = 128;

struct TetrisBoard{ 
    height_from_floor:usize,
    height_from_cutoff: usize,
    height_of_cutoff: usize,
    board: [u8; BOARD_DEPTH],
}

impl Default for TetrisBoard {
    fn default() -> TetrisBoard {
        TetrisBoard {height_from_floor:0, height_from_cutoff: 0, height_of_cutoff: 0, board: [0; BOARD_DEPTH],}
    }
}

impl TetrisBoard {
    pub fn no_collision(&self, shape: [u8; SHAPE_HEIGHT], x: usize, y:usize) -> bool {
        (0..SHAPE_HEIGHT).all(|idx| ((shape[idx] << x) & self.board[y+idx]) == 0)
    }
    pub fn place_shape(&mut self, shape: [u8; SHAPE_HEIGHT], x: usize, y:usize) {
        for _i in 0..SHAPE_HEIGHT {
            let vert_slice = shape[_i] << x;
            if vert_slice != 0 {
                self.board[y+_i] |= vert_slice;
                let height = y + _i +1;
                if height > self.height_from_cutoff {
                    self.height_from_cutoff = height;
                    self.height_from_floor = self.height_of_cutoff + height;
                }
            }
        }
    }
    pub fn find_cutoff(&self) -> usize {
        let mask = ((1<< BOARD_WIDTH) -1) as u8;
        let mut row_mask = mask;
        for y in (1..self.height_from_cutoff).rev() {
            row_mask = row_mask & !self.board[y];
            for _i in 0..BOARD_WIDTH {
                let left_wall_mask = (row_mask >> 1) & mask & !self.board[y];
                let right_wall_mask = (row_mask << 1) & mask & !self.board[y];
                let collision_mask = row_mask | left_wall_mask | right_wall_mask;
                if collision_mask == row_mask { break; } // No collision
                row_mask = collision_mask;
            }
            if row_mask == 0 { return y;}    
        }
        
        return 0;
    }
    pub fn make_cutoff(&mut self){
        let y_cutoff = self.find_cutoff();
        self.board.copy_within(y_cutoff.., 0); // shift by y
        self.height_from_cutoff -= y_cutoff;
        self.height_of_cutoff += y_cutoff;
        self.board[self.height_from_cutoff..].fill(0); //fill upper rows with zero
    }
}


#[derive(Clone, PartialEq, Eq, Hash)]
struct State {
    wind_idx: usize,
    board: [u8; BOARD_DEPTH],
}

#[derive(Clone, Copy)]
struct Result {
    num_shapes_placed: usize,
    total_height: usize,
}

fn play_tetris(tetris: &mut TetrisBoard, winds: &[u8], mut wind_idx: usize, num_shapes: usize) {

    let wind_len = winds.len();
    let mut cache: HashMap<State, Result> = HashMap::new();
    let mut shape_idx = 0;

    for _i in 0..num_shapes {
        let shape = SHAPE_DATA[shape_idx];
        let shape_width = SHAPE_WIDTH[shape_idx];
        let mut x_pos = 2;
        let mut y_pos = tetris.height_from_cutoff + 3;

        if y_pos + SHAPE_HEIGHT >= BOARD_DEPTH { // if overflow the top, shift down
            tetris.make_cutoff();
            y_pos = tetris.height_from_cutoff + 3;
        }

        loop {
            let wind = winds[wind_idx];
            wind_idx = (wind_idx + 1)% wind_len;

            match wind {
                b'>' if x_pos + shape_width >= BOARD_WIDTH => (),  //hit right wall
                b'>' => { if tetris.no_collision(shape, x_pos+1, y_pos){x_pos+=1;}}, //wind shift right
                b'<' if x_pos == 0 => (),  //hit left wall
                b'<' => {if tetris.no_collision(shape, x_pos-1, y_pos){x_pos-=1;}} // wind shift left
                _ => unreachable!(),
            }
            if y_pos == 0 {break;} // hit floor
            if !tetris.no_collision(shape, x_pos, y_pos-1) { break; } // hit other shape
            y_pos -= 1;
        }

        tetris.place_shape(shape, x_pos, y_pos);
        shape_idx = (shape_idx + 1 ) % NUM_SHAPES;


        let num_shapes_placed =_i+1;
        let cache_depth = 10 * wind_len * NUM_SHAPES;
        if num_shapes > cache_depth && (num_shapes_placed % cache_depth) == 0 {
            let current_state = State { wind_idx, board: tetris.board.clone(),};
            let current_result = Result { num_shapes_placed, total_height:tetris.height_from_floor,};

            if let Some(previous_result) = cache.get(&current_state) {
                let extra_shapes = current_result.num_shapes_placed - previous_result.num_shapes_placed;
                let extra_height = current_result.total_height - previous_result.total_height;
                let mut shapes_remaining = num_shapes - current_result.num_shapes_placed;
                let num_skips = shapes_remaining / extra_shapes;
                shapes_remaining = shapes_remaining % extra_shapes;
                
                tetris.height_from_floor += num_skips*extra_height;
                tetris.height_of_cutoff += num_skips*extra_height;
                return play_tetris(tetris, winds, wind_idx, shapes_remaining);
            }
            else {
                cache.insert(current_state, current_result);
            }
        }

        

    }

}








fn solve_tetris(my_file_name: &str) -> (usize, usize) {
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();
    let line_vec: Vec<String> = buf_lines.map(|l| l.expect("Fail to parse")).collect();

    let winds: &str = line_vec[0].trim();


    let mut board = TetrisBoard::default();
    play_tetris(&mut board, winds.as_bytes(), 0, 2022);
    let part_one = board.height_from_floor;

    let mut board_two = TetrisBoard::default();
    play_tetris(&mut board_two, winds.as_bytes(), 0, 1000000000000);
    let part_two = board_two.height_from_floor;


    return (part_one, part_two);
}
