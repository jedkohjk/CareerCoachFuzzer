from .shared import *

# Generates searches that it knows must have results

class Saver:

    def __init__(self, chop = True):
        self.lst = dict()
        self.chop = chop

    # returns the query and the full entry from which it was generated
    def poll(self) -> list:
        if self.lst:
            for key in self.lst:
                op = key
                val = self.lst.pop(key)
                break
            if self.chop:
                # randomly decides whether to randomise the case
                if random() > 0.25:
                    op = random_case(op)
                # randomly decides whether to slice the query
                if random() > 0.25:
                    op = random_slice(op)
            return [op, val]

    # decides whether or not to add an entry; returns boolean based on if key saved
    def add(self, key: str, val: list) -> bool:
        # if the key is already in the dictionary
        # do not add to the dictionary
        # stop the entry from being added to other Savers by returning true, to maximisevariation in generation corpus
        if key in self.lst:
            return True
        # whether something is added is based on chance, but the more items already saved, the less likely something is to be added
        # do not add empty or blank entries
        if random() < 4/(len(self.lst)+1) and key and key != '-':
            self.lst[key] = val
            return True
        return False

savers = [Saver(), Saver(False), Saver(), Saver()]
