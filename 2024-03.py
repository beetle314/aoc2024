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
    # Example('xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))', '161', '161'),
    Example('xmul(2,4)&mul[3,7]!^don\'t()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))', None, '48'),
    Example('xmul(2,4)&mul[3,7]!^don\'t()_mul(5,5)+mul(32,64]do()(mul(11,8)undo()?mul(8,5))', None, '136')
]


def test_a(data):
    return sum(
        int(match[0]) * int(match[1])
        for match in re.findall(r'mul\((\d{1,3}),(\d{1,3})\)', data)
    )

def test_b(data):   # 0.000304
    i = data.find('don\'t()')
    while i != -1:
        j = data.find('do()', i)
        data = data[:i] + data[j:]
        i = data.find('don\'t()')

    return test_a(data)

def test_b2(data):  # 0.000287
    total = 0

    i = 0
    while i != -1:
        j = data.find('don\'t()', i)
        total += test_a(data[i:j])
        i = data.find('do()', j)

    return total

def test_b3(data):  # 0.
    total = 0

    i = 0
    data += '\000'
    enabled = True

    while data[i] != '\000':
        if data[i] == 'd' and data[i:i+4] == 'do()':
            enabled = True
            i += 4

        elif data[i] == 'd' and data[i:i+7] == 'don\'t()':
            enabled = False
            i += 7

        elif enabled and data[i] == 'm' and data[i:i+4] == 'mul(':
            # Parse first number
            for j in range(i + 4, i + 8):
                if not data[j].isdigit():
                    break

            d1 = data[i + 4:j]
            i = j

            # Parse the comma
            if data[i] != ',':
                continue

            # Parse the second number
            for j in range(i + 1, i + 5):
                if not data[j].isdigit():
                    break

            d2 = data[i + 1:j]
            i = j

            # Parse the closing hook
            if data[i] != ')':
                continue

            total += int(d1) * int(d2)
            i += 1

        else:
            i += 1

    return total


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

        if puzzle.answer_b:
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
    N = 1000; print(min(timeit.repeat('test_b (puzzle.input_data)', globals=globals(), number=N)) / N)
    N = 1000; print(min(timeit.repeat('test_b2(puzzle.input_data)', globals=globals(), number=N)) / N)
    N = 1000; print(min(timeit.repeat('test_b3(puzzle.input_data)', globals=globals(), number=N)) / N)
    # cProfile.runctx('test_b3(puzzle.input_data)', globals(), {})


if __name__ == '__main__':
    main()
