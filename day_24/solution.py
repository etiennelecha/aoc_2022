import time
import copy
from collections import deque


with open('aoc_day24.txt', 'r') as f:
    lines = f.read().splitlines()
M = len(lines)
N = len(lines[0])
GRID = [[0 for _ in range(N)] for _ in range(M)]
ALL = 16 - 1
N_ = 1
S = 2
E = 4
W = 8
ROSE = {N_: (-1, 0), S:(1, 0), E: (0, 1), W: (0, -1)}
# grid with each containing with the list of the winds
for i in range(M):
    for j in range(N):
        if lines[i][j] == '<':
            GRID[i][j] = W
        elif lines[i][j] == '>':
            GRID[i][j] = E
        elif lines[i][j] == 'v':
            GRID[i][j] = S
        elif lines[i][j] == '^':
            GRID[i][j] = N_
        elif lines[i][j] == '#':
            GRID[i][j] = -1
CANDIDATES = list(ROSE.values())
CANDIDATES.append((0, 0))
            
class PartI:
    @staticmethod
    def total_winds(grid):
        ans = 0
        for i in range(M):
            for j in range(N):
                if grid[i][j] <= 0:
                    continue
                bitmask = 1
                for _ in range(4):
                    wind = grid[i][j] & bitmask
                    bitmask <<= 1    
                    if not wind:
                        continue
                    ans += 1
        return ans


    @staticmethod
    def get_neigh(i, j, dir):
        di, dj = dir
        if i + di == 0:
            k = M - 2
        elif i + di == M - 1:
            k = 1
        else:
            k = i + di
        if j + dj == 0:
            l = N - 2
        elif j + dj == N - 1:
            l = 1
        else:
            l = j + dj
        return k, l

    @staticmethod
    def blow(grid): # modify grid in place
        for i in range(M):
            for j in range(N):
                if grid[i][j] <= 0:
                    continue
                winds = grid[i][j] & ALL
                bitmask = 1
                for _ in range(4):
                    wind = winds & bitmask
                    bitmask <<= 1    
                    if not wind:
                        continue
                    k, l = PartI.get_neigh(i, j, ROSE[wind])
                    grid[k][l] |= wind << 4
        for i in range(M):
            for j in range(N):
                grid[i][j] >>= 4
    
    @staticmethod
    def bfs(u, v, grid):
        steps = 0
        q = deque([u])
        steps = 0
        positions = set()
        while q:
            l_0 = len(q)
            positions.clear()
            PartI.blow(grid)
            for _ in range(l_0):
                i, j = q.popleft()
                if (i, j) == v:
                    return steps
                for di, dj in CANDIDATES:
                    ii, jj = i + di, j + dj
                    if 0 <= ii <= M - 1 and grid[ii][jj] == 0 and (ii, jj) not in positions:
                        q.append((ii, jj))
                        positions.add((ii, jj))
            steps += 1
        return -1 

    def __call__(self, grid):
        s = time.time()
        start = 0, [i for i in range(N) if lines[0][i] == '.'][0]
        end = M - 1, [i for i in range(N) if lines[M - 1][i] == '.'][0]
        steps = self.bfs(start, end, grid)
        e = time.time()
        print(f'answer part I: {steps} in {e - s:.3f}s')
    
class PartII:
    def __call__(self, grid):
        print('Part II\n-----------------------------')
        s = time.time()
        start = 0, [i for i in range(N) if lines[0][i] == '.'][0]
        end = M - 1, [i for i in range(N) if lines[M - 1][i] == '.'][0]
        steps1 = PartI.bfs(start, end, grid)
        e = time.time()
        print(f'First round: {steps1} in {e - s:.3f}s')
        s = s = time.time()
        steps2 = PartI.bfs(end, start, grid)
        e = time.time()
        print(f'Second round: {steps2} in {e - s:.3f}s')
        s = s = time.time()
        steps3 = PartI.bfs(start, end, grid)
        e = time.time()
        print(f'Third round: {steps3} in {e - s:.3f}s')
        print(f'-----------------------------\nFinal answer: {steps3 + steps1 + steps2 + 2}')

if __name__  == '__main__':
    PartI()(copy.deepcopy(GRID))
    PartII()(copy.deepcopy(GRID))
    
        
                