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
EXAMPLES: list[Example] = [Example("12345", "60"), Example("2333133121414131402", "1928", "2858")]

# puzzle.view()


def test_a(data):
    inp_blocks = collections.deque(itertools.chain.from_iterable(
        (-1 if i % 2 else i//2, ) * int(num)
        for i, num in enumerate(data)
    ))

    checksum, i = 0, 0

    while inp_blocks:
        id_ = inp_blocks.popleft()

        if id_ != -1:
            checksum += id_ * i
            i += 1
        else:
            while inp_blocks and id_ == -1:
                id_ = inp_blocks.pop()

            if id_ != -1:
                checksum += id_ * i
                i += 1

    return checksum


Block = collections.namedtuple('Block', ('pos', 'len', 'id'))
Block.__repr__ = lambda b: str(b.id) * b.len

def test_b(data):
    blocks = []
    free = []

    # Construct the memory representation
    data = '0' + data
    pos = 0

    for i in range(1, len(data), 2):
        blocks.append(Block(
            pos,
            int(data[i - 1]),
            '.',
        ))

        pos += int(data[i - 1])

        blocks.append(Block(
            pos,
            int(data[i]),
            i // 2,
        ))

        pos += int(data[i])

    # Start cleaning up our memory
    for id_ in range(len(data) // 2 - 1, 0, -1):

        # Find block in memory
        for i in range(len(blocks) - 1, 0, -1):
            if blocks[i].id == id_:
                break

        # Check if we can move the block
        for j in range(0, i):
            if blocks[j].id == '.' and blocks[j].len >= blocks[i].len:
                break

        if blocks[j].len >= blocks[i].len:
            b = blocks[i]
            blocks[i] = Block(b.pos, b.len, '.')
            blocks[j] = Block(blocks[j].pos, blocks[j].len - b.len, blocks[j].id)
            blocks.insert(j, b)

    # Calculate the checksum
    checksum = 0
    pos = 0

    for block in blocks:
        if block.id == '.':
            pos += block.len
            continue

        checksum += block.id * block.len * (2 * pos + block.len - 1) // 2
        pos += block.len

    return checksum


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
