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


def parse(data: str) -> list[tuple[int, int, int, int]]:
    pairs = []

    for line in data.splitlines():
        elf_1, elf_2 = line.split(',')
        pairs.append(tuple(map(int, elf_1.split('-'))) + tuple(map(int, elf_2.split('-'))))

    return pairs  # type: ignore


def test_a(data):
    count = 0

    for pair in parse(data):
        count += (pair[0] <= pair[2] <= pair[3] <= pair[1]) or (pair[2] <= pair[0] <= pair[1] <= pair[3])

    return count


def test_b(data):
    count = 0

    for pair in parse(data):
        count += (pair[0] <= pair[3] and pair[2] <= pair[1])

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
    N = 1000; print(min(timeit.repeat('test_b (puzzle.input_data)', globals=globals(), number=N)) / N)
    # cProfile.runctx('test_b(puzzle.input_data)', globals(), {})


if __name__ == '__main__':
    main()