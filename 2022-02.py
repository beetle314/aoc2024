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
EXAMPLES: list[Example] = []

# puzzle.view()


def parse(data):
    return tuple(tuple(match.split()) for match in data.splitlines())


def test_a(data):
    SCORES = {"X": 1, "Y": 2, "Z": 3}
    OUTCOMES = {
        #   Rock          Paper         Scissors
        ("A", "X"): 3, ("A", "Y"): 6, ("A", "Z"): 0,    # Rock
        ("B", "X"): 0, ("B", "Y"): 3, ("B", "Z"): 6,    # Paper
        ("C", "X"): 6, ("C", "Y"): 0, ("C", "Z"): 3,    # Scissors
    }

    return sum(SCORES[match[1]] + OUTCOMES[match] for match in parse(data))


def test_b(data):
    OUTCOMES = {
        #   Lose          Draw           Win
        ("A", "X"): 3, ("A", "Y"): 4, ("A", "Z"): 8,    # Rock
        ("B", "X"): 1, ("B", "Y"): 5, ("B", "Z"): 9,    # Paper
        ("C", "X"): 2, ("C", "Y"): 6, ("C", "Z"): 7,    # Scissors
    }

    return sum(OUTCOMES[match] for match in parse(data))


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
    N = 1000; print(min(timeit.repeat('test_b (puzzle.input_data)', globals=globals(), number=N)) / N)
    # cProfile.runctx('test_b(puzzle.input_data)', globals(), {})


if __name__ == '__main__':
    main()
