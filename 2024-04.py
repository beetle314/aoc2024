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
    Example("XMAS\naaaa", '1'),
    Example("SAMX\naaaa", '1'),
    Example("aXa\naMa\naAa\naSa", '1'),
    Example("aSa\naAa\naMa\naXa", '1'),
    Example("Xaaa\naMaa\naaAa\naaaS", '1'),
    Example("Saaa\naAaa\naaMa\naaaX", '1'),
    Example("aaaX\naaMa\naAaa\nSaaa", '1'),
    Example("aaaS\naaAa\naMaa\nXaaa", '1'),
    Example("MaM\naAa\nSaS", None, '1'),
    Example("SaM\naAa\nSaM", None, '1'),
    Example("""MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX""", '18', '9')
]


def test_a(data):
    width = data.index('\n') + 1
    height = (len(data) + 1) // width

    count =  0

    for i, c in enumerate(data):
        if c != 'X': continue

        if data[i:i+4] == 'XMAS':       # L to R
            count += 1
        if data[i-3:i+1] == 'SAMX':     # R to L
            count += 1
        if data[i:i+3*width+1:width] == 'XMAS':   # T to B
            count += 1
        if data[i-3*width:i+1:width] == 'SAMX':   # B to T
            count += 1
        if data[i:i+3*width+4:width+1] == 'XMAS':   # TL to BR
            count += 1
        if data[i-3*width-3:i+1:width+1] == 'SAMX':   # BR to TL
            count += 1
        if data[i:i+3*width-2:width-1] == 'XMAS':    # TR to BL
            count += 1
        if data[i-3*width+3:i+1:width-1] == 'SAMX':   # BL to TR
            count += 1

    return count


def test_b(data):
    width = data.index('\n') + 1
    height = (len(data) + 1) // width

    count =  0

    for i, c in enumerate(data):
        if c != 'A': continue

        if data[i-width-1:i+width+2:width+1] in ('MAS', 'SAM') and \
            data[i-width+1:i+width:width-1] in ('MAS', 'SAM'):
            count += 1

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
        assert puzzle.answer_a == guess

    elif ANSWERING:
        puzzle.answer_a = guess
        return

    else:
        return

    # Verify the example for part B
    guess = str(test_b(puzzle.input_data))
    print('Guess B:', guess)

    if puzzle.answered_b:
        assert puzzle.answer_b == guess

    elif ANSWERING:
        puzzle.answer_b = guess

    else:
        return

    # Time to compare some solutions
    # N = 1000; print(min(timeit.repeat('test_b (puzzle.input_data)', globals=globals(), number=N)) / N)
    # N = 1000; print(min(timeit.repeat('test_b2(puzzle.input_data)', globals=globals(), number=N)) / N)
    # N = 1000; print(min(timeit.repeat('test_b3(puzzle.input_data)', globals=globals(), number=N)) / N)
    # cProfile.runctx('test_b3(puzzle.input_data)', globals(), {})


if __name__ == '__main__':
    main()
