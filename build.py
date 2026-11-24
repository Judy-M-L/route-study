# build.py
# This script loads the csv files into a SQLite database
# and creates 3 visit orders for each segment: Driver, Nearest, Exact

import csv
import sqlite3
import itertools

conn = sqlite3.connect('routes.sqlite')
cur = conn.cursor()

# make the tables (drop first so I can run it again)
cur.execute('DROP TABLE IF EXISTS stops')
cur.execute('DROP TABLE IF EXISTS travel')
cur.execute('DROP TABLE IF EXISTS visits')
cur.execute('CREATE TABLE stops (segment INTEGER, route_id TEXT, driver_position INTEGER, stop TEXT)')
cur.execute('CREATE TABLE travel (segment INTEGER, origin TEXT, destination TEXT, seconds REAL)')
cur.execute('CREATE TABLE visits (segment INTEGER, method TEXT, position INTEGER, stop TEXT)')

# load stops.csv
with open('data/stops.csv') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        cur.execute('INSERT INTO stops VALUES (?, ?, ?, ?)', row)

# load travel.csv
with open('data/travel.csv') as f:
    reader = csv.reader(f)
    next(reader)  # skip header
    for row in reader:
        cur.execute('INSERT INTO travel VALUES (?, ?, ?, ?)', row)


def route_time(route, times):
    # add up the travel time between each pair of stops
    total = 0
    for i in range(len(route) - 1):
        total = total + times[(route[i], route[i + 1])]
    return total


def nearest_neighbor(start, middle, end, times):
    # always go to the closest stop that is not visited yet
    route = [start]
    left = middle.copy()
    current = start
    while len(left) > 0:
        best_stop = None
        best_time = 999999
        for s in left:
            if times[(current, s)] < best_time:
                best_time = times[(current, s)]
                best_stop = s
        route.append(best_stop)
        left.remove(best_stop)
        current = best_stop
    route.append(end)
    return route


def brute_force(start, middle, end, times):
    # try every possible order (8 stops = 40320 orders)
    best_route = None
    best_total = 999999
    for p in itertools.permutations(middle):
        route = [start] + list(p) + [end]
        total = route_time(route, times)
        if total < best_total:
            best_total = total
            best_route = route
    return best_route


for segment in [1, 2, 3, 4]:
    # driver order
    cur.execute('SELECT stop FROM stops WHERE segment = ? ORDER BY driver_position', (segment,))
    driver = [row[0] for row in cur.fetchall()]

    # travel times as a dictionary
    times = {}
    cur.execute('SELECT origin, destination, seconds FROM travel WHERE segment = ?', (segment,))
    for origin, destination, seconds in cur.fetchall():
        times[(origin, destination)] = seconds

    # first and last stop stay the same
    start = driver[0]
    end = driver[-1]
    middle = driver[1:-1]

    nearest = nearest_neighbor(start, middle, end, times)
    exact = brute_force(start, middle, end, times)

    print('Segment', segment)
    print('  Driver: ', driver, round(route_time(driver, times) / 60, 2), 'min')
    print('  Nearest:', nearest, round(route_time(nearest, times) / 60, 2), 'min')
    print('  Exact:  ', exact, round(route_time(exact, times) / 60, 2), 'min')

    for method, route in [('Driver', driver), ('Nearest', nearest), ('Exact', exact)]:
        for i in range(len(route)):
            cur.execute('INSERT INTO visits VALUES (?, ?, ?, ?)', (segment, method, i, route[i]))

# create the route_times view
with open('sql/02_route_times.sql') as f:
    cur.executescript(f.read())

conn.commit()
conn.close()
print('done!')
