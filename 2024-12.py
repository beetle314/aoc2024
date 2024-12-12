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
    Example("""AAAA
BBCD
BBCC
EEEC""", "140", "80"),
    Example("""OOOOO
OXOXO
OOOOO
OXOXO
OOOOO""", "772", "436"),
    Example("""EEEEE
EXXXX
EEEEE
EXXXX
EEEEE""", None, "236"),
    Example("""AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA""", None, "368"),
    Example("""RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE""", "1930", "1206"),
]
PROFILE = True


def test_a(data):
    width = data.index("\n") + 1
    height = (len(data) + 1) // width

    unknown_plots = {(x, y) for x in range(width - 1) for y in range(height)}
    queue = collections.deque()

    total_price = 0

    while unknown_plots:
        # Perform flood fill
        x, y = unknown_plots.pop()
        queue.append((x, y))
        visited = {(x, y)}

        perimeter = 0
        area = 0

        while queue:
            x, y = queue.pop()
            char = data[x + y * width]

            area += 1
            perimeter += 4

            for delta in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                nx, ny = x + delta[0], y + delta[1]

                if 0 <= nx < width - 1 and 0 <= ny < height and data[nx + ny * width] == char:
                    perimeter -= 1

                    if (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited.add((nx, ny))

        # Calculate the overal price
        total_price += perimeter * area

        # Update unknown plots
        unknown_plots -= visited

    return total_price


def test_b(data):
    width = data.index("\n") + 1
    height = (len(data) + 1) // width

    data = '\n' * width + data + '\n' * width + '\n'

    unknown_plots = {(x, y) for x in range(width - 1) for y in range(1, height + 1)}
    queue = collections.deque()

    total_price = 0

    while unknown_plots:
        # Perform flood fill
        x, y = unknown_plots.pop()
        queue.append((x, y))
        visited = {(x, y)}

        n_sides = 0
        area = 0

        while queue:
            x, y = queue.pop()
            char = data[x + y * width]
            area += 1

            # Check which cells still need to be visited
            for dx, dy in ((-1, 0), (0, -1), (1, 0), (0, 1)):
                nx, ny = x + dx, y + dy

                if data[nx + ny * width] == char:
                    if (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited.add((nx, ny))

            # Count the number of edges involved
            for dx, dy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                c1 = data[x + dx +  y       * width]
                c2 = data[x      + (y + dy) * width]

                # Check if the corner is convex
                if c1 != char and c2 != char:
                    n_sides += 1

                # Check if the corner is concave
                elif c1 == char and c2 == char and \
                     data[x + dx + (y + dy) * width] != char:
                    n_sides += 1

        # Calculate the overal price
        total_price += n_sides * area

        # Update unknown plots
        unknown_plots -= visited

    return total_price


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

    for ex in puzzle.examples:
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
