use std::fs::File;
use std::io::{BufRead, BufReader};
use std::time::Instant;
use std::cmp;

type Packet = Option<serde_json::Value>;


fn main() {   
    let start = Instant::now();
    let file_name= "C:\\Users\\Chris\\Documents\\CodeProjects\\AdventOfCode\\Yr2022\\PuzzleData\\puzzle_day_thirteen.txt";
    let (part_one, part_two) = order_packets(file_name);
    let duration = start.elapsed();    
    println!("Part One: {}  Part Two: {}", part_one, part_two);
    println!("Time taken to execute: {} microseconds", duration.as_micros());    
}


// Returns two bools, first is good order, second is equal
fn is_good_order(packet_one: &Packet, packet_two: &Packet) -> (bool, bool) {
    match (packet_one, packet_two) {
        (None, None) => unreachable!(),
        (None, Some(_)) => (true, false),
        (Some(_), None) => (false, false),
        (Some(one), Some(two)) => {
            if one.is_number() && two.is_number() {
                let a = one.as_u64().unwrap();
                let b = two.as_u64().unwrap();
                (a <= b, a ==b )
            }
            else if one.is_number() && two.is_array() {
                is_good_order(&Some(serde_json::Value::Array(vec![one.clone()])),
                              &Some(two.clone()))
            }
            else if two.is_number() && one.is_array() {
                is_good_order(&Some(one.clone()),
                              &Some(serde_json::Value::Array(vec![two.clone()]))                               )
            }
            else {
                let mut good_order : bool = true;
                let mut undetermined: bool = true;
                let max_len: usize = cmp::max(one.as_array().unwrap().len(), two.as_array().unwrap().len());
                let mut idx: usize = 0;

                while good_order && undetermined && idx < max_len {
                    (good_order, undetermined) = is_good_order(&one.get(idx).cloned(),
                                                            &two.get(idx).cloned());
                    idx += 1;
                }
                return (good_order, undetermined);
            }
        }
    }
}


fn order_packets(my_file_name: &str) -> (usize, usize) {    
    
    let file = File::open(my_file_name).expect("File does not exist");
    let buf_lines = BufReader::new(file).lines();    
    let input_packets: Vec<Packet> = buf_lines.filter_map(|l| (serde_json::from_str(&l.expect("")).ok())).collect();

    let good_ordered_idxs : Vec<usize> = input_packets
                                                .chunks(2)
                                                .into_iter()
                                                .enumerate()
                                                .filter(|(_, pair)| is_good_order(&pair[0], &pair[1]).0)
                                                .map(|(i, _)| i+1)
                                                .collect();
    let part_one: usize = good_ordered_idxs.iter().sum();

    let packet_two = serde_json::from_str("[[2]]").ok();
    let packet_six = serde_json::from_str("[[6]]").ok();
    let mut packet_two_counter = 1;
    let mut packet_six_counter = 2;

    for packet in input_packets {
        if is_good_order(&packet, &packet_two).0 { packet_two_counter += 1; }
        if is_good_order(&packet, &packet_six).0 { packet_six_counter += 1; }
    }
    let part_two = packet_two_counter * packet_six_counter;
    return (part_one, part_two);
}
