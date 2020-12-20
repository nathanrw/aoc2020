import argparse
import re
import functools
import operator

def task_1_part_1():
    with open('input1.txt') as f:
        lines = f.readlines()
    numbers = [ int(line) for line in lines ]
    def get_number(numbers):
        for x in numbers:
            for y in numbers:
                if x + y == 2020:
                    return x*y
        return None
    number = get_number(numbers)
    assert number is not None
    print(number)


def task_1_part_2():
    with open('input1.txt') as f:
        lines = f.readlines()
    numbers = [ int(line) for line in lines ]
    def get_number(numbers):
        for x in numbers:
            for y in numbers:
                for z in numbers:
                    if x + y + z == 2020:
                        return x*y*z
        return None
    number = get_number(numbers)
    assert number is not None
    print(number)


def task_2_read_records():
    with open('input2.txt') as f:
        lines = f.readlines()
    class Record(object):
        def __init__(self, line):
            pattern = "(\\d+)-(\\d+) (\\w): (\\w+)"
            match = re.search(pattern, line)
            assert match
            self.a = int(match.group(1))
            self.b = int(match.group(2))
            self.c = match.group(3)
            self.password = match.group(4)
    return [ Record(line) for line in lines ]


def task_2_part_1():
    def validate(r):
        count = r.password.count(r.c)
        return r.a <= count and count <= r.b
    count = len([r for r in task_2_read_records() if validate(r)])
    print(count)


def task_2_part_2():
    def validate(r):
        return (r.password[r.a-1] == r.c) != (r.password[r.b-1] == r.c)
    count = len([r for r in task_2_read_records() if validate(r)])
    print(count)


def task_3_read_grid():
    with open('input3.txt') as f:
        lines = f.readlines()
    class GridRow(object):
        def __init__(self, line):
            assert len(line) > 0
            self.orig = [c for c in line.strip()]
            self.line = []
            self.set_items = {}
        def __getitem__(self, i):
            while len(self.line) <= i:
                self.line += self.orig
            return self.line[i]
        def __setitem__(self, i, val):
            self.__getitem__(i)
            self.line[i] = val
        def print(self, column):
            self.__getitem__(column)
            print("".join(self.line[:column]))
    class Grid(object):
        def __init__(self, lines):
            self.lines = [ GridRow(l) for l in lines ]
        def __len__(self):
            return len(self.lines)
        def __getitem__(self, j):
            assert 0 <= j and j < len(self)
            return self.lines[j]
        def print(self, column, nrow=-1):
            for row in self.lines[:nrow]:
                row.print(column)
    return Grid(lines)


def task_3_evaluate_slope(dx, dy):
    print("Evaluate slope:", dx, dy)
    grid = task_3_read_grid()
    i = dx
    j = dy
    count = 0
    print("Before: (80x20 subsection)")
    grid.print(80, 20)
    print()
    while j < len(grid):
        if grid[j][i] == '#':
            grid[j][i] = 'X'
            count += 1
        else:
            grid[j][i] = 'O'
        i += dx
        j += dy
    print("After: (80x20 subsection)")
    grid.print(80, 20)
    print("Number of trees hit:", count)
    return count


def task_3_part_1():
    task_3_evaluate_slope(3, 1)


def task_3_part_2():
    slopes = [
        [1, 1],
        [3, 1],
        [5, 1],
        [7, 1],
        [1, 2]
    ]
    hit_counts = [task_3_evaluate_slope(slope[0], slope[1]) for slope in slopes]
    result = functools.reduce(operator.mul, hit_counts, 1)
    print("Result:", result)


def main():
    #task_1_part_1()
    #task_1_part_2()
    #task_2_part_1()
    #task_2_part_2()
    task_3_part_1()
    task_3_part_2()


if __name__ == '__main__':
    main()