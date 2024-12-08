import re
import timeit

from aocd import puzzle
from aocd.examples import Example


ANSWERING = True
EXAMPLES: list[Example] = []

VALUE_MAP = {
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'zero': 0,
} | {str(i): i for i in range(10)}

VALUE_MAP_INV = {k[::-1]: v for k, v in VALUE_MAP.items()}


def test_a(data):
    return sum(
        int(re.search(r"\d", line).group()) * 10
        + int(re.search(r"\d", line[::-1]).group())
        for line in data.splitlines()
    )


def test_b(data):
    return sum(
        VALUE_MAP[re.search("|".join(VALUE_MAP), line).group()] * 10
        + VALUE_MAP_INV[re.search("|".join(VALUE_MAP_INV), line[::-1]).group()]
        for line in data.splitlines()
    )


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
