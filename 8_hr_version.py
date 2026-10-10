from collections import deque


class Dinic:
    def __init__(self, n):
        self.graph = [[] for _ in range(n)]

    def add_edge(self, u, v, capacity):
        forward = [v, capacity, len(self.graph[v]), capacity]
        backward = [u, 0, len(self.graph[u]), 0]

        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def bfs(self, source, sink):
        self.level = [-1] * len(self.graph)
        self.level[source] = 0
        queue = deque([source])

        while queue:
            u = queue.popleft()

            for v, cap, rev, original in self.graph[u]:
                if cap > 0 and self.level[v] == -1:
                    self.level[v] = self.level[u] + 1
                    queue.append(v)

        return self.level[sink] != -1

    def dfs(self, u, sink, flow):
        if u == sink:
            return flow

        while self.ptr[u] < len(self.graph[u]):
            edge = self.graph[u][self.ptr[u]]
            v, cap, rev, original = edge

            if cap > 0 and self.level[v] == self.level[u] + 1:
                pushed = self.dfs(v, sink, min(flow, cap))

                if pushed:
                    edge[1] -= pushed
                    self.graph[v][rev][1] += pushed
                    return pushed

            self.ptr[u] += 1

        return 0

    def max_flow(self, source, sink):
        total = 0

        while self.bfs(source, sink):
            self.ptr = [0] * len(self.graph)

            while True:
                pushed = self.dfs(source, sink, float("inf"))

                if pushed == 0:
                    break

                total += pushed

        return total


def maximum_flow_allocation(teams, guides, preferences):
    n = len(teams)
    m = len(guides)

    source = 0
    team_start = 1
    guide_start = team_start + n
    sink = guide_start + m

    network = Dinic(sink + 1)

    for i, (tid, domain, size) in enumerate(teams):
        if 2 <= size <= 4:
            network.add_edge(source, team_start + i, 1)

            compatible = [
                j for j, (gid, gd, capacity) in enumerate(guides)
                if gd == domain and capacity > 0
            ]

            compatible.sort(
                key=lambda j: (
                    (guides[j][0], tid) not in preferences,
                    -guides[j][2],
                    j
                )
            )

            for j in compatible:
                network.add_edge(team_start + i, guide_start + j, 1)

    for j, (gid, domain, capacity) in enumerate(guides):
        network.add_edge(guide_start + j, sink, capacity)

    maximum = network.max_flow(source, sink)

    assignments = {}
    loads = [0] * m

    for i, (tid, domain, size) in enumerate(teams):
        node = team_start + i

        for edge in network.graph[node]:
            v, cap, rev, original = edge

            if guide_start <= v < sink and original == 1 and cap == 0:
                j = v - guide_start
                assignments[i] = j
                loads[j] += 1
                break

    return maximum, assignments, loads


def greedy_allocation(teams, guides, preferences):
    remaining = [g[2] for g in guides]
    assignments = {}

    for i, (tid, domain, size) in enumerate(teams):
        if not 2 <= size <= 4:
            continue

        candidates = [
            j for j, (gid, gd, capacity) in enumerate(guides)
            if gd == domain and remaining[j] > 0
        ]

        candidates.sort(
            key=lambda j: (
                (guides[j][0], tid) not in preferences,
                -remaining[j],
                j
            )
        )

        if candidates:
            j = candidates[0]
            assignments[i] = j
            remaining[j] -= 1

    return assignments


def main():
    print("Enter number of teams:")
    n = int(input())

    teams = []

    print("Enter each team: TeamID Domain Size")
    for _ in range(n):
        tid, domain, size = input().split()
        teams.append((tid, domain, int(size)))

    print("Enter number of guides:")
    m = int(input())

    guides = []

    print("Enter each guide: GuideID Domain Capacity")
    for _ in range(m):
        gid, domain, capacity = input().split()
        guides.append((gid, domain, int(capacity)))

    print("Enter number of preferences (0 if none):")
    p = int(input())

    preferences = set()
    team_ids = {t[0] for t in teams}
    guide_ids = {g[0] for g in guides}

    print("Enter each preference as GuideID TeamID:")
    for _ in range(p):
        gid, tid = input().split()

        if gid in guide_ids and tid in team_ids:
            preferences.add((gid, tid))

    maximum, optimal, loads = maximum_flow_allocation(
        teams, guides, preferences
    )

    greedy = greedy_allocation(teams, guides, preferences)

    print("\nMAX-FLOW OPTIMAL ALLOCATION:")
    for i, (tid, domain, size) in enumerate(teams):
        if i in optimal:
            print(f"{tid} {guides[optimal[i]][0]}")
        else:
            if not 2 <= size <= 4:
                reason = "invalid team size"
            elif not any(g[1] == domain for g in guides):
                reason = "no matching domain"
            elif not any(
                g[1] == domain and g[2] > 0 for g in guides
            ):
                reason = "no available guide capacity"
            else:
                reason = "capacity constraint"
            print(f"{tid} UNASSIGNED - {reason}")

    print("\nGUIDE LOAD REPORT:")
    for j, (gid, domain, capacity) in enumerate(guides):
        print(f"{gid}: {loads[j]}/{capacity}")

    print("\nGREEDY VS OPTIMAL REPORT:")
    print(f"Greedy assigned: {len(greedy)}")
    print(f"Maximum-flow assigned: {maximum}")
    print(f"Greedy gap: {maximum - len(greedy)}")

    print("\nGREEDY ALLOCATION:")
    for i, (tid, domain, size) in enumerate(teams):
        if i in greedy:
            print(f"{tid} {guides[greedy[i]][0]}")
        else:
            print(f"{tid} UNASSIGNED")

    unassigned = [
        teams[i][0] for i in range(n) if i not in optimal
    ]

    print("\nUNASSIGNED:",
          ", ".join(unassigned) if unassigned else "none")


if __name__ == "__main__":
    main()