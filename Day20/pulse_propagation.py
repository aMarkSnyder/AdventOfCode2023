from argparse import ArgumentParser
from dataclasses import dataclass
from math import lcm

@dataclass
class Pulse:
    source: str
    dest: str
    value: str

class FlipFlop:
    def __init__(self, name: str) -> None:
        self.name = name
        self.sources = []
        self.dests = []
        self.state = 'off'

    def add_source(self, source: str):
        self.sources.append(source)

    def add_dest(self, dest: str):
        self.dests.append(dest)

    def send(self, value):
        return [Pulse(self.name, dest, value) for dest in self.dests]

    def receive(self, pulse: Pulse):
        if pulse.value == 'high':
            return []
        if self.state == 'off':
            self.state = 'on'
            return self.send('high')
        else:
            self.state = 'off'
            return self.send('low')
        
class Conjunction:
    def __init__(self, name: str) -> None:
        self.name = name
        self.sources = []
        self.dests = []
        self.memory = {}

    def add_source(self, source: str):
        self.sources.append(source)
        self.memory[source] = 'low'

    def add_dest(self, dest: str):
        self.dests.append(dest)

    def send(self, value):
        return [Pulse(self.name, dest, value) for dest in self.dests]

    def receive(self, pulse: Pulse):
        self.memory[pulse.source] = pulse.value
        for remembered_value in self.memory.values():
            if remembered_value == 'low':
                return self.send('high')
        return self.send('low')
    
class Broadcast:
    def __init__(self, name: str) -> None:
        self.name = name
        self.dests = []

    def add_source(self, source: str):
        pass

    def add_dest(self, dest: str):
        self.dests.append(dest)

    def send(self, value):
        return [Pulse(self.name, dest, value) for dest in self.dests]

    def receive(self, pulse: Pulse):
        return self.send(pulse.value)
    
def initialize_modules(data):
    modules = {}
    source_dests = {}
    for line in data:
        source, dests = line.split(' -> ')
        dests = dests.split(', ')
        match source[0]:
            case 'b':
                name = source
                modules[source] = Broadcast(source)
            case '%':
                name = source[1:]
                modules[name] = FlipFlop(name)
            case '&':
                name = source[1:]
                modules[name] = Conjunction(name)
        source_dests[name] = dests

    for source, dests in source_dests.items():
        for dest in dests:
            modules[source].add_dest(dest)
            if dest in modules:
                modules[dest].add_source(source)

    return modules

def main(data):
    modules = initialize_modules(data)

    button_presses = 1000
    total_pulses = {
        'low': 0,
        'high': 0,
    }
    for press in range(button_presses):
        #print(f'Press {press}')
        current_pulses = [Pulse('button', 'broadcaster', 'low')]
        while current_pulses:
            next_pulses = []
            for pulse in current_pulses:
                total_pulses[pulse.value] += 1
                #print(f'{pulse.source} -{pulse.value}-> {pulse.dest}')
                pulse_response = modules[pulse.dest].receive(pulse) if pulse.dest in modules else []
                next_pulses.extend(pulse_response)
            current_pulses = next_pulses
    
    print(total_pulses['low'] * total_pulses['high'])

    modules = initialize_modules(data)

    # By inspection, &lx is the only source of rx
    # it has sources &cl, &rp, &lb, &nj
    # for &lx to send a low, all of its sources need be remembered high at once
    # which probably means they need to pulse high at the same time because based on
    # printouts they do not pulse high very often
    lx_source_pulses = {
        'cl': 0,
        'rp': 0,
        'lb': 0,
        'nj': 0,
    }
    for press in range(1,10**9):
        current_pulses = [Pulse('button', 'broadcaster', 'low')]
        while current_pulses:
            next_pulses = []
            for pulse in current_pulses:
                if pulse.source in lx_source_pulses and pulse.value == 'high' and not lx_source_pulses[pulse.source]:
                    lx_source_pulses[pulse.source] = press
                pulse_response = modules[pulse.dest].receive(pulse) if pulse.dest in modules else []
                next_pulses.extend(pulse_response)
            current_pulses = next_pulses
        if all(lx_source_pulses.values()):
            break

    print(lcm(*lx_source_pulses.values()))

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
