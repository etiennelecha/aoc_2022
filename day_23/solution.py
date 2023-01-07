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
DIRECTIONS = {0: N, 2: S, 1: W, 3: E}
INV_DIV = {v : k for k, v in DIRECTIONS.items()}
NORTH = {NE, N, NW}
EAST = {NE, E, SE}
SOUTH = {SE, S, SW}
WEST = {W, SW, NW}
PRIO = deque([N, S, W, E])
MAP_ = {N: NORTH, S: SOUTH, E: EAST, W: WEST}

class PartI:
    ROUNDS = 10
    @staticmethod
    def first_half(elves_og, prio):
        elves = elves_og.copy()
        for i, j in elves:
            if not any((i + di, j + dj) in elves for di, dj in {N, S, E, W, NW, NE, SW, SE}):
                continue
            for side in prio:
                if not any((i + di, j + dj) in elves for di, dj in MAP_[side]):
                    elves[(i, j)] <<= 2 
                    elves[(i, j)] += INV_DIV[side]
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
            if not elf >> 2:
                continue
            d = elf & 3
            di, dj = DIRECTIONS[d]
            neigh = i + 2 * di, j + 2 * dj
            if neigh in elves and elves[neigh] >> 2 and elves[neigh] & 3 == (d + 2) % 4:
                visited.add(neigh)
                elves[(i, j)] = 1
                elves[neigh] = 1    
            else:
                elves[(i + di, j + dj)] = 1
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