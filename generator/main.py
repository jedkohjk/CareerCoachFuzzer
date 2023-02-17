from .existing import *
from .new import *

# Main generator

# functions imported from other modules
fns = [[i.poll for i in savers], [make_name, make_ic,  make_number, make_email]]
# relative priority of generating names, nrics, numbers and emails respectively
# since emails are new, they have the highest priority
priority = [0.25, 0.125, 0.125, 0.5]

# some test cases before the fuzzing
# empty string to test for AC5
# ', ", \ are special characters, used test if they escape these characters
# - is used to denote a blank entry; {space}, - and null are tested to see if they have any special meaning
# '-' * 127 is unlikely to match anything; this is used to guarantee testing AC6, though fuzzer is likely to generate queries that match nothing too
# non-printable characters are also tested
standard = ['i'+chr(0)+'j', chr(21)*2, chr(31), '-' * 127, ' ', 'null', '-', '\\', '"', "'", '']

# keeps a count of which types it has tried to generate for
# tries to generate for all types
tries = [0, 0, 0, 0]

def generate(counts):
    # if anything from the standard list is not yet tested, test them
    if standard:
        return [standard.pop(), None, int(random()*4)]
    # chooses which type to generate for based on priority, match counts and tries
    scores = [(counts[i]+1)*(tries[i]+1)/priority[i] for i in range(4)]
    min_score = min(scores)
    tested = scores.index(min_score)
    tries[tested] += 1
    # if it has tried to generate for this type many times with no success, generate for that type from existing entries
    if tries[tested] > scores[tested] * random():
        op = fns[0][tested]()
        if op is not None:
            return op + [tested]
    return [fns[1][tested](), None, tested]
