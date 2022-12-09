use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;
//use std::boxed::Box;
use std::collections::HashMap;

/*

I WAS HOPING TO BE ABLE TO USE SOME OOP OR TREE STRUCTURE TO REPRESENT
THE DIRECTORY STRUCTURE BUT IT APPEARS THAT IT IS REALLY DIFFICULT TO 
IMPLEMENT THIS KIND OF DATA STRUCTURE IN RUST



*/



/*
enum FileType {
    DIRECTORY,
    FILE,
}

pub struct FileSystem {
    name: String,
    size: u32,
    ftype: FileType,
    child_list: Vec<Box<FileSystem>>
}


impl FileSystem {
    pub fn new(n:&str, s:u32, ft: FileType) -> FileSystem {
        FileSystem {name:n.to_string(), size:s, ftype:ft, child_list: Vec::new() }
    }



    pub fn get_box(self, box_name: String) -> Option<Box<FileSystem>> {
        if box_name.is_empty() {
            return Some(Box::new(self));
        }
        let search_name = box_name.replace(&self.name, "");
        let x = self.child_list.iter().find(|x| x.name.starts_with(&search_name) );        
        match x {
            Some(x) => return Some(*x.clone()),
            _ => return None,
        }
    }
}
*/





fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_seven.txt";
    let file_system = file_system_build(file_name); 
    
    let size_dict = dir_structure(&file_system);
    let total_under = total_under_val(&size_dict, 100000);
    let free_space = unused_space(&file_system, 70000000);
    let min_over = min_over_val(&size_dict, 30000000-free_space);
    let duration = start.elapsed();
    println!("Part One: {}    Part Two: {}", total_under, min_over);   
    println!("Time taken to execute: {} microseconds", duration.as_micros());    

}


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}


fn file_system_build(my_file_name: &str) -> HashMap<String, u32> {
    
    //let mut file_system : FileSystem =  FileSystem::new("/", 0, FileType::DIRECTORY);
    let mut file_system : HashMap<String, u32> = HashMap::new();
    let mut current_path : Vec<String> = vec!["".to_string()];
       
    if let Ok(lines) = read_lines(my_file_name) {
        for line in lines {
            if let Ok(ip) = line {                                
                if &ip[0..4] == "$ cd" {                    
                    if &ip[4..] == " /" {
                        current_path = vec!["".to_string()];
                    }
                    else if &ip[4..] == " .." {
                        current_path.pop();
                    }
                    else {                        
                        let new_str = &ip[5..].to_string();
                        current_path.push(new_str.clone());
                        let dirpath_str = current_path.clone().join("/");
                        file_system.insert(  dirpath_str, 0 as u32 );
                    }
                }

                if ip.chars().next().expect("Should be a char").is_numeric() {
                    let details : Vec<&str> = ip.split(' ').collect();
                    let filepath_str = &mut current_path.clone().join("/").to_string();
                    filepath_str.push('/');
                    filepath_str.push_str(details[1]);                    
                    file_system.insert(filepath_str.to_string(), details[0].parse::<u32>().unwrap());
                }           
            }
        }
    }
    return file_system;
}


fn dir_size(file_system: &HashMap<String, u32>, dir_path: String) -> u32 {
    return file_system.iter().filter_map(|(k,v)| {
        match k.contains(&dir_path) {
            true => Some(v),
            _ => None, }
        }).sum();
}


fn dir_structure(file_system: &HashMap<String, u32>) -> HashMap<String, u32> {
    let mut result : HashMap<String, u32> = HashMap::new();
    for (k, _v) in file_system.iter() {        
            let mut dir_path_vec: Vec<&str> = k.split('/').collect();
            dir_path_vec.pop();
            let dir_path_str : String = dir_path_vec.join("/");
            let dir_path_key = dir_path_str.clone();
        if !result.contains_key(&dir_path_key) {
            result.insert(dir_path_str, dir_size(file_system, dir_path_key));
        }
    }
    return result;
}


fn total_under_val(size_dict: &HashMap<String, u32>, val: u32) -> u32 {
    return size_dict.values().filter(|&&v| v <= val).sum();
}

fn min_over_val(size_dict: &HashMap<String, u32>, val: u32) -> u32 {
    return *size_dict.values().filter(|&&v| v >= val).min().unwrap();
}

fn unused_space(file_system: &HashMap<String, u32>, total_disk_space: u32) -> u32 {
    let total_used: u32 = file_system.values().sum();
    return total_disk_space - total_used;
}
