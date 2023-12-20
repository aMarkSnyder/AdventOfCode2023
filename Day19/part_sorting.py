from argparse import ArgumentParser
from dataclasses import dataclass
import re
import copy

def all_ints(s):
    return [int(i) for i in re.findall(r'\b\d+\b', s)]

@dataclass
class Part:
    x: int
    m: int
    a: int
    s: int

    def get_val(self, letter):
        match letter:
            case 'x': return self.x
            case 'm': return self.m
            case 'a': return self.a
            case 's': return self.s

    def value(self):
        return self.x + self.m + self.a + self.s

class Step:
    def __init__(self, string) -> None:
        if ':' not in string:
            self.terminal = True
            self.condition = lambda x: True
            self.simple_condition = lambda x: True
            self.dest = string
            self.val = 'x'
            self.comparator = '>'
            self.test_val = 0
        else:
            self.terminal = False
            condition, dest = string.split(':')
            self.dest = dest

            self.val = condition[0]
            self.comparator = condition[1]
            self.test_val = int(condition[2:])

            match self.comparator:
                case '>':
                    self.condition = lambda part: part.get_val(self.val) > self.test_val
                    self.simple_condition = lambda num: num > self.test_val
                case '<':
                    self.condition = lambda part: part.get_val(self.val) < self.test_val
                    self.simple_condition = lambda num: num < self.test_val


class Workflow:
    def __init__(self, string) -> None:
        name, steps = string.split('{')
        self.name = name

        steps = steps[:-1]
        steps = steps.split(',')

        self.steps = []
        for step in steps:
            self.steps.append(Step(step))

    def destination(self, part: Part):
        for step in self.steps:
            if step.condition(part):
                return step.dest
        return None


def count_accepted(workflows, current_workflow, current_ranges):
    accepted = []
    for current_range in current_ranges.values():
        if len(current_range) == 0:
            return 0
    if current_workflow == 'R':
        return 0
    if current_workflow == 'A':
        total = 1
        for current_range in current_ranges.values():
            total *= len(current_range)
        return total
    for step in workflows[current_workflow].steps:
        current_range = current_ranges[step.val]
        # The entire current range of the value under test might wind up taking the same path
        if step.test_val not in current_range or step.test_val == current_range[0] or step.test_val == current_range[-1]:
            # Either it all meets the condition and we go there instead or nothing meets it and we continue without changes
            if step.simple_condition(current_ranges[step.val][0]):
                child_current_ranges = copy.copy(current_ranges)
                accepted.append(count_accepted(workflows, step.dest, child_current_ranges))
                break
        # Otherwise some of it continues in this workflow and some of it goes to the child workflow
        else:
            match step.comparator:
                case '>':
                    continuing_range = range(current_range.start, step.test_val+1)
                    child_range = range(step.test_val+1, current_range.stop)
                case '<':
                    child_range = range(current_range.start, step.test_val)
                    continuing_range = range(step.test_val, current_range.stop)
            child_current_ranges = copy.copy(current_ranges)
            child_current_ranges[step.val] = child_range
            accepted.append(count_accepted(workflows, step.dest, child_current_ranges))
            current_ranges[step.val] = continuing_range
    return sum(accepted)

def main(data):
    workflows = {}
    for idx, line in enumerate(data):
        if line == '':
            break
        workflow = Workflow(line)
        workflows[workflow.name] = workflow

    parts = []
    for line in data[idx+1:]:
        parts.append(Part(*all_ints(line)))

    endpoint = {
        'A': [],
        'R': [],
    }
    for part in parts:
        dest = 'in'
        while dest not in ['A', 'R']:
            dest = workflows[dest].destination(part)
        endpoint[dest].append(part)

    total_value = 0
    for part in endpoint['A']:
        total_value += part.value()
    print(total_value)

    starting_ranges = {
        'x': range(1, 4001),
        'm': range(1, 4001),
        'a': range(1, 4001),
        's': range(1, 4001),
    }
    print(count_accepted(workflows, 'in', starting_ranges))

def read_input(input_file):
    data = []
    with open(input_file, 'r') as input:
        for line in input:
            data.append(line.strip())
    return data

if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('input_file', nargs='?', default='input.txt')
    args = parser.parse_args()
    data = read_input(args.input_file)
    main(data)
