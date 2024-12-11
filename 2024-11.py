import collections
import cProfile
import functools
import itertools
import math
import timeit
import operator
import pstats
import re

from aocd import puzzle
from aocd.examples import Example

ANSWERING = True
EXAMPLES: list[Example] = [
    # Example("0 1 10 99 999", "7"),  # 1 step: 1 2024 1 0 9 9 2021976
    # Example("125 17", "22"),  # 6 steps: 2097446912 14168 4048 2 0 2 4 40 48 2024 40 48 80 96 2 8 6 7 6 0 3 2
    Example("125 17", "55312"),  # 25 steps
]
PROFILE = True


@functools.cache
def run(number, num_iter):
    if num_iter == 0:
        return 1
    elif number == 0:
        return run(1, num_iter - 1)
    elif not (n := int(math.log10(number)) + 1) % 2:
        split = 10 ** (n/2)
        return run(number // split, num_iter - 1) + run(number % split, num_iter - 1)
    else:
        return run(number * 2024, num_iter - 1)


def test_a(data):
    run.cache_clear()
    return sum(run(int(n), 25) for n in data.split())


def test_b(data):
    run.cache_clear()
    return sum(run(int(n), 75) for n in data.split())


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
    print(f'Guess A: {guess:>10}')

    if puzzle.answered_a:
        assert puzzle.answer_a == guess, puzzle.answer_a

    elif ANSWERING:
        puzzle.answer_a = guess
        return

    else:
        return

    # Verify the example for part B
    guess = str(test_b(puzzle.input_data))
    print(f'Guess B: {guess:>10}')

    if puzzle.answered_b:
        assert puzzle.answer_b == guess, puzzle.answer_b

    elif ANSWERING:
        puzzle.answer_b = guess

    else:
        return

    # Time to compare some solutions
    if PROFILE:
        prof = cProfile.Profile()
        prof.runctx('test_b(puzzle.input_data)', globals(), {})

        stats = pstats.Stats(prof)
        stats.sort_stats('tottime')
        stats.print_stats(10)

        N = 100
        print(min(timeit.repeat('test_b(puzzle.input_data)', globals=globals(), number=N)) / N)


if __name__ == '__main__':
    main()
