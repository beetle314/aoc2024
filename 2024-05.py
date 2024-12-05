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


def parse(data):
    edges, to_print = data.split("\n\n")
    return (
        tuple(e.split("|") for e in edges.splitlines()),
        tuple(s.split(",") for s in to_print.splitlines())
    )


def test_a(data):
    edges, to_print = parse(data)

    result = 0

    for update in to_print:
        valid = True

        for e in edges:
            if e[0] in update and e[1] in update and update.index(e[0]) > update.index(e[1]):
                valid = False

        if valid:
            result += int(update[len(update)//2])

    return result


def top_sort(edges, nodes):
    result = []

    neighbours = {n: [e[1] for e in edges if e[0] == n and e[1] in nodes] for n in nodes}
    num_incoming = {
        n: sum(1 for nb in neighbours.values() if n in nb)
        for n in nodes
    }

    to_visit = collections.deque(n for n, i in num_incoming.items() if i == 0)

    while to_visit:
        n = to_visit.pop()
        result.append(n)

        for m in neighbours[n]:
            num_incoming[m] -= 1
            if num_incoming[m] == 0:
                to_visit.append(m)

    return result


def test_b(data):
    edges, to_print = parse(data)

    result = 0

    for update in to_print:
        # Filter out any valid updates
        valid = True

        for e in edges:
            if e[0] in update and e[1] in update and update.index(e[0]) > update.index(e[1]):
                valid = False

        if valid:
            continue

        # Reorder the other updates
        ordered = top_sort(edges, update)
        result += int(ordered[len(ordered)//2])

    return result


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
