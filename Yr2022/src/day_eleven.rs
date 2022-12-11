use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use std::collections::HashMap;



fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_eleven.txt";
    let part_one = false;
    let monkey_business = load_monkeys(file_name, part_one);    
    let duration = start.elapsed();
    println!("Monkey Business: {}", monkey_business);
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}



pub struct Item  {
    val : u32,
    remainders: HashMap<u32, u32>,
}

impl Item {
    pub fn reduce(&mut self, divisor_list: &Vec<u32>) {
        for div in divisor_list {
            self.remainders.entry(*div).and_modify(|x| {*x = *x % div}).or_insert(self.val as u32);
            }
    }
    pub fn is_divisible_by(&mut self, div: u32) -> bool {
        return self.remainders[&div] == 0;
    }
}


pub struct Monkey {
    items: Vec<Item>,
    op_char: char,
    modifier: u32,
    divisor: u32,
    true_tgt: u32,
    false_tgt: u32,
    inspect_ctr: u32,    
}

impl Monkey {
    pub fn inspect(&mut self, divisor_list: &Vec<u32>, part_one: bool) -> (u32, Item) {
        let mut item = self.items.pop().expect("There should be an item");
        self.inspect_ctr += 1;
        match part_one {
        true => {  match self.op_char {
                '*' => {  item.val =  (item.val * self.modifier)/3 ; },
                '+' => {  item.val =  (item.val + self.modifier)/3 ; },
                _ => {  item.val =  (item.val * item.val)/3; },
            }  
            let tgt = if item.val % self.divisor  == 0 {self.true_tgt} else {self.false_tgt};
            return (tgt, item);
            },
        false => { match self.op_char {
                '*' => { for v in item.remainders.values_mut() {*v =  *v * self.modifier; }},
                '+' => { for v in item.remainders.values_mut() {*v =  *v + self.modifier; }},
                _ => { for v in item.remainders.values_mut() {*v =  *v * *v; }},
            }        
            item.reduce(divisor_list);
            let tgt = if item.is_divisible_by(self.divisor) {self.true_tgt} else {self.false_tgt};
            return (tgt, item);
        }    
        }
    }
    
    pub fn reduce_all(&mut self, divisor_list: &Vec<u32>) {
        for _idx in 0..self.items.len() {
            self.items[_idx].reduce(divisor_list);
        }
    }
}


fn simulate_round(monkey_map: &mut HashMap<u32, Monkey>, divisor_list: &Vec<u32>, part_one: bool) {
    for _monkey_idx_usize in 0..monkey_map.len() {
        let monkey_idx = _monkey_idx_usize as u32;
        while monkey_map[ &monkey_idx ].items.len() > 0 {
            let (tgt, item) = monkey_map.get_mut(&monkey_idx).map(|val| val.inspect(divisor_list, part_one)).expect("");
            monkey_map.entry(tgt).and_modify(|x| {x.items.push(item)});
        }
    }
}


fn simulate_monkeys(monkey_map: &mut HashMap<u32, Monkey>, num_rounds: usize, part_one:bool) {
    let divisor_list: Vec<u32> = monkey_map.iter().map(|(_k,v)| v.divisor ).collect();
    for monkey in monkey_map.values_mut() {
        monkey.reduce_all(&divisor_list);
    }
    for _i in 0..num_rounds {
        simulate_round(monkey_map, &divisor_list, part_one);
    }
}


fn get_monkey_business(monkey_map: &HashMap<u32, Monkey>) -> u32{
    let mut activities : Vec<u32> = monkey_map.values().map(|m| m.inspect_ctr).collect();
    activities.sort_by(|a,b| b.cmp(a) );    
    return activities[0] * activities[1];
}


fn load_monkeys(my_file_name: &str, part_one: bool) -> u32{    
    let mut monkey_map :HashMap<u32, Monkey> = HashMap::new();
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();
    let line_vec: Vec<String> = buf_lines.map(|l| l.expect("Fail to parse")).collect();

    for line_idx in (0..line_vec.len()).step_by(7) {
        let first_line: Vec<&str> = line_vec[line_idx].split(&[' ', ':']).collect();
        let m_id : u32 = first_line[1].parse().unwrap();

        let second_line : Vec<&str> = line_vec[line_idx + 1].split(&[':']).collect();
        let item_list_str: Vec<&str> = second_line[1].split(&[',']).collect();
        let item_list : Vec<u32> = item_list_str.iter().map(|s| s.trim().parse::<u32>().unwrap()).collect();

        let third_line : Vec<&str> = line_vec[line_idx + 2].split(&[' ']).collect();
        let modifier_str  = third_line[7];
        let mut arg_op_char = 'X';
        let mut arg_modifier = 0;
        match modifier_str {
            "old" => (),
            _ => {arg_op_char = third_line[6].chars().next().unwrap();
                 arg_modifier = modifier_str.parse::<u32>().unwrap();}
        }

        let fourth_line : Vec<&str> = line_vec[line_idx + 3].split(&[' ']).collect();
        let arg_divisor : u32 = fourth_line[5].parse::<u32>().unwrap();

        let fifth_line : Vec<&str> = line_vec[line_idx + 4].split(&[' ']).collect();
        let arg_t_tgt: u32 = fifth_line[9].parse::<u32>().unwrap();
        
        let sixth_line : Vec<&str> = line_vec[line_idx + 5].split(&[' ']).collect();
        let arg_f_tgt: u32 = sixth_line[9].parse::<u32>().unwrap();

        monkey_map.insert(m_id, Monkey {items:Vec::new(), op_char:arg_op_char, modifier:arg_modifier,
                                divisor:arg_divisor, true_tgt:arg_t_tgt, false_tgt:arg_f_tgt, inspect_ctr:0});
        for item_val in item_list {
            monkey_map.get_mut(&m_id).expect("").items.push(Item {val:item_val , remainders:HashMap::new()});
        }

    }
    
    let runs = if part_one {20} else {10000};
    simulate_monkeys(&mut monkey_map, runs, part_one);
    let monkey_business = get_monkey_business(&monkey_map);
    return monkey_business;
}

