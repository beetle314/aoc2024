import collections
import re
import timeit

from aocd import puzzle
from aocd.examples import Example


ANSWERING = True
EXAMPLES: list[Example] = []


def parse(data) -> list[list[dict[str, int]]]:
    games: list[list[dict[str, int]]] = []

    for game in data.splitlines():
        games.append([])
        for draw in game.split(': ', 1)[1].split('; '):
            games[-1].append(collections.defaultdict(int))
            for p in draw.split(", "):
                num, clr = p.split(" ")
                games[-1][-1][clr] = int(num)

    return games


def test_a(data):
    games = parse(data)
    result = 0

    for id, game in enumerate(games, 1):
        if all(draw['red'] <= 12 and draw['green'] <= 13 and draw['blue'] <= 14 for draw in game):
            result += id

    return result


def test_b(data):
    games = parse(data)

    return sum(
        max(d['red'] for d in game)
        * max(d['green'] for d in game)
        * max(d['blue'] for d in game)
        for game in games
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
