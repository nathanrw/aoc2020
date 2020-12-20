import argparse
import re

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


def main():
    #task_1_part_1()
    #task_1_part_2()
    task_2_part_1()
    task_2_part_2()


if __name__ == '__main__':
    main()