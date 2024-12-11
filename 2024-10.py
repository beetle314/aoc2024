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
EXAMPLES: list[Example] = [
    Example("""0123
1234
8765
9876""", "1"),
    Example(""".....0.
..4321.
..5..2.
..6543.
..7..4.
..8765.
..9....""", None, "3"),
    Example("""89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732""", None, "81")
]

# puzzle.view()


def test_a(data):
    width = data.index('\n')
    data = (' ' * width + '\n') + data + ('\n' + ' ' * width)

    score = 0

    start_i = -1
    while (start_i := data.find('0', start_i + 1)) > -1:
        to_visit = collections.deque({start_i})
        found = set()

        while to_visit:
            i = to_visit.pop()
            value = chr(ord(data[i]) + 1)

            for dir in (-1, -1 - width, 1, width + 1):
                if data[i + dir] == value:
                    if data[i + dir] == '9':
                        found.add(i + dir)
                    else:
                        to_visit.append(i + dir)

        score += len(found)

    return score


def test_b(data):
    width = data.index('\n')
    data = (' ' * width + '\n') + data + ('\n' + ' ' * width)

    score = 0

    start_i = -1
    while (start_i := data.find('0', start_i + 1)) > -1:
        to_visit = collections.deque({start_i})
        score += 1
        print(to_visit)

        while to_visit:
            i = to_visit.pop()
            value = chr(ord(data[i]) + 1)

            for dir in (-1, -1 - width, 1, width + 1):
                if data[i + dir] == value:
                    score += 1
                    if data[i + dir] != '9':
                        to_visit.append(i + dir)

            score -= 1

    return score


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
    N = 1; print(min(timeit.repeat('test_b (puzzle.input_data)', globals=globals(), number=N)) / N)
    cProfile.runctx('test_b(puzzle.input_data)', globals(), {})


if __name__ == '__main__':
    main()
