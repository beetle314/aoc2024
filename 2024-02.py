import bisect
import collections
import cProfile
import itertools
import operator
import timeit

from aocd import puzzle
from aocd.examples import Example

ANSWERING = True
EXAMPLES: list[Example] = []


def parse(data):
    result = []

    for line in data.splitlines():
        result.append(list(map(int, line.split())))

    return result


def test_a(data):
    data = parse(data)
    cnt = 0

    for report in data:
        if report[1] < report[0]:
            report.reverse()

        for i in range(1, len(report)):
            if 3 < report[i] - report[i - 1] or 1 > report[i] - report[i - 1]:
                # print(report, i, report[i] - report[i - 1])
                safe = False
                break

        else:
            cnt += 1

    return cnt

def is_safe(report):
    if report[1] < report[0]:
        report.reverse()

    for i in range(1, len(report)):
        if 3 < report[i] - report[i - 1] or 1 > report[i] - report[i - 1]:
            break

    else:
        return True

    return False

def test_b(data):
    data = parse(data)
    cnt = 0

    for report in data:
        if is_safe(report):
            cnt += 1

        elif any(is_safe(report[:i] + report[i + 1:]) for i in range(len(report))):
            cnt += 1

    return cnt


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
                return

        if puzzle.answer_b:
            guess = str(test_b(ex.input_data))
            print(f'Example B:  Expected {ex.answer_b:>10}    Got {guess:>10}')
            if guess != ex.answer_b:
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

    elif ANSWERING and not puzzle.answered_b:
        puzzle.answer_b = guess

    else:
        return

    # Time to compare some solutions
    # N = 100; print(min(timeit.repeat('test_b (puzzle.input_data)', globals=globals(), number=N)) / N)
    # cProfile.runctx('test_b(puzzle.input_data)', globals(), {})


if __name__ == '__main__':
    main()
