from time import perf_counter_ns
from dataclasses import dataclass
from typing import Deque, Union
from collections import deque
from tqdm import tqdm


def cmd_eval(old, eval_str):
    return eval(eval_str)


@dataclass
class Item:
    init_val: int
    def setup(self, divisor_list):
        self.remainders = {k : self.init_val % k for k in divisor_list}
    def reduce(self, divisor_list):
        self.remainders = { k: self.remainders[k] % k for k in divisor_list}
    def eval(self, eval_str):
        self.remainders = {k:cmd_eval(old, eval_str) for k,old in self.remainders.items()}    
    def is_divisible_by(self, divisor):
        return True if self.remainders[divisor] == 0 else False


@dataclass
class Monkey:
    items: Deque[Union[Item, int]]
    op_str: str
    divisor: int
    true_tgt: int
    false_tgt: int
    inspect_ctr: int = 0
    
    def setup(self, divisor_list):
        for item in self.items:
            if isinstance(item, Item):
                item.setup(divisor_list)

    def inspect_and_reduce(self, divisor_list, item):
        item.eval(self.op_str)
        item.reduce(divisor_list)
        tgt = self.true_tgt if item.is_divisible_by(self.divisor) else self.false_tgt
        return tgt, item

    def inspect_and_divide(self, item, reduction=3):
        item = cmd_eval(item, self.op_str) // reduction
        tgt = self.true_tgt if item % self.divisor == 0 else self.false_tgt
        return tgt, item

    def inspect(self, divisor_list):
        self.inspect_ctr += 1
        item = self.items.popleft()
        if isinstance(item, int):
            return self.inspect_and_divide(item)          ### Part One
        else:
            return self.inspect_and_reduce(divisor_list, item)  ### Part Two


def simulate_round(monkey_dict, divisor_list):
    for _monkey_idx, monkey in monkey_dict.items():
        for item_idx in range(0, len(monkey.items)):
            tgt, val = monkey.inspect(divisor_list)
            monkey_dict[tgt].items.append(val)


def simulate_monkeys(monkey_dict, num_rounds):
    divisor_list = [monkey.divisor for _,monkey in monkey_dict.items()]
    for _, monkey in monkey_dict.items():
        monkey.setup(divisor_list)
    for _i in tqdm(range(0, num_rounds)):
        simulate_round(monkey_dict, divisor_list)


def study_monkeys(monkey_dict):
    activities = sorted([monkey.inspect_ctr for _,monkey in monkey_dict.items()])
    return activities[-1] * activities[-2]


def build_monkey(cmd_lines, part_one):
    m_id = int(cmd_lines[0][-3])
    item_list = [int(x) for x in cmd_lines[1].strip().split(':')[-1].split(',')]
    op_str = cmd_lines[2].strip().split('=')[-1]
    div = int(cmd_lines[3].strip().split(' ')[-1])
    tr_tgt = int(cmd_lines[4].strip().split(' ')[-1])
    f_tgt = int(cmd_lines[5].strip().split(' ')[-1])
    if part_one:
        return m_id, Monkey(deque(item_list), op_str, div, tr_tgt, f_tgt)
    else:
        return m_id, Monkey(deque([Item(x) for x in item_list]), op_str, div, tr_tgt, f_tgt)


def load_monkeys(filename: str, part_one=True):
    cmd_lines = []
    monkey_dict = {}
    with open(filename, 'r') as file:
        cmd_lines = file.readlines()    
    for line_idx in range(0, len(cmd_lines), 7):
        k, v = build_monkey( cmd_lines[line_idx:line_idx+7], part_one)
        monkey_dict[k] = v
    return monkey_dict
     

if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_eleven.txt"
    
    part_one = False
    monkey_dict = load_monkeys(file_loc, part_one)
    if part_one:
        simulate_monkeys(monkey_dict, 20)
    else:
        simulate_monkeys(monkey_dict, 10000)
    monkey_business = study_monkeys(monkey_dict)
    
    print (f"Level of monkey business: {monkey_business}")       
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")


