import re
import pprint
import numpy as np
from alive_progress import alive_bar
from typing import *


EXAMPLE = """
Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II
""".strip()


INF = 1 << 20


def warshall_floyd(matrix):
    V = len(matrix)
    dist = [[INF for i in range(V)] for j in range(V)]

    for u in range(V):
        for v in range(V):
            dist[u][v] = matrix[u][v]
        dist[u][u] = 0

    for k in range(V):
        for u in range(V):
            for v in range(V):
                new_dist = dist[u][k] + dist[k][v]
                if new_dist < dist[u][v]:
                    dist[u][v] = new_dist
    return dist


def parse(s: str) -> tuple[list[list[int]], list[int], int]:
    pattern = re.compile(
        r'Valve (.+) has flow rate=(\d+); tunnels? leads? to valves? (.+)')

    parts = []
    valves = dict()
    rates = []
    for i, line in enumerate(s.split('\n')):
        valve, fr, others = pattern.findall(line)[0]
        rates.append(int(fr))
        valves[valve] = i
        parts.append((valve, fr, others.split(', ')))

    n = len(valves)
    mtx = np.zeros((n, n), dtype=int)
    mtx[:, :] = INF
    for valve, _, others in parts:
        u = valves[valve]
        for v in (valves[o] for o in others):
            mtx[u][v] = 1

    dist = warshall_floyd(mtx)

    # Many valve has flow rate=0. We don't visit there to open the valves.
    # Therefore, they can be removed from the graph and regarded as a cost of
    # moving to another valve.
    graph = [[] for _ in range(n)]
    for u in range(n):
        if valves['AA'] != u and rates[u] == 0:
            continue
        for v in range(n):
            if u != v and mtx[u][v] and rates[v] > 0:
                graph[u].append((v, dist[u][v]))

    start = valves['AA']

    return graph, rates, start


def max_pressure(graph, rates, start, t) -> int:
    ans = 0

    def bfs(cur: int, point: int, t: int, visited: set[int]):
        nonlocal ans

        if t <= 0:
            return

        visited.add(cur)
        if rates[cur]:
            t -= 1  # time to open valve
            point += rates[cur] * t
            ans = max(ans, point)

        for nxt, cost in graph[cur]:
            if nxt in visited:
                continue

            bfs(nxt, point, t-cost, visited)

        visited.remove(cur)

    bfs(start, 0, t, set())
    return ans


def part1(s: str) -> int:
    graph, rates, start = parse(s)
    return max_pressure(graph, rates, start, t=30)


def divide_nodes(nodes: list[int]) -> Iterator[tuple[list[int], list[int]]]:
    n = len(nodes)

    # We don't care which is me or elepahnt. Because of this symmetry, we can
    # reduce the combination by half.
    for i in range(2 ** (n-1)):
        my_nodes = []
        eleph_nodes = []

        for u in range(n):
            if (i >> u) & 1:
                my_nodes.append(nodes[u])
            else:
                eleph_nodes.append(nodes[u])
        yield my_nodes, eleph_nodes


def get_subgraph(graph, nodes):
    subgraph = [[] for _ in range(len(graph))]

    for u in range(len(graph)):
        if u not in nodes:
            continue
        for (v, cost) in graph[u]:
            if v in nodes:
                subgraph[u].append((v, cost))
    return subgraph


def bit_add(val, x):
    return val | (1 << x)


def bit_remove(val, x):
    return val ^ (1 << x)


def bit_has(val, x):
    return (val >> x) & 1


CACHE = dict()


def max_pressure2(graph, rates, start, t) -> int:
    # A set can be represented by a single integer: node u is present if u-th
    # bit is 1 therefore a state can be represented as a tuple of integers and
    # the tuple is a cache key.

    # NOTE this fucntion needs several GBs of memory but actually not so fast...

    graph_key = 0
    for u in range(len(graph)):
        if graph[u]:
            graph_key = bit_add(graph_key, u)

    def bfs(cur: int, t: int, visited_bit: int):
        key = (graph_key, cur, t, visited_bit)
        cache = CACHE.get(key)
        if cache is not None:
            return cache

        if t <= 0:
            return 0

        visited_bit = bit_add(visited_bit, cur)

        if rates[cur]:
            t -= 1  # time to open valve
            point = rates[cur] * t
        else:
            point = 0

        other_point = 0
        for nxt, cost in graph[cur]:
            if bit_has(visited_bit, nxt):
                continue

            other_point = max(other_point, bfs(nxt, t-cost, visited_bit))

        ret = point + other_point
        CACHE[key] = ret
        return ret

    return bfs(start, t, 0)


def part2(s: str) -> int:
    graph, rates, start = parse(s)
    ans = 0

    non_zero_nodes = [u for u in range(len(rates)) if rates[u]]
    with alive_bar(2 ** (len(non_zero_nodes)-1)) as bar:
        for my_nodes, eleph_nodes in divide_nodes(non_zero_nodes):

            if start not in my_nodes:
                my_nodes.append(start)
            if start not in eleph_nodes:
                eleph_nodes.append(start)

            my_graph = get_subgraph(graph, my_nodes)
            eleph_graph = get_subgraph(graph, eleph_nodes)

            my_pressure = max_pressure2(my_graph, rates, start, t=26)
            eleph_pressure = max_pressure2(eleph_graph, rates, start, t=26)

            ans = max(ans, my_pressure+eleph_pressure)

            bar()
    return ans


assert part1(EXAMPLE) == 1651
assert part2(EXAMPLE) == 1707

with open('inputs/day16.txt') as f:
    s = f.read()
print('part1', part1(s))
print('part2', part2(s))
