import random

# each function must work in o(1)

class RandomizedSet:

    def __init__(self):
        self.values = [] # array of values
        self.pos = {}    # value -> index

    def insert(self, val: int) -> bool:
        if val in self.pos: 
            return False
            
        index = len(self.values)
        self.values.append(val)
        self.pos[val] = index
        
        return True        

    def remove(self, val: int) -> bool:
        if val not in self.pos:
            return False

        index = self.pos[val]

        # remove from the array
        last = self.values[-1] 
        self.values[index] = last
        del self.values[-1]

        # update hashmap
        self.pos[last] = index
        del self.pos[val]

        return True
        

    def getRandom(self) -> int:
        index = random.randrange(0, len(self.values))

        return self.values[index]
    