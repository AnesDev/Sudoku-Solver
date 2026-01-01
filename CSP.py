import numpy as np

class SudokoCSP() :
    def __init__(self, grid):
        self.grid = grid
        
        # variables are all empty cells 
        self.variables = [(r,c) for r in range(9) for c in range(9) if grid[r][c] == 0]
        
        self.domains = {var: set(x for x in range(1, 10)) for var in self.variables}

        # Enforce node consistency
        for i in range(9):
            for j in range(9):
                pair = (i, j)
                val = self.grid[i][j]
                if val != 0:
                    for var in self.domains.keys():
                        if var[0] == i or var[1] == j or self.same_block(var, pair) : 
                            self.domains[var].discard(val)
    
    def same_block(self, a, b):
            xa = a[0] // 3
            ya = a[1] // 3
            xb = b[0] // 3
            yb = b[1] // 3
            return xa == xb and ya == yb

    def get_neighbors(self, z):
        return [v for v in self.variables if v != z and
              (v[0] == z[0] or v[1] == z[1] or self.same_block(z, v))]
    
    # Check arc consistency
    def is_consistent(self, x, y):
        for z in self.domains[y]:
            if z != x:return True
        return False
    
    def is_valid(self, r, c, val):
        if val in self.grid[r]:
            return False
        if val in self.grid[:, c]:
            return False
        br, bc = 3 * (r // 3), 3 * (c // 3)
        if val in self.grid[br:br+3, bc:bc+3]:
            return False
        return True
    
    # Enforce arc consistency between a and b
    def revise(self, a, b):
        revised = False
        for v in self.domains[a].copy():
            if not self.is_consistent(v, b):
                self.domains[a].discard(v)
                revised = True

        return revised

    
    # Enforce arc consistency across all variables
    def ac3(self):
        queue = [(a,b) for a in self.variables for b in self.get_neighbors(a)]

        while(len(queue) != 0):
            pair = queue.pop(0)
            a, b = pair
            if self.revise(a,b):
                if len(self.domains[a]) == 0:
                    return False
                for c in self.get_neighbors(a):
                    if (c != b):
                        queue.append((c,a))
        return True
    
    def dfs(self, current_domains):
            empty = [v for v in self.variables if self.grid[v[0], v[1]] == 0]
            if not empty:
                return True

            r, c = min(empty, key=lambda v: len(current_domains[v]))

            for val in sorted(current_domains[(r, c)]):
                if self.is_valid(r, c, val):
                    self.grid[r, c] = val
                    
                    local_domains = {v: d.copy() for v, d in current_domains.items()}
                    local_domains[(r, c)] = {val}
                    
                    original_domains = self.domains
                    self.domains = local_domains
                    
                    if self.ac3():
                        if self.dfs(local_domains):
                            return True
                    
                    self.domains = original_domains
                    
                    self.grid[r, c] = 0
            return False

    def solve(self):
        # initial ac3
        if not self.ac3():
            print("Not solvable")
            return False
        
        # dfs + lookahead
        if self.dfs(self.domains): 
            print(self.grid)
            return True
        else:
            print("Not solvable")
            return False
