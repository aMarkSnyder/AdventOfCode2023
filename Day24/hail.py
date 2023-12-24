from argparse import ArgumentParser
from dataclasses import dataclass
from sympy import symbols, solve
import re

def all_ints(s):
    return [int(i) for i in re.findall(r'-?\d+', s)]

@dataclass(frozen=True)
class Hailstone:
    px: int
    py: int
    pz: int
    vx: int
    vy: int
    vz: int

    def pos(self, t):
        return [p + v*t for p,v in ((self.px,self.vx), (self.py,self.vy), (self.pz,self.vz))]
    
    def time(self, x):
        return (x - self.px) / self.vx
    
@dataclass(frozen=True)
class Point:
    x: int
    y: int
    z: int
    t: int

def find_intersection(hail1: Hailstone, hail2: Hailstone):
    # x = px + vx * t
    # y = py + vy * t
    # z = pz + vz * t
    # t = (x - px) / vx = (y - py) / vy = (z - pz) / vz
    # y = py + vy * (x - px) / vx
    # y = py + vy/vx * x - vy/vx * px
    # -vy/vx * x + y = py - vy/vx * px
    # A1*x + B1*y = C1
    # A2*x + B2*y = C2
    # x = (C1*B2 - C2*B1) / (A1*B2 - A2*B1)
    # y = (A1*C2 - A2*C1) / (A1*B2 - A2*B1)

    a1 = -hail1.vy/hail1.vx
    a2 = -hail2.vy/hail2.vx
    b1, b2 = 1, 1
    c1 = hail1.py - hail1.px * hail1.vy / hail1.vx
    c2 = hail2.py - hail2.px * hail2.vy / hail2.vx

    divisor = a1*b2 - a2*b1
    if not divisor:
        return None
    
    x = (c1*b2 - c2*b1) / divisor
    y = (a1*c2 - a2*c1) / divisor
    t1 = (x - hail1.px) / hail1.vx
    z1 = hail1.pz + t1 * hail1.vz
    t2 = (x - hail2.px) / hail2.vx
    z2 = hail2.pz + t2 * hail2.vz

    return (Point(x,y,z1,t1), Point(x,y,z2,t2))

def main(data):
    hailstones = []
    for line in data:
        hailstones.append(Hailstone(*all_ints(line)))

    # Star 1
    test_min, test_max = 7, 27
    #test_min, test_max = 200000000000000, 400000000000000
    
    intersections = 0
    for idx, hailstone1 in enumerate(hailstones):
        for hailstone2 in hailstones[idx+1:]:
            locs = find_intersection(hailstone1, hailstone2)
            #print(locs)
            if not locs:
                continue
            valid = True
            for loc in locs:
                if loc.t < 0 or not (test_min <= loc.x <= test_max) or not (test_min <= loc.y <= test_max):
                    valid = False
            if valid:
                intersections += 1
    print(intersections)

    # Star 2
    # variables: px, py, pz, vx, vy, vz, t1, t2, ..., tn
    # px + vx*t1 = px1 + vx1*t1
    # each of these for 3 points gives 9 equations, 9 unknowns
    px, py, pz, vx, vy, vz, t1, t2, t3 = symbols('px py pz vx vy vz t1 t2 t3')
    soln = solve([
        px + vx*t1 - hailstones[0].px - hailstones[0].vx*t1,
        py + vy*t1 - hailstones[0].py - hailstones[0].vy*t1,
        pz + vz*t1 - hailstones[0].pz - hailstones[0].vz*t1,
        px + vx*t2 - hailstones[1].px - hailstones[1].vx*t2,
        py + vy*t2 - hailstones[1].py - hailstones[1].vy*t2,
        pz + vz*t2 - hailstones[1].pz - hailstones[1].vz*t2,
        px + vx*t3 - hailstones[2].px - hailstones[2].vx*t3,
        py + vy*t3 - hailstones[2].py - hailstones[2].vy*t3,
        pz + vz*t3 - hailstones[2].pz - hailstones[2].vz*t3,
    ], [px,py,pz,vx,vy,vz,t1,t2,t3], dict=True)
    soln = soln[0]
    print(sum((soln[px], soln[py], soln[pz])))

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
