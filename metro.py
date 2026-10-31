import csv
from collections import deque, defaultdict
from pathlib import Path

DATA = Path(__file__).with_name("metro.csv")


def load_data():
    """Read metro.csv and build the station graph."""
    stations = {}  # English name -> Persian name
    graph = defaultdict(dict)  # station -> {neighbor: line}
    lines = defaultdict(list)  # line -> [(order, station), ...]

    with open(DATA, encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            stations[row["name_en"]] = row["name_fa"]
            lines[row["line"]].append((int(row["order"]), row["name_en"]))

    # Connect each station to the next one on the same line.
    # Interchange stations share a name, so they become one node.
    for line, items in lines.items():
        names = [name for _, name in sorted(items)]
        for a, b in zip(names, names[1:]):
            graph[a][b] = line
            graph[b][a] = line
    return stations, graph


def find_station(text, stations):
    """Match English or Persian text (case-insensitive, partial OK)."""
    t = text.strip().lower()
    exact = [en for en, fa in stations.items() if t in (en.lower(), fa)]
    if exact:
        return exact
    return [en for en, fa in stations.items() if t in en.lower() or text.strip() in fa]


def shortest_path(source, target, graph):
    """Breadth-first search: returns [(line, station), ...] or None."""
    if source == target:
        return []
    queue = deque([source])
    parent = {source: None}  # station -> (previous station, line used)

    while queue:
        node = queue.popleft()
        for neighbor, line in graph[node].items():
            if neighbor in parent:
                continue
            parent[neighbor] = (node, line)
            if neighbor == target:
                # Walk back from the target to rebuild the route.
                path = []
                while parent[neighbor] is not None:
                    node, line = parent[neighbor]
                    path.append((line, neighbor))
                    neighbor = node
                return path[::-1]
            queue.append(neighbor)
    return None


def print_route(source, target, path, stations):
    print(f"{len(path)} stops: {source} ({stations[source]}) -> {target} ({stations[target]})")

    # Group consecutive stops on the same line into legs.
    legs = []
    for line, station in path:
        if legs and legs[-1][0] == line:
            legs[-1][1].append(station)
        else:
            legs.append((line, [station]))

    start = source
    for line, stops in legs:
        print(f"  Line {line}: {start} -> {stops[-1]} ({len(stops)} stops)")
        start = stops[-1]
    print(f"  Transfers: {max(len(legs) - 1, 0)}")


def ask(prompt, stations):
    """Ask until a single station matches. Empty input returns None."""
    while True:
        text = input(prompt).strip()
        if not text:
            return None
        matches = find_station(text, stations)
        if len(matches) == 1:
            return matches[0]
        if matches:
            print("  Did you mean: " + "; ".join(matches[:8]))
        else:
            print("  Station not found.")


def main():
    stations, graph = load_data()
    print(f"Loaded {len(stations)} stations. Press Enter on an empty line to quit.")
    while True:
        source = ask("Origin station: ", stations)
        if source is None:
            break
        target = ask("Destination station: ", stations)
        if target is None:
            break
        path = shortest_path(source, target, graph)
        if path is None:
            print("No route found.")
        else:
            print_route(source, target, path, stations)
        print()


if __name__ == "__main__":
    main()
