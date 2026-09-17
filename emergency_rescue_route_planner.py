from collections import deque
import heapq

graph = {
    "A": ["B", "C"],
    "B": ["D", "E"],
    "C": ["F", "G"],
    "D": ["H"],
    "E": ["H"],
    "F": ["I"],
    "G": ["J"],
    "H": ["K"],
    "I": ["K"],
    "J": ["K"],
    "K": ["L"],
    "L": []
}

weighted_graph = {
    "A": [("B", 2), ("C", 4)],
    "B": [("D", 3), ("E", 1)],
    "C": [("F", 2), ("G", 5)],
    "D": [("H", 4)],
    "E": [("H", 1)],
    "F": [("I", 3)],
    "G": [("J", 2)],
    "H": [("K", 2)],
    "I": [("K", 1)],
    "J": [("K", 3)],
    "K": [("L", 2)],
    "L": []
}

START = "A"
GOAL = "L"

def bfs(graph, start, goal):
    queue = deque([[start]])
    visited = {start}
    nodes_expanded = 0

    while queue:
        path = queue.popleft()
        current = path[-1]
        nodes_expanded += 1

        if current == goal:
            return path, nodes_expanded

        for neighbor in graph[current]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None, nodes_expanded

def uniform_cost_search(graph, start, goal):
    # Each item is: (total_cost, path)
    priority_queue = [(0, [start])]
    best_cost = {start: 0}
    nodes_expanded = 0

    while priority_queue:
        cost, path = heapq.heappop(priority_queue)
        current = path[-1]

        if cost > best_cost.get(current, float("inf")):
            continue

        nodes_expanded += 1

        if current == goal:
            return path, cost, nodes_expanded

        for neighbor, edge_cost in graph[current]:
            new_cost = cost + edge_cost

            if new_cost < best_cost.get(neighbor, float("inf")):
                best_cost[neighbor] = new_cost
                heapq.heappush(
                    priority_queue,
                    (new_cost, path + [neighbor])
                )

    return None, float("inf"), nodes_expanded

def depth_limited_search(graph, current, goal, limit, path, counter):
    counter[0] += 1
    path = path + [current]

    if current == goal:
        return path

    if limit == 0:
        return None

    for neighbor in graph[current]:
        # Avoid cycles in the current path
        if neighbor not in path:
            result = depth_limited_search(
                graph,
                neighbor,
                goal,
                limit - 1,
                path,
                counter
            )

            if result is not None:
                return result

    return None


def iterative_deepening_search(graph, start, goal, max_depth=20):
    total_nodes_expanded = 0

    for depth in range(max_depth + 1):
        counter = [0]

        result = depth_limited_search(
            graph,
            start,
            goal,
            depth,
            [],
            counter
        )

        total_nodes_expanded += counter[0]

        if result is not None:
            return result, depth, total_nodes_expanded

    return None, -1, total_nodes_expanded


# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------

def calculate_path_cost(path, weighted_graph):
    if path is None:
        return None

    total_cost = 0

    for i in range(len(path) - 1):
        current = path[i]
        next_node = path[i + 1]

        for neighbor, cost in weighted_graph[current]:
            if neighbor == next_node:
                total_cost += cost
                break

    return total_cost


def print_path(path):
    if path is None:
        return "No path found"

    return " -> ".join(path)

if __name__ == "__main__":

    print("=" * 60)
    print("       EMERGENCY RESCUE ROUTE PLANNER")
    print("=" * 60)
    print(f"Start location : {START}")
    print(f"Patient        : {GOAL}")

    # BFS
    bfs_path, bfs_nodes = bfs(graph, START, GOAL)

    print("\n[1] Breadth-First Search")
    print("Path           :", print_path(bfs_path))
    print("Path length    :", len(bfs_path) - 1)
    print("Path cost      :", calculate_path_cost(bfs_path, weighted_graph))
    print("Nodes expanded :", bfs_nodes)

    # Uniform Cost Search
    ucs_path, ucs_cost, ucs_nodes = uniform_cost_search(
        weighted_graph,
        START,
        GOAL
    )

    print("\n[2] Uniform Cost Search")
    print("Path           :", print_path(ucs_path))
    print("Minimum cost   :", ucs_cost)
    print("Nodes expanded :", ucs_nodes)

    # Iterative Deepening Search
    ids_path, ids_depth, ids_nodes = iterative_deepening_search(
        graph,
        START,
        GOAL
    )

    print("\n[3] Iterative Deepening Search")
    print("Path           :", print_path(ids_path))
    print("Depth reached  :", ids_depth)
    print("Path cost      :", calculate_path_cost(ids_path, weighted_graph))
    print("Nodes expanded :", ids_nodes)

    print("\n" + "=" * 60)
    print("RECOMMENDATION")
    print("=" * 60)
    print("The cheapest route is:")
    print(print_path(ucs_path))
    print("Total cost:", ucs_cost)
