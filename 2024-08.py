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
    Example("""T.........
...T......
.T........
..........
..........
..........
..........
..........
..........
..........""", None, '9'),
    Example(puzzle.examples[0].input_data, puzzle.examples[0].answer_a, '34'),
]

# puzzle.view()


def parse(data):
    width = data.index('\n') + 1
    height = (len(data) + 1) // width

    antennae = collections.defaultdict(list)

    for i, c in enumerate(data):
        if c not in '.\n':
            antennae[c].append((i % width, i // width))

    return antennae, width - 1, height

def print_antinodes(data, antinodes):
    width = data.index('\n') + 1

    for coords in antinodes:
        i = width * coords[1] + coords[0]
        data = data[:i] + '#' + data[i + 1:]

    print(data)

def test_a(data):
    antennae, width, height = parse(data)
    nodes = set()

    for key, coords in antennae.items():
        for p1, p2 in itertools.permutations(coords, 2):
            delta = (p1[0] - p2[0], p1[1] - p2[1])
            antinode = (p1[0] + delta[0], p1[1] + delta[1])

            if 0 <= antinode[0] < width and 0 <= antinode[1] < height:
                nodes.add(antinode)

    return len(nodes)


def test_b(data):
    antennae, width, height = parse(data)
    nodes = set()

    for key, coords in antennae.items():
        for p1, p2 in itertools.permutations(coords, 2):
            delta = (p1[0] - p2[0], p1[1] - p2[1])
            antinode = p1

            while 0 <= antinode[0] < width and 0 <= antinode[1] < height:
                nodes.add(antinode)
                antinode = (antinode[0] + delta[0], antinode[1] + delta[1])

    # print_antinodes(data, nodes)
    return len(nodes)


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
