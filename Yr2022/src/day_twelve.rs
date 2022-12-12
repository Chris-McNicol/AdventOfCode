use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use std::collections::HashMap;
use std::hash::Hash;
use std::collections::BinaryHeap;
use std::cmp::Ordering;
use std::cmp;

type Pos = (usize,usize);


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_twelve.txt";
    load_landscape(file_name);
    let duration = start.elapsed();    
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


struct Graph<T: Eq> {
    nodes: HashMap<T, Vec<(T, usize)>>,
}

impl <T: Eq + Hash> Graph<T> {
    pub fn add_edge(&mut self, u: T, v: T, edge_w: usize ) {
        self.nodes.entry(u).or_insert(Vec::new()).push( (v, edge_w));
    }
}


#[derive(Copy, Clone, Eq, PartialEq)]
struct State {
    cost: usize,
    position: (usize,usize),
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        other.cost.cmp(&self.cost).then_with(|| self.position.cmp(&other.position))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}



fn shortest_paths(graph: &Graph<Pos>, s: Pos, d: Pos, arr: &Vec<Vec<i32>>,
                 target_height: i32) -> Option<usize> {
    let mut costs : HashMap<Pos, usize> = HashMap::new();

    for (node, _) in graph.nodes.iter() {
        costs.insert(*node, usize::MAX);
    }
    costs.insert(s, 0);
    let mut heap = BinaryHeap::new();
    heap.push(State { cost: 0, position: s});

    while let Some( State {cost, position} ) = heap.pop() {
        if position == d { return Some(cost); }

        if target_height >= 0 {
            if arr[position.0][position.1] == target_height {
                return Some(cost);
            }
        }

        if cost > costs[&position] { continue;}
        
        if graph.nodes.contains_key(&position) {
            for edge in &graph.nodes[&position] { 
                let next = State {cost: cost + edge.1, position: edge.0};
                if costs.contains_key(&next.position) {
                    if next.cost < costs[&next.position] {
                        heap.push(next);
                        costs.insert(next.position, next.cost);
                    }
                }           
            }
        }
    }
    return None
}


fn is_reachable(arr: &Vec<Vec<i32>>, my_pos: Pos, test_pos: (i32, i32)) -> bool {
    if test_pos.0 < 0 || test_pos.1 < 0 || test_pos.0 >= arr.len() as i32|| test_pos.1 >= arr[0].len() as i32 {
        return false;
    }
    return arr[test_pos.0 as usize][test_pos.1 as usize] <= arr[my_pos.0][my_pos.1] + 1;
}


fn load_landscape(my_file_name: &str){    
    
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();
    let line_vec: Vec<String> = buf_lines.map(|l| l.expect("Fail to parse")).collect();
    let mut arr : Vec<Vec<i32>> = Vec::new();
    let mut start_pos: Pos = (usize::MAX,usize::MAX);
    let mut end_pos: Pos = (usize::MAX,usize::MAX);

    for (line_idx, line) in line_vec.iter().enumerate() {
        let unformat_line_arr: Vec<u32> = line.chars().map(|x| (x as char).into()).collect();
        if let Some(find_start) = unformat_line_arr.iter().position(|&v| v == 83) {start_pos = (line_idx, find_start);}
        if let Some(find_end) = unformat_line_arr.iter().position(|&v| v == 69) {end_pos = (line_idx, find_end);}
        let line_arr = unformat_line_arr.iter().map(|&x| {
            match x {
                69 => 26,
                83 => 1,
                _ =>  x as i32 - 96,
            }}).collect();
        arr.push(line_arr);
    }

    let mut graph = Graph{nodes: HashMap::new() };
    let mut reverse_graph = Graph{ nodes: HashMap::new()};

    for (row_idx, row) in arr.iter().enumerate() {
        for (col_idx, _element) in row.iter().enumerate() {
            let up = (row_idx as i32 -1, col_idx as i32);
            let down = (row_idx as i32 + 1, col_idx as i32);
            let left = (row_idx as i32, col_idx as i32 - 1);
            let right = (row_idx as i32, col_idx as i32 + 1);
            let check_vec = vec![up, down, left, right];
            for direction in check_vec.iter() {
                if is_reachable(&arr, (row_idx, col_idx), *direction) {
                    let source: Pos = (row_idx, col_idx);
                    let target: Pos = (direction.0 as usize, direction.1 as usize);
                    graph.add_edge(source, target, 1);
                    reverse_graph.add_edge(target, source, 1);
                }
            }
        }
    }    

    if let Some(dist) = shortest_paths(&graph, start_pos, end_pos, &arr, -1) {
        println!("Shortest distance (Part One) {}", dist);
    }

    if let Some(min_cost) = shortest_paths(&reverse_graph, end_pos, start_pos, &arr, 1) {
        println!("Shortest distance (Part Two) {}", min_cost);
    }

    return
}

