import re

class ThreeDVect():
    
    def __init__(self, x=0, y=0, z=0):
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
        return f'{self.x} | {self.y} | {self.z}'


class ThreeDMatriX():

    def __init__(self, u:ThreeDVect, v:ThreeDVect, w:ThreeDVect):
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
        b = b.transpose()
        u1 = ThreeDVect(self.u | b.u, self.u | b.v, self.u | b.w)
        u2 = ThreeDVect(self.v | b.u, self.v | b.v, self.v | b.w)
        u3 = ThreeDVect(self.w | b.u, self.w | b.v, self.w | b.w)
        return ThreeDMatriX(u1, u2, u3)
    
    def __repr__(self):
        return f'{self.u.x} | {self.u.y} | {self.u.z}\n{self.v.x} | {self.v.y} | {self.v.z}\n{self.w.x} | {self.w.y} | {self.w.z}'

class Cube():

    def __init__(self, edge_l:int, og:ThreeDVect = ThreeDVect(0, 0, 0)):
        self.edge_l = edge_l
        self.og = og
    
    def get_vect_face(self, u: ThreeDVect):
        if u.x == self.og.x: x = 1
        elif u.x == self.og.x + self.edge_l: x = -1
        else: x = 0
        if u.y == self.og.y: y = 1
        elif u.y == self.og.y + self.edge_l: y = -1
        else: y = 0
        if u.z == self.og.z: z = 1
        elif u.z == self.og.z + self.edge_l: z = -1
        else: z = 0
        return ThreeDVect(x, y, z)
    
    def is_edge(self, u:ThreeDVect):
        return  int(u.x == self.og.x or u.x == self.og.x + self.edge_l) +\
                int(u.y == self.og.y or u.y == self.og.y + self.edge_l) +\
                int(u.z == self.og.z or u.z == self.og.z + self.edge_l) >= 2

VEC_X = ThreeDVect(1, 0, 0)
VEC_Y = ThreeDVect(0, 1, 0)
VEC_Z = ThreeDVect(0, 0, 1)

ROTATIONS = {VEC_X : ThreeDMatriX(VEC_X, -VEC_Z, VEC_Y),
            VEC_Y: ThreeDMatriX(VEC_Z, VEC_Y, -VEC_X),
            VEC_Z: ThreeDMatriX(-VEC_Y, VEC_X, VEC_Z),
            -VEC_X : ThreeDMatriX(VEC_X, VEC_Z, -VEC_Y),
            -VEC_Y: ThreeDMatriX(-VEC_Z, VEC_Y, VEC_X),
            -VEC_Z: ThreeDMatriX(VEC_Y, -VEC_X, VEC_Z)}

AXIS = {v: k for k, v in ROTATIONS.items()}

ID = ThreeDMatriX(VEC_X, VEC_Y, VEC_Z)

CUBE_LENGTH = 52

if __name__ == '__main__':
    
    with open('aoc_day22.txt', 'r') as f:
        grid, s = f.read().split('\n\n')
    lines = grid.splitlines()
    
    fold = [[['X'] * CUBE_LENGTH for _ in range(CUBE_LENGTH)] for _ in range(CUBE_LENGTH)]
    
    p_grid = ThreeDVect(199, 0, 0)
    p_cube = ThreeDVect(1, 1, 0)
    d_grid = ThreeDVect(0, 1, 0)
    d_cube = d_grid
    initial_rot_grid = ROTATIONS[-VEC_Z]
    cube = Cube(CUBE_LENGTH)
    visited = set() 
    rot_grid = initial_rot_grid
    trans_grid_cube = ID
    faces = {}
    folded = {}
    
    faces[cube.get_vect_face(p_cube)] = trans_grid_cube
    while True:
        next_d_grid = rot_grid * d_grid
        next_p_grid = p_grid + d_grid
        i, j = next_p_grid.x, next_p_grid.y
        #print(f'{rot_grid, next_p_grid, p_grid, d_grid}dwe')
        if (i, j) not in visited and i < len(lines) and len(lines[i]) > j and lines[i][j] != ' ':
            #print(i, j)
            p_grid = next_p_grid
            d_grid = next_d_grid
            d_cube = (rot_grid @ trans_grid_cube) * d_cube
            next_p_cube = p_cube + d_cube
            if cube.is_edge(next_p_cube):
                trans_grid_cube @= ROTATIONS[cube.get_vect_face(p_cube) * d_cube]
                d_cube = (trans_grid_cube @ rot_grid) * d_cube
                next_p_cube += d_cube
                faces[cube.get_vect_face(next_p_cube)] = trans_grid_cube
            p_cube = next_p_cube
            fold[p_cube.x][p_cube.y][p_cube.z] = lines[i][j]
            folded[p_cube] = (i, j)
            rot_grid = initial_rot_grid
        elif rot_grid != ROTATIONS[VEC_Z] @ ROTATIONS[VEC_Z]:
            rot_grid @= ROTATIONS[VEC_Z]
        else:
            break
    
        
    print((ROTATIONS[VEC_Z]) * d_grid, ((ROTATIONS[VEC_Z] @ ROTATIONS[VEC_Z]) * d_grid))
            


    


        
    