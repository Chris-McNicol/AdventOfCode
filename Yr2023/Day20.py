from dataclasses import dataclass
from typing import List, Dict, Set, Tuple
import tqdm
from functools import lru_cache, reduce
import itertools
import numpy as np
from enum import Enum
import math
from heapq import heappush, heappop, heapify
from collections import deque


def get_lines(file):
    with open(file, 'r') as in_file:
        result_lines =  in_file.readlines()
    result_lines = [line.strip() for line in result_lines]
    return result_lines


class PulseType(Enum):
    LOW = 0
    HIGH = 1


@dataclass
class Pulse:
    src: str
    dest: str
    p_type: PulseType
    

@dataclass
class Module:
    id_str : str
    destinations: List[str]
    sources: List[str]
    memory: Dict

    def receive(self, pulse: Pulse):
        return self.transmit(pulse_type=pulse.p_type)

    def transmit(self, pulse_type: PulseType):
        return [Pulse(self.id_str, dest, pulse_type) for dest in self.destinations]


@dataclass
class FlipFlop(Module):
    is_on: bool = False
    def receive(self, pulse:Pulse):
        if pulse.p_type == PulseType.LOW:
            self.is_on = not self.is_on
            return self.transmit(PulseType.HIGH if self.is_on else PulseType.LOW)


@dataclass
class Conjunction(Module):    
    def receive(self, pulse:Pulse):
        self.memory[pulse.src] = pulse.p_type
        any_low = any([v == PulseType.LOW for _k, v in self.memory.items()])
        return self.transmit(PulseType.HIGH if any_low else PulseType.LOW)


class Network:
    def __init__(self, lines):
        self.modules = {}
        for line in lines:
            module, dest_str = line.split('->')
            dest_list =  [dest.strip() for dest in dest_str.split(',')]
            is_flipflop, module_name = module[0] == '%', module[1:].strip()
            if module.strip() == 'broadcaster':
                self.modules['broadcaster'] = Module('broadcaster', dest_list, [], {})
                continue            
            if is_flipflop:
                self.modules[module_name] = FlipFlop(module_name, dest_list, [], {}, False)
            else:
                self.modules[module_name] = Conjunction(module_name, dest_list, [], {})
        
        self.modules['rx'] = Module('rx', [], [], {})
        
        for mod_name, mod in self.modules.items():
            for dest in mod.destinations:                     
                self.modules[dest].memory[mod_name] = PulseType.LOW
                self.modules[dest].sources.append(mod_name)
        return
    

    def press_button(self):        
        self.pulse_buffer = deque([Pulse('button', 'broadcaster', PulseType.LOW)])
        self.pulse_history = []
        low_pulses, hi_pulses = 0,0
        
        while self.pulse_buffer:       
            p = self.pulse_buffer.popleft()
            self.pulse_history.append(p)
            low_pulses += 1 if p.p_type == PulseType.LOW else 0
            hi_pulses += 1 if p.p_type == PulseType.HIGH else 0
            transmits = self.modules[p.dest].receive(p)

            if transmits is not None:
                for tx in transmits:                    
                    self.pulse_buffer.append(tx)
                               
        #low_pulses = sum([1 for p in self.pulse_history if p.p_type == PulseType.LOW])
        #hi_pulses = sum([1 for p in self.pulse_history if p.p_type == PulseType.HIGH])        
        return (low_pulses, hi_pulses)
    
    def spam_button(self, num_button_presses):
        low_counter, hi_counter = 0,0
        for i in range(num_button_presses):
            lo, hi = self.press_button()
            low_counter += lo
            hi_counter += hi
        return low_counter * hi_counter
    
    def cycle_finder(self):        
        rx_feed_name = self.modules['rx'].sources[0]        # Assuming only one module feeds rx
        src_loops = {}       
        
        for src in self.modules[rx_feed_name].sources:
            searching_for_loop, first_low, button_counter = True, None, 0
            while searching_for_loop:
                self.press_button()
                button_counter += 1                
                for p in self.pulse_history:
                    if p.dest == src and p.p_type == PulseType.LOW:
                        if first_low is None:
                            first_low = button_counter
                        else:
                            src_loops[src] = button_counter - first_low
                            searching_for_loop = False

        return reduce(math.lcm, [v for k,v in src_loops.items()]) 


        


        

if __name__ == "__main__":
    filename = r'Yr2023\PuzzleData\Day20.txt'
    #filename = r'Yr2023\PuzzleData\Example.txt'
    lines = get_lines(filename)    
    net = Network(lines)

    part_one = net.spam_button(1000)
    part_two = net.cycle_finder()
    print(f"Part One: {part_one}    Part Two:  {part_two}")
