import collections
import cProfile
import hashlib
import itertools
import timeit
import operator
import pstats
import re

from aocd import puzzle
from aocd.examples import Example

ANSWERING = True
EXAMPLES: list[Example] = []
PROFILE = True


def test_a(data):
    for i in itertools.count(1):
        guess = hashlib.md5((data + str(i)).encode("utf-8")).hexdigest()

        if guess.startswith("00000"):
            return i


def test_b(data):
    for i in itertools.count(1):
        guess = hashlib.md5((data + str(i)).encode("utf-8")).hexdigest()

        if guess.startswith("000000"):
            return i


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
