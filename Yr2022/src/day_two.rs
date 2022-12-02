use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;
use std::collections::HashMap;

#[macro_use]
extern crate lazy_static;

#[derive(Eq, PartialEq, Hash, Copy, Clone)]
pub enum RPS {
    ROCK = 1,
    PAPER = 2,
    SCISSORS = 3,
}

#[derive(Eq, PartialEq, Hash, Copy, Clone)]
pub enum OUTCOME {
    WIN = 6,
    DRAW = 3,
    LOSE = 0,
}

lazy_static! {
static ref MOVE_MAP : HashMap<char, RPS> = HashMap::from([('A',RPS::ROCK), ('B',RPS::PAPER), ('C',RPS::SCISSORS),
            ('X',RPS::ROCK), ('Y',RPS::PAPER), ('Z',RPS::SCISSORS)]);

static ref WIN_MAP : HashMap<RPS, RPS> = HashMap::from([(RPS::ROCK,RPS::SCISSORS), (RPS::PAPER,RPS::ROCK), (RPS::SCISSORS,RPS::PAPER)]);

static ref LOSE_MAP : HashMap<RPS, RPS> = HashMap::from([(RPS::SCISSORS,RPS::ROCK), (RPS::ROCK,RPS::PAPER), (RPS::PAPER,RPS::SCISSORS)]);

static ref OUTCOME_MAP : HashMap<char, OUTCOME> = HashMap::from([('X',OUTCOME::LOSE), ('Y',OUTCOME::DRAW), ('Z',OUTCOME::WIN)]);
}


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_two.txt";
    let tot_score = sum_scores(file_name, true);
    let duration = start.elapsed();
    println!("Total score: {}", tot_score);    
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}


fn strategy_score(opponent_move: &RPS, my_move : &RPS) -> i32 {
    //Calculate score assuming 2nd column is my move
    let mut result_score = *my_move as i32;
    let win_move = WIN_MAP.get(my_move).unwrap();
    if opponent_move == win_move {
        result_score += OUTCOME::WIN as i32; }
    else if opponent_move == my_move {
        result_score += OUTCOME::DRAW as i32;        
    }
    return result_score;
}


fn outcome_score(opponent_move: &RPS, outcome_required : &OUTCOME) -> i32{
    //Calculate score assuming 2nd column is outcome required
    let mut result_score = *outcome_required as i32;
    match outcome_required {
        OUTCOME::DRAW => result_score += *opponent_move as i32,
        OUTCOME::LOSE => result_score += *WIN_MAP.get(opponent_move).unwrap() as i32,
        OUTCOME::WIN => result_score += *LOSE_MAP.get(opponent_move).unwrap() as i32,
    }
    return result_score;
}


fn sum_scores(my_file_name: &str, outcome_method: bool) -> i32 {
    // Sum the scores using one of two methods
    let mut total_score: i32 = 0;
    if let Ok(lines) = read_lines(my_file_name) {
        for line in lines {
            if let Ok(ip) = line {
                let first_char = ip.chars().nth(0).unwrap();
                let second_char = ip.chars().nth(2).unwrap();
                if outcome_method {
                    total_score += outcome_score(MOVE_MAP.get(&first_char).unwrap(),
                                                 OUTCOME_MAP.get(&second_char).unwrap());
                }
                else {
                    total_score += strategy_score(MOVE_MAP.get(&first_char).unwrap(),
                                                 MOVE_MAP.get(&second_char).unwrap());
                }            
            }
        }
    }
    return total_score
}

