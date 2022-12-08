use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;
use std::cmp;


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_eight.txt";
    let (arr, arr_t) = build_arr(file_name);
    let vis_count = count_visible(&arr, &arr_t);
    let max_scenic_score_val = max_scenic_score(&arr, &arr_t);
    let duration = start.elapsed();
    println!("Visible Trees: {}", vis_count);
    println!("Max scenic score: {}", max_scenic_score_val);
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}


fn transpose<T>(v: Vec<Vec<T>>) -> Vec<Vec<T>>
where
    T: Clone,
{
    assert!(!v.is_empty());
    (0..v[0].len())
        .map(|i| v.iter().map(|inner| inner[i].clone()).collect::<Vec<T>>())
        .collect()
}


fn build_arr(my_file_name: &str) -> (Vec<Vec<u32>>, Vec<Vec<u32>>) {    
    let mut vec_arr : Vec<Vec<u32>> = Vec::new();   
    if let Ok(lines) = read_lines(my_file_name) {
        for line in lines {
            if let Ok(ip) = line {
                let mut line_vec = Vec::new();
                for c in ip.chars() {
                    let my_int = c.to_digit(10);
                    match my_int {
                        Some(i) => line_vec.push(i),
                        None => (),
                    }
                }                
                vec_arr.push(line_vec);
            }
        }
    }
    let arr_t = transpose(vec_arr.clone());
    return (vec_arr, arr_t);
}


fn check_max(slice : &[u32], arr: &Vec<Vec<u32>>, row_idx: usize, col_idx: usize) -> bool{
    match slice.iter().max() {
        Some(x) => return x < &arr[col_idx][row_idx],
        None => return false,
    }
}


fn is_element_visible(arr: &Vec<Vec<u32>>, arr_t: &Vec<Vec<u32>>, row_idx: usize, col_idx: usize) -> bool {
    if row_idx == 0 || row_idx == arr[0].len()-1 || col_idx == 0 || col_idx == arr.len()-1 {
        return true;
    }
    let mut visible: bool = false;
    let left : &[u32] =  &arr[col_idx][0..row_idx];
    let right : &[u32] =  &arr[col_idx][row_idx+1..];
    let up : &[u32] =  &arr_t[row_idx][0..col_idx];
    let down : &[u32] =  &arr_t[row_idx][col_idx+1..];
    
    visible = visible || check_max(&left, &arr, row_idx, col_idx);
    visible = visible || check_max(&right, &arr, row_idx, col_idx);
    visible = visible || check_max(&up, &arr, row_idx, col_idx);
    visible = visible || check_max(&down, &arr, row_idx, col_idx);

    return visible;
}


fn count_visible(arr: &Vec<Vec<u32>>, arr_t: &Vec<Vec<u32>>) -> u32 {
    let mut counter : u32 = 0;
    let iter = (0..arr[0].len()).map(|row_idx| arr.iter().flatten().skip(row_idx).step_by(arr.len()));
    for (row_idx, row_values) in iter.enumerate() {
        for (col_idx, _value) in row_values.enumerate() {
            if is_element_visible(arr, arr_t, row_idx, col_idx) {
                counter += 1;
            }
        }
    }
    return counter;
}


fn check_direction(slice: &[u32], this_tree: &u32, reverse: bool) -> usize {
    if reverse {
       for (tree_idx, tree) in slice.into_iter().rev().enumerate() {
            if tree >= this_tree {
                return tree_idx + 1;
            }
        }
    }
    else {
        for (tree_idx, tree) in slice.iter().enumerate() {
            if tree >= this_tree {
                return tree_idx + 1;
            }
        }
    }
    return slice.len();
}


fn scenic_score(arr: &Vec<Vec<u32>>, arr_t: &Vec<Vec<u32>>, row_idx: usize, col_idx: usize) -> u32 {
    if row_idx == 0 || row_idx == arr[0].len()-1 || col_idx == 0 || col_idx == arr.len()-1 {
        return 0;
    }
    let mut scenic_score: u32 = 1;
    let this_tree = &arr[col_idx][row_idx];
    let left : &[u32] =  &arr[col_idx][0..row_idx];
    let right : &[u32] =  &arr[col_idx][row_idx+1..];
    let up : &[u32] =  &arr_t[row_idx][0..col_idx];
    let down : &[u32] =  &arr_t[row_idx][col_idx+1..];
    
    scenic_score *= check_direction(&left, this_tree, true) as u32;
    scenic_score *= check_direction(&right, this_tree, false) as u32;
    scenic_score *= check_direction(&up, this_tree, true) as u32;
    scenic_score *= check_direction(&down, this_tree, false) as u32;

    return scenic_score;
}


fn max_scenic_score(arr: &Vec<Vec<u32>>, arr_t: &Vec<Vec<u32>>) -> u32 {
    let mut result : u32 = 0;
    let iter = (0..arr[0].len()).map(|row_idx| arr.iter().flatten().skip(row_idx).step_by(arr.len()));
    for (row_idx, row_values) in iter.enumerate() {
        for (col_idx, _value) in row_values.enumerate() {
            let this_score = scenic_score(&arr, &arr_t, row_idx, col_idx);            
            result = cmp::max(result, this_score);
            
        }
    }
    return result;
}