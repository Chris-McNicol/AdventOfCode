from time import perf_counter_ns
from enum import IntEnum

class RPS(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class OUTCOME(IntEnum):
    WIN = 6
    DRAW = 3
    LOSE = 0

move_map = {'A':RPS.ROCK, 'B':RPS.PAPER, 'C': RPS.SCISSORS,
            'X':RPS.ROCK, 'Y':RPS.PAPER, 'Z':RPS.SCISSORS}

win_map = {RPS.ROCK:RPS.SCISSORS, RPS.PAPER:RPS.ROCK, RPS.SCISSORS:RPS.PAPER}

lose_map = {RPS.SCISSORS:RPS.ROCK, RPS.ROCK:RPS.PAPER, RPS.PAPER:RPS.SCISSORS}

outcome_map = {'X':OUTCOME.LOSE, 'Y':OUTCOME.DRAW, 'Z':OUTCOME.WIN}


def strategy_score(opponent_move, my_move):
    """Calculate score assuming 2nd column is my move"""
    result_score = my_move
    if opponent_move == my_move:               #Draw
        result_score += OUTCOME.DRAW
    elif win_map[my_move] == opponent_move:    #Win
        result_score += OUTCOME.WIN
    return result_score


def outcome_score(opponent_move, outcome_required):
    """Calculate score assuming 2nd column is outcome required"""
    result_score = outcome_required
    if outcome_required == OUTCOME.DRAW:
        result_score += opponent_move
    elif outcome_required == OUTCOME.LOSE:
        result_score += win_map[opponent_move]
    else:
        result_score += lose_map[opponent_move]
    return result_score


def calculate_score(filename, outcome_method=False):
    """Calculate score using one of two methods"""
    score_counter = 0
    with open(filename, 'r') as file:
        for line in file:
            # I'm not thrilled with using magic numbers for indices, not very robust if input is wrong
            #moves = [move_map[move] for move in line.replace('\n','').split(' ')]
            if outcome_method:                
                opponent_move, outcome_required = move_map[line[0]], outcome_map[line[2]]
                score_counter += outcome_score(opponent_move, outcome_required)            
            else:
                opponent_move, my_move = move_map[line[0]], move_map[line[2]]
                score_counter += strategy_score(opponent_move, my_move)
    return score_counter


if __name__ == "__main__":
    time_start = perf_counter_ns()
    file_loc = r"C:\Users\Chris\Documents\CodeProjects\AdventOfCode\Yr2022\PuzzleData\puzzle_day_two.txt"
    print(calculate_score(file_loc, True))
    print(f"Elapsed time : {(perf_counter_ns() - time_start)/1000:.0f} microseconds")
