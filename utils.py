import re

# Does not match negatives!
def all_ints(s):
    return [int(i) for i in re.findall(r'\b\d+\b', s)]
