from dataclasses import dataclass
from typing import List, Dict
import tqdm
from functools import lru_cache, reduce
import numpy as np

def get_lines(file):
    with open(file, 'r') as in_file:
        result_lines =  in_file.readlines()
    result_lines = [line.strip() for line in result_lines]
    return result_lines


@dataclass
class Race:
    duration: int
    record: int

    def beats_record(self, hold_time):
        distance = (self.duration - hold_time) * hold_time
        return distance > self.record
    
    def num_beating_moves(self):
        discriminant = np.sqrt(self.duration**2 - 4*self.record)
        root_one, root_two = (self.duration + discriminant)/2, (self.duration - discriminant)/2
        round_root_one, round_root_two = np.floor(root_one), np.ceil(root_two)
        success_interval = (round_root_one - round_root_two) + 1
        for root in round_root_one, round_root_two:
            if not self.beats_record(root):    # subtract if the root exactly matches record
                success_interval -= 1
        return int(success_interval)



@dataclass
class Tournament:
    race_list: List[Race]

    @classmethod
    def from_line_arr(cls, line_arr, part_one=True):
        if part_one:
            times, records = line_arr[0].split(':')[1].strip().split(' '), line_arr[1].split(':')[1].strip().split(' ')
            times, records = [time for time in times if time.isdigit()], [record for record in records if record.isdigit()]
            return Tournament([Race(int(time), int(record)) for time, record in zip(times,records)])
        else:
            times, records = [ch for ch in line_arr[0] if ch.isdigit()], [ch for ch in line_arr[1] if ch.isdigit()]
            return Tournament([Race(int(''.join(times)), int(''.join(records)))])

    def beating_moves(self):
        return [race.num_beating_moves() for race in self.race_list]
    
    def error_margin(self):
        return reduce(lambda x,y :x*y, self.beating_moves())



if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day06.txt' 
    lines = get_lines(filename)
    part_one_tourney = Tournament.from_line_arr(lines)
    part_two_tourney = Tournament.from_line_arr(lines, part_one=False)
    part_one = part_one_tourney.error_margin()
    part_two = part_two_tourney.error_margin()

    print(f"Part One: {part_one}    Part Two:  {part_two}")
    
  