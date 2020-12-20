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


def task_4_read_passports(filename):
    with open(filename) as f:
        lines = f.readlines()
    passports = [{}]
    for line in lines:
        fields = line.strip().split()
        if len(fields) == 0:
            passports.append({})
            continue
        for field in fields:
            tokens = field.split(":")
            assert len(tokens) == 2
            assert not tokens[0] in passports[-1]
            passports[-1][tokens[0]] = tokens[1]
    return [p for p in passports if len(p) > 0]


def task_4_validate_height(value_str):
    value = int(value_str[:-2])
    units = value_str[-2:]
    if units == "cm":
        return 150 <= value and value <= 193
    elif units == "in":
        return 59 <= value and value <= 76
    else:
        return False


def task_4_validate_passport(passport, apply_rules=True):
    print()
    ok = True
    optional = ['cid']
    rules = {
        'byr': ["\\d{4}", lambda x: 1920 <= int(x) and int(x) <= 2002 ],
        'iyr': ["\\d{4}", lambda x: 2010 <= int(x) and int(x) <= 2020 ],
        'eyr': ["\\d{4}", lambda x: 2020 <= int(x) and int(x) <= 2030 ],
        'hgt': ["\\d+(cm|in)", task_4_validate_height],
        'hcl': ["#[0-9a-f]{6}", None],
        'ecl': ["amb|blu|brn|gry|grn|hzl|oth", None],
        'pid': ["\\d{9}", None],
        'cid': [None, None]
    }
    for key in rules:

        # Ensure key is in passport unless optional
        if not key in passport:
            if key in optional:
                continue
            else:
                print(key, "missing")
                ok = False
                continue

        # Apply validation rules unless doing quick check
        if not apply_rules:
            continue
        value = passport[key]
        pattern = rules[key][0]
        predicate = rules[key][1]
        matched = True
        if pattern is not None:
            match = re.match(pattern, value)
            if not match:
                print("R", key, ":", pattern, "!=~", value)
                ok = False
                matched = False
            else:
                print("R", key, ":", pattern, "=~", value)
        if matched and predicate is not None:
            if not predicate(value):
                print("P", key, ":", value, "predicate failed")
                ok = False
            else:
                print("P", key, ":", value, "OK")

    # Check for unwanted fields
    for key in passport:
        if not key in rules:
            print(key, "unwanted")
            ok = False

    print(ok)
    return ok



def task_4_part_1():
    passports = task_4_read_passports("input4.txt")
    num_valid = len([p for p in passports if task_4_validate_passport(p, False)])
    assert num_valid == 204
    print(num_valid)


def task_4_part_2():
    passports = task_4_read_passports("input4.txt")
    num_valid = len([p for p in passports if task_4_validate_passport(p)])
    num_invalid = len([p for p in passports if not task_4_validate_passport(p)])
    print(num_valid)
    print(num_invalid)


def main():
    #task_1_part_1()
    #task_1_part_2()
    #task_2_part_1()
    #task_2_part_2()
    #task_3_part_1()
    #task_3_part_2()
    #task_4_part_1()
    task_4_part_2()


if __name__ == '__main__':
    main()