import bisect
import collections
import cProfile
import itertools
import operator
import timeit

from aocd import puzzle
from aocd.examples import Example

ANSWERING = True
EXAMPLES: list[Example] = [
    Example('3   4\n4   3\n2   5\n1   3\n3   9\n3   3', '11', '31')
]


def parse(data):
    list_1 = []
    list_2 = []

    for line in data.splitlines():
        a, b = map(int, line.split())

        list_1.append(a)
        list_2.append(b)

    return sorted(list_1), sorted(list_2)


def test_a(data):
    data = parse(data)

    return sum(
        abs(a - b)
        for a, b in zip(*data)
    )

def test_b(data):
    list_1, list_2 = parse(data)

    return sum(
        a * list_2.count(a)
        for a in list_1
    )

def test_b1(data):
    list_1, list_2 = parse(data)
    ptr_1, ptr_2 = 0, 0
    result = 0

    while ptr_1 < len(list_1) and ptr_2 < len(list_2):
        if list_1[ptr_1] < list_2[ptr_2]:
            ptr_1 += 1

        elif list_1[ptr_1] > list_2[ptr_2]:
            ptr_2 += 1

        else:
            cnt_2 = 0
            while list_1[ptr_1] == list_2[ptr_2]:
                cnt_2 += 1
                ptr_2 += 1

            i = ptr_1
            cnt_1 = 0

            while ptr_1 < len(list_1) and list_1[i] == list_1[ptr_1]:
                cnt_1 += 1
                ptr_1 += 1

            result += list_1[i] * cnt_2 * cnt_1

    return result

def test_b2(data):
    v1 = collections.defaultdict(int)
    v2 = collections.defaultdict(int)

    for line in data.splitlines():
        a, b = line.split()

        v1[int(a)] += 1
        v2[int(b)] += 1

    return sum(key * num * v2[key] for key, num in v1.items())


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
    N = 100; print(min(timeit.repeat('test_b (puzzle.input_data)', globals=globals(), number=N)) / N)
    N = 100; print(min(timeit.repeat('test_b1(puzzle.input_data)', globals=globals(), number=N)) / N)
    N = 100; print(min(timeit.repeat('test_b2(puzzle.input_data)', globals=globals(), number=N)) / N)
    # cProfile.runctx('test_b(puzzle.input_data)', globals(), {})


if __name__ == '__main__':
    main()
