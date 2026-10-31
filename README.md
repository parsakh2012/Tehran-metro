# Tehran Metro Route Finder

A small Python program, inspired by CS50's [Degrees](https://cs50.harvard.edu/ai/2024/projects/0/degrees) project, that finds the shortest route between two Tehran Metro stations. Give it an origin and a destination and it prints the route with the fewest stops, which line to ride on each leg, and where to transfer.

## Files

- `metro.py` - the program (breadth-first search over the station graph)
- `metro.csv` - the dataset: 140 unique stations across Lines 1-7
- `README.md` - this file

## Requirements

Python 3. No third-party packages are needed.

## Usage

1. Open a terminal and go to the project folder (where `metro.py` and `metro.csv` are):

   ```bash
   cd path/to/project
   ```

2. Run the program:

   ```bash
   python3 metro.py
   ```

   On Windows, use `python metro.py` if `python3` is not available.

3. Type the origin and destination when prompted:

   ```
   Origin station: Tajrish
   Destination station: Azadegan
   ```

4. The route is printed, and you are asked for another pair. Press Enter on an empty line to quit.

### Input tips

- Station names can be entered in English or Persian.
- Matching is case-insensitive and partial names work (for example `tajr`).
- If a partial name matches several stations, the program lists them so you can be more specific.

## Example output

```
22 stops: Tajrish (تجریش) -> Azadegan (آزادگان)
  Line 1: Tajrish -> Shahid Beheshti  (9 stops)
  Line 3: Shahid Beheshti -> Azadegan  (13 stops)
  Transfers: 1
  Full path: Tajrish > Gheytariyeh > ... > Azadegan
```

## How it works

1. `metro.csv` is read and consecutive stations on each line are connected to form a graph.
2. Stations with the same English name on different lines are treated as one node, which makes them transfer points.
3. Breadth-first search starts at the origin and expands one stop at a time, so the first time it reaches the destination it has found a route with the fewest stops.
4. The route is grouped by line so you can see where to change trains.

## Dataset

`metro.csv` has the columns `line, order, name_en, name_fa`, where `order` is the position of the station along its line.

Limitations:

- Stations under construction and the Imam Khomeini Airport branch of Line 1 are not included.
- The route is the one with the fewest stops, not the shortest travel time.
- Persian station names were written by hand and should be checked against the official metro map.

To fix or extend the data, edit `metro.csv` only.

## Data source

Station lists and interchanges: [List of Tehran Metro stations (Wikipedia)](https://en.wikipedia.org/wiki/List_of_Tehran_Metro_stations)
