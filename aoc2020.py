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


def task_5_decode_seat_id(code):
    assert len(code) == 10
    row_code = code[:7]
    column_code = code[7:]
    assert len(row_code) == 7
    def decode_bsp(code, l, r, min, max):
        assert len(l) == 1
        assert len(r) == 1
        assert code.count(l) + code.count(r) == len(code)
        if len(code) == 0:
            assert min == max
            return min
        assert min != max
        c = code[0]
        rest = code[1:]
        if c == l:
            return decode_bsp(rest, l, r, min, (min+max)//2)
        elif c == r:
            return decode_bsp(rest, l, r, (min+max)//2+1, max)
        else:
            assert False
    column = decode_bsp(column_code, 'L', 'R', 0, 7)
    row = decode_bsp(row_code, 'F', 'B', 0, 127)
    seat_id = row * 8 + column
    return seat_id


def task_5_read_seat_ids():
    with open('input5.txt') as f:
        lines = f.readlines()
    return [ task_5_decode_seat_id(line.strip()) for line in lines ]


def task_5_part_1():
    ids = task_5_read_seat_ids()
    highest = sorted(ids)[-1]
    assert highest == 953
    print(highest)


def task_5_part_2():
    my_seat = None
    ids = sorted(task_5_read_seat_ids())
    for i in range(len(ids)-1):
        if ids[i] != ids[i+1]-1:
            my_seat = ids[i]+1
            break
    print(my_seat)
    assert my_seat == 615


def task_6_read_groups():
    with open('input6.txt') as f:
        lines = f.readlines()
    class Group(object):
        def __init__(self):
            self.answers = {}
            self.count = 0
    groups = [Group()]
    for line in lines:
        chars = line.strip()
        if len(chars) == 0:
            groups.append(Group())
            continue
        groups[-1].count += 1
        for char in chars:
            count = groups[-1].answers.get(char, 0)
            groups[-1].answers[char] = count+1
    return [ g for g in groups if g.count > 0 ]


def task_6_part_1():
    groups = task_6_read_groups()
    count = sum([ len(g.answers) for g in groups ])
    assert count == 6799
    print(count)


def task_6_part_2():
    groups = task_6_read_groups()
    count = sum([len([k for k in g.answers if g.answers[k] == g.count]) for g in groups])
    print(count)
    assert count == 3354


def task_7_read_rules():
    with open('input7.txt') as f:
        lines = f.readlines()
    def parse_rule(line):
        class Rule(object):
            def __init__(self, colour, contents):
                self.colour = colour
                self.contents = contents
        comma_split = line.split(",")
        contain_split = comma_split[0].split("contain")
        container_str = contain_split[0]
        contents_strs = [contain_split[1]] + comma_split[1:]
        container_tokens = container_str.split()
        container_colour = " ".join(container_tokens[:2])
        contents = {}
        for contents_str in contents_strs:
            contents_tokens = contents_str.split()
            if contents_tokens[0] == "no":
                continue
            contents_count = int(contents_tokens[0])
            contents_colour = " ".join(contents_tokens[1:3])
            contents[contents_colour] = contents_count
        return Rule(container_colour, contents)
    return [ parse_rule(line) for line in lines ]


def task_7_find_possible_containers(rules, colour, seen=set()):
    direct_parents = [ r.colour for r in rules if colour in r.contents ]
    for c in direct_parents:
        if c in seen: continue
        print(c)
        seen.add(c)
        task_7_find_possible_containers(rules, c, seen)
    return seen


def task_7_count_contents(rules, colour):
    rules_for_colour = [ r for r in rules if r.colour == colour ]
    assert len(rules_for_colour) == 1
    rule = rules_for_colour[0]
    count = 0
    for content_colour in rule.contents:
        n = rule.contents[content_colour]
        count += n * (1 + task_7_count_contents(rules, content_colour))
    return count


def task_7_part_1():
    rules = task_7_read_rules()
    containers = task_7_find_possible_containers(rules, "shiny gold")
    answer = len(containers)
    assert answer == 246
    print(answer)


def task_7_part_2():
    rules = task_7_read_rules()
    answer = task_7_count_contents(rules, "shiny gold")
    print(answer)
    assert answer == 2976

def main():
    #task_1_part_1()
    #task_1_part_2()
    #task_2_part_1()
    #task_2_part_2()
    #task_3_part_1()
    #task_3_part_2()
    #task_4_part_1()
    #task_4_part_2()
    #task_5_part_1()
    #task_5_part_2()
    #task_6_part_1()
    #task_6_part_2()
    task_7_part_1()
    task_7_part_2()


if __name__ == '__main__':
    main()