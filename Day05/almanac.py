from argparse import ArgumentParser

class RangeMap():
    def __init__(self) -> None:
        self.ranges = {}

    def add_range(self, dest, src, length):
        self.ranges[range(src, src+length)] = dest - src

    def source_to_dest(self, number):
        for span, offset in self.ranges.items():
            if number in span:
                return number + offset
        return number
    
    def dest_to_source(self, number):
        for span, offset in self.ranges.items():
            if number-offset in span:
                return number-offset
        return number
    
def merge_ranges(ranges):
    ranges = [[interval.start, interval.stop] for interval in ranges]
    sorted_ranges = sorted(ranges, key=lambda x: x[0])
    new_ranges = [sorted_ranges[0]]
    for current in sorted_ranges:
        previous = new_ranges[-1]
        if current[0] <= previous[1]:
            previous[1] = max(previous[1], current[1])
        else:
            new_ranges.append(current)

    return [range(interval[0],interval[1]) for interval in new_ranges]
    
def create_map_from_section(data, starting_data_idx):
    this_map = RangeMap()
    # Stops when it finds the empty line that comes after each section
    data_idx = starting_data_idx
    while data_idx < len(data) and data[data_idx]:
        entry = data[data_idx]
        dest, src, length = (int(number) for number in entry.split())
        this_map.add_range(dest, src, length)
        data_idx += 1
    return this_map, data_idx

def main(data):
    data_idx = 3
    seed_to_soil, data_idx = create_map_from_section(data, data_idx)
    soil_to_fertilizer, data_idx = create_map_from_section(data, data_idx+2)
    fertilizer_to_water, data_idx = create_map_from_section(data, data_idx+2)
    water_to_light, data_idx = create_map_from_section(data, data_idx+2)
    light_to_temperature, data_idx = create_map_from_section(data, data_idx+2)
    temperature_to_humidity, data_idx = create_map_from_section(data, data_idx+2)
    humidity_to_location, data_idx = create_map_from_section(data, data_idx+2)

    # Star 1
    seeds = [int(seed) for seed in data[0][6:].split()]

    locations = []
    for seed in seeds:
        soil = seed_to_soil.source_to_dest(seed)
        fertilizer = soil_to_fertilizer.source_to_dest(soil)
        water = fertilizer_to_water.source_to_dest(fertilizer)
        light = water_to_light.source_to_dest(water)
        temperature = light_to_temperature.source_to_dest(light)
        humidity = temperature_to_humidity.source_to_dest(temperature)
        location = humidity_to_location.source_to_dest(humidity)
        locations.append(location)

    print(min(locations))

    # Star 2
    seed_ranges = []
    for seed_idx in range(0,len(seeds),2):
        starting_seed = seeds[seed_idx]
        seed_ranges.append(range(starting_seed, starting_seed+seeds[seed_idx+1]))

    found = False
    # Reverse search - instead of calculating the locations of all the seeds, find the first location that corresponds to a seed we have
    # I have 1.6 * 10**9 seeds to search and one of them will probably be mapped to a location less than that
    for min_loc in range(sum(len(seed_range) for seed_range in seed_ranges)):
        humidity = humidity_to_location.dest_to_source(min_loc)
        temperature = temperature_to_humidity.dest_to_source(humidity)
        light = light_to_temperature.dest_to_source(temperature)
        water = water_to_light.dest_to_source(light)
        fertilizer = fertilizer_to_water.dest_to_source(water)
        soil = soil_to_fertilizer.dest_to_source(fertilizer)
        seed = seed_to_soil.dest_to_source(soil)
        
        for seed_range in seed_ranges:
            if seed in seed_range:
                found = True
        
        if found:
            print(min_loc)
            break

    if not found:
        print('Not found')

    # Brute force search ran in separate kernel but did not finish before I figured out the reverse search and ran it to completion
    # for idx, seed_range in enumerate(seed_ranges):
    #     print(f'starting seed_range {idx} out of {len(seed_ranges)})
    #     for seed in seed_range:
    #         soil = seed_to_soil.source_to_dest(seed)
    #         fertilizer = soil_to_fertilizer.source_to_dest(soil)
    #         water = fertilizer_to_water.source_to_dest(fertilizer)
    #         light = water_to_light.source_to_dest(water)
    #         temperature = light_to_temperature.source_to_dest(light)
    #         humidity = temperature_to_humidity.source_to_dest(temperature)
    #         location = humidity_to_location.source_to_dest(humidity)
    #         print(seed, soil, fertilizer, water, light, temperature, humidity, location, '\n')
    #         if location < min_loc:
    #             min_loc = location

    # print(min_loc)

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
    data = read_input(args.input)
    main(data)
