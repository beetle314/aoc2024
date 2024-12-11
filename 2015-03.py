import collections
import itertools
import operator
import re

from aocd import puzzle
from aocd.examples import Example

ANSWERING = True
EXAMPLES: list[Example] = []


def test_a(data):
    pos = 0 + 0j
    visited = {pos}

    for char in data:
        match char:
            case '^': pos -= 1j
            case 'v': pos += 1j
            case '>': pos += 1
            case '<': pos -= 1

        visited.add(pos)

    return len(visited)


def test_b(data):
    pos = [0 + 0j, 0 + 0j]
    turn = 0
    visited = {pos[0]}

    for char in data:
        match char:
            case '^': pos[turn] -= 1j
            case 'v': pos[turn] += 1j
            case '>': pos[turn] += 1
            case '<': pos[turn] -= 1

        visited.add(pos[turn])
        turn = (turn + 1) % 2

    return len(visited)


def main():
    # Open the problem if it hasn't been solved yet
    if not puzzle.prose0_path.exists():
        puzzle.view()
        puzzle.examples  # Forces the download of our prose
        return
 
    # Insert examples if they failed to parse proper
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
    # N = 1; print(min(timeit.repeat('test_b (puzzle.input_data)', globals=globals(), number=N)) / N)
    # cProfile.runctx('test_b(puzzle.input_data)', globals(), {})


if __name__ == '__main__':
    main()
