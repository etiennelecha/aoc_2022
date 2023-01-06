import re
from collections import deque

with open('aoc_day18.txt', 'r') as f:
    cubess = f.read().splitlines()
cubes = []
for cube in cubess:
    x, y, z = re.findall(r'\d+', cube)
    cubes.append((int(x), int(y), int(z)))

class PartI:

    def exterior_faces(self, cubes):
        cubes.sort()
        neighbors = 0
        for i in range(len(cubes)):
            for j in range(i + 1, len(cubes)):
                x, y, z = cubes[i]
                xx, yy, zz = cubes[j]
                if abs(x - xx) + abs(y - yy) + abs(z- zz) == 1:
                    neighbors += 1
                if xx > x and yy > y:
                    break
        return 6 * len(cubes) - 2 * neighbors

    def __call__(self):
        return self.exterior_faces(cubes)

class PartII:

    def bfs(self, x, y, z):
        visited = {(x, y, z)} | set(cubes)
        interior = True
        q = deque([(x, y, z)])
        while q:
            x, y, z = q.popleft()
            for delta in {1, -1}:
                if (x + delta, y, z) not in visited and 0 <= x + delta < 20:
                    q.append((x + delta, y, z))
                    visited.add((x + delta, y, z))
                if (x, y + delta, z) not in visited and 0 <= y + delta < 20:
                    q.append((x, y + delta, z))
                    visited.add((x, y + delta, z))
                if (x, y, z + delta) not in visited and 0 <= z + delta < 20:
                    q.append((x, y , z + delta))
                    visited.add((x, y, z + delta))
                if x + delta < 0 or x + delta >= 20 or y + delta < 0 or y + delta >= 20 or z + delta < 0 or z + delta >= 20:
                    interior = False
        return visited - set(cubes), interior
    
    def __call__(self):
        all_visited = set(cubes)
        total_faces = PartI().exterior_faces(cubes)
        for x in range(20):
            for y in range(20):
                for z in range(20):
                    if (x, y, z) not in all_visited:
                        visited, interior = self.bfs(x, y, z)
                        all_visited |= visited
                        if interior:
                            total_faces -= PartI().exterior_faces(list(visited))
        return total_faces       

if __name__ == '__main__':
    print(PartI()())
    print(PartII()())
        