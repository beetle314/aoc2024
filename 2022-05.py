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

Move = collections.namedtuple('Move', ('num', 'start', 'end'))


def parse(data: str) -> tuple[list[collections.deque[str]], list[Move]]:
    state_block, moves_block = data.split('\n\n')

    line_len = state_block.index('\n') + 1

    state = [
        collections.deque(
            itertools.filterfalse(
                ' '.__eq__,
                map(
                    state_block.__getitem__,
                    range(i, len(state_block) - line_len + 1, line_len),
                ),
            ),
        )
        for i in range(1, line_len, 4)
    ]

    moves = []
    for line in moves_block.splitlines():
        _, num, _, start, _, end = line.split()
        moves.append(Move(int(num), int(start), int(end)))

    return state, moves


def test_a(data):
    state, moves = parse(data)

    for (num, start, end) in moves:
        state[end - 1].extendleft(state[start - 1].popleft() for _ in range(num))

    return ''.join(col[0] for col in state)


def test_b(data):
    state, moves = parse(data)

    for (num, start, end) in moves:
        state[end - 1].extendleft(reversed([state[start - 1].popleft() for _ in range(num)]))

    return ''.join(col[0] for col in state)


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
