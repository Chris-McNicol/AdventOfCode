use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;
//use std::boxed::Box;

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
    let _file_system = file_system_build(file_name); 
    let duration = start.elapsed();
    //println!("Packet start: {}    Message start: {}", file_system);    
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


fn read_lines<P>(filename: P) -> io::Result<io::Lines<io::BufReader<File>>>
where P: AsRef<Path>, {
    let file = File::open(filename)?;
    Ok(io::BufReader::new(file).lines())
}





fn file_system_build(my_file_name: &str) -> (usize, usize) {
    
    //let mut file_system : FileSystem =  FileSystem::new("/", 0, FileType::DIRECTORY);
   
    if let Ok(lines) = read_lines(my_file_name) {
        for line in lines {
            if let Ok(ip) = line {
                let _bloop = String::from("bloop");
                match ip {
                    _bloop => println!("Bloop"),

                }

            }
        }
    }
    return (0,0);
}
