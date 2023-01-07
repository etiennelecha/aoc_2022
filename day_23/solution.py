from collections import deque

with open('aoc_day23.txt', 'r') as f:
    lines = f.read().splitlines()
ELVES = {}
for i, line in enumerate(lines):
    for j, c in enumerate(line):
        if c == '#':
            ELVES[(i, j)] = 1
N = (-1, 0)
S = (1, 0)
E = (0, 1)
W = (0, -1)
NE = (-1, 1)
NW = (-1, -1)
SE = (1, 1)
SW = (1, -1)

PRIO = deque([int('111', 2), int('1110000', 2), int('11100', 2), int('11000001', 2)])
MAP_ = {int('111', 2): N, int('1110000', 2): S, int('11100', 2): W, int(' 11000001', 2): E}
ALL = int('11111111', 2)
OPPOSITES = {int('111', 2): int('1110000', 2),
            int('1110000', 2): int('111', 2),
            int('11100', 2): int('11000001', 2),
            int('11000001', 2): int('11100', 2)}
                 
class PartI:
    ROUNDS = 10
    @staticmethod
    def get_neighbors(elves, key):
        assert key in elves, 'Please provide actual elf'
        ans = 0
        bit_mask = 1
        i, j = key
        for di, dj in [NE, N, NW, W, SW, S, SE, E]:
            if (i + di, j + dj) in elves:
                ans |= bit_mask
            bit_mask <<= 1
        return ans

    @staticmethod
    def first_half(elves_og, prio):
        elves = elves_og.copy()
        for i, j in elves:
            neighbors = PartI.get_neighbors(elves, (i, j))
            if not neighbors:
                continue
            for side in prio:
                if not neighbors & side:
                    elves[(i, j)] <<= 8 
                    elves[(i, j)] |= side
                    break
        return elves

    @staticmethod
    def second_half(elves_og):
        elves = elves_og.copy()
        visited = set()
        a = list(elves.keys()).copy()
        for i, j in a:
            if (i, j) in visited:
                continue 
            visited.add((i, j))
            elf = elves[(i, j)]
            if not elf >> 8:
                continue
            d = elf & ALL
            di, dj = MAP_[d]
            neigh = i + 2 * di, j + 2 * dj
            if neigh in elves and elves[neigh] >> 8 and elves[neigh] & ALL == OPPOSITES[elf & ALL]:
                visited.add(neigh)
                elves[(i, j)] >>= 8
                elves[neigh] >>= 8    
            else:
                elves[(i + di, j + dj)] = elves[(i , j)] >> 8
                del elves[(i , j)]
        return elves

    def __call__(self, elves_og, prio_og):
        elves = elves_og.copy()
        prio = prio_og.copy()
        for _ in range(self.ROUNDS):
            elves = self.first_half(elves, prio)
            elves = self.second_half(elves)
            prio.rotate(-1)
        i_min = min(i for i, _ in elves)
        i_max = max(i for i, _ in elves)
        j_min = min(j for _, j in elves)
        j_max = max(j for _, j in elves)
        return (1 + i_max - i_min) * (1 +  j_max - j_min) - len(elves)
    
class PartII:
   
    def __call__(self, elves_og, prio_og):
        rounds = 0
        elves = elves_og.copy()
        prio = prio_og.copy()
        while True:
            elves1 = elves.copy()
            elves1 = PartI.first_half(elves1, prio)
            elves1 = PartI.second_half(elves1)
            prio.rotate(-1)
            rounds += 1
            if elves1 == elves:
                return rounds
            elves = elves1

if __name__ == '__main__':
    print(PartI()(ELVES, PRIO))
    print(PartII()(ELVES, PRIO))