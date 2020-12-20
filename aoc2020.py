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


def task_2_part_1():
    with open('input2.txt') as f:
        lines = f.readlines()
    class Record(object):
        def __init__(self, line):
            pattern = "(\\d+)-(\\d+) (\\w): (\\w+)"
            match = re.search(pattern, line)
            assert match
            self.rule_min_count = int(match.group(1))
            self.rule_max_count = int(match.group(2))
            self.rule_character = match.group(3)
            self.password = match.group(4)
        def is_valid(self):
            count = self.password.count(self.rule_character)
            return self.rule_min_count <= count and count <= self.rule_max_count
    records = [ Record(line) for line in lines ]
    count = len([record for record in records if record.is_valid()])
    print(count)


def task_2_part_2():
    with open('input2.txt') as f:
        lines = f.readlines()
    class Record(object):
        def __init__(self, line):
            pattern = "(\\d+)-(\\d+) (\\w): (\\w+)"
            match = re.search(pattern, line)
            assert match
            self.rule_index_1 = int(match.group(1))-1
            self.rule_index_2 = int(match.group(2))-1
            self.rule_character = match.group(3)
            self.password = match.group(4)
        def is_valid(self):
            index_1_matches = self.password[self.rule_index_1] == self.rule_character
            index_2_matches = self.password[self.rule_index_2] == self.rule_character
            return index_1_matches != index_2_matches
    records = [ Record(line) for line in lines ]
    count = len([record for record in records if record.is_valid()])
    print(count)


def main():
    #task_1_part_1()
    #task_1_part_2()
    task_2_part_1()
    task_2_part_2()


if __name__ == '__main__':
    main()