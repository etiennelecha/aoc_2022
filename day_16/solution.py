import re

with open('aoc_day16.txt', 'r') as f:
    lines = f.read().splitlines()
nodes = []
for line in lines:
    valves = re.findall(r'([A-Z][A-Z])', line)
    flow = int(re.findall(r'\d+', line)[0])
    nodes.append((valves[0], flow, valves[1:]))
nodes.sort()
dic = {valve: i for i, (valve, _, _) in enumerate(nodes)}

def g(node):
    value, flow, neighs = node
    return dic[value], flow, [dic[neigh] for neigh in neighs]

nodes = list(map(g, nodes))
neighbors = [n for _, _, n in nodes]
flows = [flow for _, flow, _ in nodes]


class PartI:

    dp = [[-1] * 31 for _ in range(len(flows))] 
    # dp[i][j] max pressure released in the end IF NO OTHER MOVE IS MADE after step j when at node i  

    def dfs(self, node, pressure, open, step): # pressure: pressure already released, open: set of valves opened
        if step > 30:
            return
        incr = sum(flows[i] for i in open)
        curr = pressure + (31 - step) * incr
        if self.dp[node][step] >= curr:
            return
        self.dp[node][step] = curr
        for n in neighbors[node]:
            self.dfs(n, pressure + incr, open, step + 1)
            if flows[node] != 0 and node not in open:
                self.dfs(n, pressure + 2 * incr, open | {node}, step + 2)
    
    def __call__(self):
        self.dfs(0, 0, set(), 0)
        return max(self.dp[i][j] for i in range(len(flows)) for j in range(31))

class PartII:
    
    dp = [[[-1] * 27 for _ in range(len(flows))] for _ in range(len(flows))] 
    # dp[i][j][k] max pressure released in the end IF NO OTHER MOVE IS MADE after step k,  when at node i, j

    def dfs(self, node1, node2, pressure, open, step): # pressure: pressure already released, open: set of valves opened
        if step > 26:
            return
        incr = sum(flows[i] for i in open)
        curr = pressure + (26 - step) * incr
        if self.dp[node1][node2][step] >= curr:
            return
        self.dp[node1][node2][step] = curr
        if (flows[node1] != 0 and node1 not in open) and not (flows[node2] != 0 and node2 not in open):
            for n2 in neighbors[node2]:
                self.dfs(node1, n2, pressure + incr, open | {node1}, step + 1)
        if (flows[node2] != 0 and node2 not in open) and not (flows[node1] != 0 and node1 not in open):
            for n1 in neighbors[node1]:
                self.dfs(n1, node2, pressure + incr, open | {node2}, step + 1)
        for n1 in neighbors[node1]:
            for n2 in neighbors[node2]:
                self.dfs(n1, n2, pressure + incr, open, step + 1)
                if (flows[n1] != 0 and n1 not in open) and (flows[n2] != 0 and n2 not in open):
                    self.dfs(n1, n2, pressure + 2 * incr, open | {n1, n2}, step + 2)
    
    def __call__(self):
        self.dfs(0, 0, 0, set(), 0)
        return max(self.dp[i][j][k] for i in range(len(flows)) for j in range(len(flows)) for k in range(27))


if __name__ == '__main__':
    print(PartI()())
    print(PartII()())

