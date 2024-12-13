"""
min  3 a + b
s.t.        a            <= 100
                       b <= 100
     c[a,x] a + c[b,x] b  = x
     c[a,y] a + c[b,y] b  = y
"""
import collections

from aocd.examples import Example

EXAMPLES: list[Example] = [
    Example("""Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279""", "480")
]

Machine = collections.namedtuple("Machine", ("da", "db", "loc"))


def parse(data: str) -> list[Machine]:
    machines = []

    for machine in data.split("\n\n"):
        a_line, b_line, prize_line = machine.splitlines()

        delta_a = tuple(int(c[2:]) for c in a_line[10:].split(", "))
        delta_b = tuple(int(c[2:]) for c in b_line[10:].split(", "))
        prize_loc = tuple(int(c[2:]) for c in prize_line[7:].split(", "))

        machines.append(Machine(delta_a, delta_b, prize_loc))

    return machines


def part_a(data: str) -> int:
    machines = parse(data)

    soln = 0

    for m in machines:
        # First check if A and B are muliples of each other. This would mean
        # that our second constraint is actually dependent on the first. So
        # we have infinitely many soln's.
        is_indep = (m.da[0] * m.db[1] != m.da[1] * m.db[0])

        # If the two are independent, there's at most one way to get to our
        # prize. So we don't need to do anything clever.
        if is_indep:
            # Note: we round to prevent floating-point issues. This does mean
            #       that we need to double-check if the solution is a proper
            #       integer one.
            a = (m.loc[0] * m.db[1] - m.loc[1] * m.db[0]) // (m.da[0] * m.db[1] - m.da[1] * m.db[0])
            b = (m.loc[1] * m.da[0] - m.loc[0] * m.da[1]) // (m.da[0] * m.db[1] - m.da[1] * m.db[0])

            if m.da[0] * a + m.db[0] * b != m.loc[0]:
                # There is no solution available
                continue

            # Add in our a, b <= 100 constraints
            if a > 100 or b > 100:
                continue

            soln += 3 * a + b

        else:
            # Turns out, no machines in our data belong here. So we can skip on
            # the slightly more complex case of there being infinitely many
            # solutions.
            pass

    return soln


def part_b(data: str) -> int:
    machines = parse(data)

    soln = 0

    for m in machines:
        m = Machine(m.da, m.db, (m.loc[0] + 10000000000000, m.loc[1] + 10000000000000))

        # First check if A and B are muliples of each other. This would mean
        # that our second constraint is actually dependent on the first. So
        # we have infinitely many soln's.
        is_indep = (m.da[0] * m.db[1] != m.da[1] * m.db[0])

        # If the two are independent, there's at most one way to get to our
        # prize. So we don't need to do anything clever.
        if is_indep:
            # Note: we round to prevent floating-point issues. This does mean
            #       that we need to double-check if the solution is a proper
            #       integer one.
            a = (m.loc[0] * m.db[1] - m.loc[1] * m.db[0]) // (m.da[0] * m.db[1] - m.da[1] * m.db[0])
            b = (m.loc[1] * m.da[0] - m.loc[0] * m.da[1]) // (m.da[0] * m.db[1] - m.da[1] * m.db[0])

            if m.da[0] * a + m.db[0] * b != m.loc[0]:
                # There is no solution available
                continue

            soln += 3 * a + b

        else:
            # Turns out, no machines in our data belong here. So we can skip on
            # the slightly more complex case of there being infinitely many
            # solutions.
            pass

    return soln
