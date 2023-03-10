import re
from collections import deque

with open('aoc_day22.txt', 'r') as f:
    grid, s = f.read().split('\n\n')
lines = grid.splitlines()

class ThreeDVect():
    
    def __init__(self, x:int=0, y:int=0, z:int=0):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, v) -> bool:
        return self.x == v.x and self.y == v.y and self.z == v.z
    
    def __hash__(self) -> int:
        return hash((self.x, self.y, self.z))

    def __add__(self, v):
        return ThreeDVect(self.x + v.x, self.y + v.y, self.z + v.z)
    
    def __neg__(self):
        return ThreeDVect(-self.x, -self.y, -self.z)
    
    def __mul__(self, v):
        u1, u2, u3 = self.x, self.y, self.z
        v1, v2, v3 = v.x, v.y, v.z
        return ThreeDVect(u2 * v3 - u3 * v2, u3 * v1 - u1 * v3, u1 * v2 - u2 * v1)
    
    def __or__(self, v) -> int:
        return self.x * v.x + self.y * v.y + self.z * v.z

    def __repr__(self):
        return f'|| {self.x} | {self.y} | {self.z} ||'


class ThreeDMatriX():

    def __init__(self, u:ThreeDVect, v:ThreeDVect, w:ThreeDVect):
        # a matrix is just a collection of vectors IN LINE (easier to formalute vector mult)
        # so 1st line is u, 2nd v, 3rd w
        self.u = u
        self.v = v
        self.w = w
    
    def transpose(self):
        u, v, w = self.u, self.v, self.w
        u1 = ThreeDVect(u.x, v.x, w.x)
        u2 = ThreeDVect(u.y, v.y, w.y)
        u3 = ThreeDVect(u.z, v.z, w.z)
        return ThreeDMatriX(u1, u2, u3)

    def __eq__(self, b):
        return self.u == b.u and self.v == b.v and self.w == b.w
    
    def __hash__(self):
        return hash((self.u, self.v, self.w))

    def __mul__(self, v: ThreeDVect):
        return ThreeDVect(self.u | v, self.v | v, self.w | v)
    
    def __matmul__(self, b):
        # component cij of a @ b is sum over k aik * bkj, so we need to transpose b to
        # use scalar product def     
        b = b.transpose()
        u1 = ThreeDVect(self.u | b.u, self.u | b.v, self.u | b.w)
        u2 = ThreeDVect(self.v | b.u, self.v | b.v, self.v | b.w)
        u3 = ThreeDVect(self.w | b.u, self.w | b.v, self.w | b.w)
        return ThreeDMatriX(u1, u2, u3)
    
    def __pow__(self, k):
        ans = ID
        for _ in range(k):
            ans @= self
        return ans

    def __repr__(self):
        return  f'|| {self.u.x} | {self.u.y} | {self.u.z} ||\n' +\
                f'|| {self.v.x} | {self.v.y} | {self.v.z} ||\n' +\
                f'|| {self.w.x} | {self.w.y} | {self.w.z} ||'

class Cube():

    def __init__(self, edge_l:int, og:ThreeDVect = ThreeDVect(0, 0, 0)):
        self.edge_l = edge_l
        self.og = og
    
    def get_vect_face(self, u: ThreeDVect):
        if u.x == self.og.x: x = 1
        elif u.x == self.og.x + self.edge_l - 1: x = -1
        else: x = 0
        if u.y == self.og.y: y = 1
        elif u.y == self.og.y + self.edge_l - 1: y = -1
        else: y = 0
        if u.z == self.og.z: z = 1
        elif u.z == self.og.z + self.edge_l - 1: z = -1
        else: z = 0
        return ThreeDVect(x, y, z)
    
    def is_edge(self, u:ThreeDVect):
        return  int(u.x == self.og.x or u.x == self.og.x + self.edge_l - 1) +\
                int(u.y == self.og.y or u.y == self.og.y + self.edge_l - 1) +\
                int(u.z == self.og.z or u.z == self.og.z + self.edge_l - 1) >= 2

VEC_X = ThreeDVect(1, 0, 0)
VEC_Y = ThreeDVect(0, 1, 0)
VEC_Z = ThreeDVect(0, 0, 1)
ID = ThreeDMatriX(VEC_X, VEC_Y, VEC_Z)

ROTATIONS = {VEC_X : ThreeDMatriX(VEC_X, -VEC_Z, VEC_Y),
            VEC_Y: ThreeDMatriX(VEC_Z, VEC_Y, -VEC_X),
            VEC_Z: ThreeDMatriX(-VEC_Y, VEC_X, VEC_Z)}
ROTATIONS[-VEC_X] = ROTATIONS[VEC_X] ** 3
ROTATIONS[-VEC_Y] = ROTATIONS[VEC_Y] ** 3
ROTATIONS[-VEC_Z] = ROTATIONS[VEC_Z] ** 3

AXIS = {v: k for k, v in ROTATIONS.items()}

DIRECTIONS = {(int(0), int(1)): 0, (1, 0): 1, (0, -1): 2, (-1, 0): 3}
CUBE_LENGTH = 52

class PartII:

    def matrix(self, rotations: deque[ThreeDVect]) -> ThreeDMatriX:
        r = rotations.copy()
        ans = ID
        while r:
            ans @= ROTATIONS[r.popleft()]
        return ans

    def inverse_matrix(self, rotations: deque[ThreeDVect]) -> ThreeDMatriX:
        r = rotations.copy()
        ans = ID
        while r:
            ans @= ROTATIONS[-r.pop()]
        return ans
    
    def fold_into_cube(self, p_grid:ThreeDVect, p_cube:ThreeDVect, d_grid:ThreeDVect):
        fold = [[['X'] * CUBE_LENGTH for _ in range(CUBE_LENGTH)] for _ in range(CUBE_LENGTH)]
        initial_rot_grid = ROTATIONS[-VEC_Z]
        cube = Cube(CUBE_LENGTH)
        visited = set() 
        rot_grid = initial_rot_grid
        trans_grid_cube = ID
        
        faces = {}
        folded = {}
        unfolded = {}
        rotations_faces = deque([])
        faces[VEC_Z] = rotations_faces.copy()
    
        while True:
        
            next_d_grid = rot_grid * d_grid
            next_p_grid = p_grid + next_d_grid
            i, j = next_p_grid.x, next_p_grid.y
            
            if (i, j) not in visited and 0 <= i < len(lines) and len(lines[i]) > j >= 0 and lines[i][j] != ' ':
                p_grid = next_p_grid
                d_grid = next_d_grid
                
                d_cube = trans_grid_cube * d_grid
                next_p_cube = p_cube + d_cube
                
                if cube.is_edge(next_p_cube):
                    axis = d_cube * cube.get_vect_face(p_cube)
                    trans_grid_cube = ROTATIONS[axis] @ trans_grid_cube
                    d_cube = trans_grid_cube * d_grid
                    next_p_cube += d_cube
                    if cube.get_vect_face(next_p_cube) not in faces:
                        rotations_faces.appendleft(axis)
                        faces[cube.get_vect_face(next_p_cube)] = rotations_faces.copy()
                
                p_cube = next_p_cube
                fold[p_cube.x][p_cube.y][p_cube.z] = lines[i][j]
                folded[(i, j)] = p_cube
                unfolded[p_cube] = (i, j)
                
                visited.add((i, j))
                rot_grid = initial_rot_grid

            elif rot_grid != ROTATIONS[VEC_Z] ** 2:
                rot_grid @= ROTATIONS[VEC_Z]
            else:
                break
        
        return fold, folded, unfolded, faces
    
    def walk(self, fold:list[list[list[str]]], u0:ThreeDVect, steps:int, dir:ThreeDVect):
        step = 0
        u = u0
        cube = Cube(CUBE_LENGTH)
        while step < steps:
            u1 = u + dir
            if fold[u1.x][u1.y][u1.z] == '#':
                break
            if fold[u1.x][u1.y][u1.z] == 'X':
                axis = dir * cube.get_vect_face(u)
                dir_trans = ROTATIONS[axis] * dir
                u1 += dir_trans
                if fold[u1.x][u1.y][u1.z] == '#':
                    break
                dir = dir_trans
            u = u1
            step += 1
        return u, dir

    def __call__(self):
        fold, folded, unfolded, faces = self.fold_into_cube(p_grid=ThreeDVect(199, -1, 0),
                                                            p_cube=ThreeDVect(50, 0, 0),
                                                            d_grid=ThreeDVect(0, 1, 0))
        start_steps = int(re.findall(r'^\d+', s)[0])
        instructions = re.findall(r'([LR])(\d+)', s)
        start_pos = folded[(0, 50)]
        cube = Cube(CUBE_LENGTH)
        start_dir = self.matrix(faces[cube.get_vect_face(start_pos)]) * ThreeDVect(0, 1, 0)
        u, dir = self.walk(fold, start_pos, start_steps, start_dir)
        for instruction in instructions:
            rot, steps = instruction; steps = int(steps)
            if rot == 'L':
                dir = ROTATIONS[cube.get_vect_face(u)] * dir
            else:
                dir = ROTATIONS[-cube.get_vect_face(u)] * dir
            u, dir = self.walk(fold, u, steps, dir)
        
        x, y = unfolded[u]
        d = self.inverse_matrix(faces[cube.get_vect_face(u)]) * dir
        return (x + 1) * 1000 + (y + 1) * 4 + DIRECTIONS[(d.x, d.y)]


if __name__ == '__main__':
    print(PartII()())
    


    


        
    