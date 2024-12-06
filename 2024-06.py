import bisect
import collections
import cProfile
import itertools
import operator
import re
import timeit

from aocd import puzzle
from aocd.examples import Example

ANSWERING = True
EXAMPLES: list[Example] = [Example(puzzle.examples[0].input_data, "41", "6")]


def parse(data):
    width = data.index('\n') + 1
    height = (len(data) + 1) // width

    start_pos = data.index('^')
    start_pos = (start_pos % width, start_pos // width)

    obsts = set()
    i = data.find('#')
    while i != -1:
        obsts.add((i % width, i // width))
        i = data.find('#', i + 1)

    return start_pos, obsts, width, height

def print_(data, pos):
    data = data.replace('^', '.').replace('.', ' ')
    width = data.index('\n') + 1
    i = pos[0] + pos[1] * width
    data = (data[:i] + '^' + data[i + 1:])
    # print('=' * width, data[i - width * 3:i + width * 3], '=' * width, sep='\n')
    print(data)
    input()


def get_visited_pos(pos, obsts, width, height):
    aim = (0, -1)
    visited = set()

    while 0 < pos[0] < width - 1 and 0 < pos[1] < height:
        visited.add(pos)
        # print_(data, pos)
        new_pos = (pos[0] + aim[0], pos[1] + aim[1])
        if new_pos in obsts:
            aim = (-aim[1], aim[0])
        else:
            pos = new_pos

    return visited

def test_a(data):
    return len(get_visited_pos(*parse(data)))


def is_loop(pos, obsts, width, height, aim=(0, -1)) -> bool:
    states = set()

    while 0 < pos[0] < width - 1 and 0 < pos[1] < height:
        if pos + aim in states:
            return True
        states.add(pos + aim)

        new_pos = (pos[0] + aim[0], pos[1] + aim[1])
        if new_pos in obsts:
            aim = (-aim[1], aim[0])
        else:
            pos = new_pos

    else:
        return False

def test_b(data):
    pos, obsts, width, height = parse(data)
    visited = get_visited_pos(pos, obsts, width, height)
    count = 0

    for new_obst in visited:
        count += is_loop(pos, obsts | {new_obst}, width, height)

    return count


def main():
    # Insert examples if they failed to parse properly
    # or we see obvious gaps in the test cases
    if EXAMPLES:
        puzzle._get_examples = lambda: EXAMPLES

    # Verify all examples before continuing
    for ex in puzzle.examples:
        if ex.answer_a:
            guess = str(test_a(ex.input_data))
            print(f'Example A:  Expected {ex.answer_a:>10}    Got {guess:>10}')
            if guess != ex.answer_a:
                print(ex.input_data)
                return

        if ex.answer_b:
            guess = str(test_b(ex.input_data))
            print(f'Example B:  Expected {ex.answer_b:>10}    Got {guess:>10}')
            if guess != ex.answer_b:
                print(ex.input_data)
                return

    # Verify the example for part A
    guess = str(test_a(puzzle.input_data))
    print('Guess A:', guess)

    if puzzle.answered_a:
        assert puzzle.answer_a == guess, puzzle.answer_a

    elif ANSWERING:
        puzzle.answer_a = guess
        return

    else:
        return

    # Verify the example for part B
    guess = str(test_b(puzzle.input_data))
    print('Guess B:', guess)

    if puzzle.answered_b:
        assert puzzle.answer_b == guess, puzzle.answer_b

    elif ANSWERING:
        puzzle.answer_b = guess

    else:
        return

    # Time to compare some solutions
    # N = 1000; print(min(timeit.repeat('test_b (puzzle.input_data)', globals=globals(), number=N)) / N)
    # cProfile.runctx('test_b(puzzle.input_data)', globals(), {})


if __name__ == '__main__':
    main()
