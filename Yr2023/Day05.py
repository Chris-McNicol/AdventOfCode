from dataclasses import dataclass
from typing import List, Dict
import tqdm
from functools import lru_cache


def get_lines(file):
    with open(file, 'r') as in_file:
        result_lines =  in_file.readlines()
    result_lines = [line.strip() for line in result_lines]
    return result_lines


@dataclass
class SeedMap:
    src_start: int
    dest_start: int
    map_range: int    

    def map_val(self, val):
        return self.dest_start - self.src_start + val
    
    def is_mapped(self, val):
        return (self.src_start <= val < self.src_start+self.map_range)
    

@dataclass
class ElfMap:
    source_name: str
    dest_name: str
    mapping: List[SeedMap]
    cache: Dict


    @classmethod
    def from_line_array(cls, line_arr):        
        mapping = []
        name_break = line_arr[0].split('-')
        src_name, dest_name = name_break[0], name_break[2][:-5]  
        for line in line_arr[1:]:
            dest_start, src_start, map_range = line.split(' ')
            mapping.append(SeedMap(int(src_start), int(dest_start), int(map_range)))
        return ElfMap(src_name, dest_name, mapping, {})
    

    def mapped_val(self, input_val):       
        for each_map in self.mapping:
            if each_map.is_mapped(input_val):
                output_val = each_map.map_val(input_val)
                return output_val
        return input_val


    def check_interval(self, input_interval):
        overlaps = []
        for elf_map in self.mapping:
            src, seed_range = elf_map.src_start, elf_map.map_range
            appendices = []
            while input_interval:                
                start, end = input_interval.pop()                
                prefix =  (start, min(end, src))
                overlap = (max(start, src), min(src + seed_range, end))
                suffix =  (max(src + seed_range, start), end)
                if prefix[0] < prefix[1]:
                    appendices.append(prefix)
                if overlap[0] < overlap[1]:
                    overlaps.append( (elf_map.map_val(overlap[0]), elf_map.map_val(overlap[1])) )
                if suffix[0] < suffix[1]:
                    appendices.append(suffix)
            input_interval = appendices
        return overlaps+input_interval
        

@dataclass
class ElfMegaMap:
    seeds: List[int]
    elf_maps: List[ElfMap]

    @classmethod
    def from_line_array(cls, line_arr):
        seeds = [int(seed) for seed in line_arr[0].split(' ')[1:] if seed.isdigit()]
        mappings = []
        map_lines, current_map_lines = [], []
        for line in line_arr[2:]:
            if line == '':
                map_lines.append(current_map_lines)
                current_map_lines = []
            else:
                current_map_lines.append(line)
        map_lines.append(current_map_lines)
        mappings = [ElfMap.from_line_array(map_line) for map_line in map_lines]
        return ElfMegaMap(seeds, mappings)
    

    def find_loc_for_seed(self, seed):
        val = seed
        for elf_map in self.elf_maps:
            val = elf_map.mapped_val(val)
        return val

    def get_min_loc(self, part_one=True):
        if part_one:
            loc_list = [self.find_loc_for_seed(seed) for seed in self.seeds]
            return min(loc_list)
        else:    
            interval_lower_bounds = []        
            for seed_start, seed_range in zip(self.seeds[::2], self.seeds[1::2]):            
                interval = [(seed_start, seed_start + seed_range)]
                for elf_map in self.elf_maps:
                    interval = elf_map.check_interval(interval)                
                interval_lower_bounds.append(min(interval)[0])            
            return min(interval_lower_bounds)
            

if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day05.txt' 
    #filename = r'Yr2023\PuzzleData\Example.txt'
    lines = get_lines(filename)
    mega_map = ElfMegaMap.from_line_array(lines)    
    part_one = mega_map.get_min_loc(part_one=True)
    part_two = mega_map.get_min_loc(part_one=False)
        
    print(f"Part One: {part_one}    Part Two:  {part_two}")
    
  