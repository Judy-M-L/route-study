# Amazon Delivery Route Analysis (SQL + Python)

## Overview
Delivery drivers have to decide which stop to go to next. A simple rule is "always go to the nearest stop". In this project I wanted to check if this rule actually gives the shortest driving time, using real Amazon delivery data.

I compared 3 ways of ordering the stops:
- **Driver:** the order the real Amazon driver used
- **Nearest:** always go to the closest stop that hasn't been visited
- **Exact:** the fastest possible order (found by trying every order)

## Dataset
- Source: 2021 Amazon Last Mile Routing Research Challenge (public data on AWS)
- Real Amazon delivery routes from 5 US cities in 2018
- I used 4 routes and took 10 stops from the middle of each route. I kept it small so I could test every possible order (8 middle stops = 40,320 orders)
- The first and last stop stay the same for all 3 methods
- Files:
  - `data/stops.csv`: the stops and the driver's actual order
  - `data/travel.csv`: Amazon's estimated travel time (seconds) between every pair of stops

## Questions
1. How long does each method take?
2. Is nearest first always the fastest?
3. How close is the real driver to the best possible order?
4. How much money is the difference worth?

## Project Structure
```
route-study/
├── README.md
├── build.py              # loads csv into SQLite and makes the 3 orders
├── routes.sqlite
├── data/
│   ├── stops.csv
│   └── travel.csv
└── sql/
    ├── 01_explore.sql    # looking at the data
    ├── 02_route_times.sql # total time for each method
    ├── 03_compare.sql    # comparing the 3 methods
    └── 04_cost.sql       # cost of the extra time
```

## Key Findings

| Segment | Driver (min) | Nearest (min) | Exact (min) |
|---|---:|---:|---:|
| 1 | 5.86 | 7.95 | 5.86 |
| 2 | 17.04 | 18.41 | 16.47 |
| 3 | 10.56 | 12.78 | 10.56 |
| 4 | 31.97 | 30.15 | 30.07 |
| **Total** | **65.43** | **69.28** | **62.96** |

- Nearest first was **slower than the driver in 3 out of 4 segments**. In segment 1 it was 35.5% slower than the best order.
- The real driver already used the best order in 2 segments (1 and 3).
- So "go to the nearest stop" is not always the fastest. Sometimes taking a slightly longer trip now saves time later.
- If a driver costs $30/hour, the extra time costs about $3.16 for nearest first and $1.24 for the driver order (compared to the best order). This is a very small sample so the dollar amount is small.

## Limitations
- Only 4 segments with 10 stops each, so I can't say how often this happens across all of Amazon.
- I only looked at driving time. Parking, time to deliver, and delivery time windows are not included.
- $30/hour is my assumption, not real Amazon cost.

## Tools
- SQLite
- Python (csv, sqlite3, itertools)

## How to Run
```
python3 build.py
sqlite3 -header -column routes.sqlite < sql/03_compare.sql
sqlite3 -header -column routes.sqlite < sql/04_cost.sql
```

## What I Learned
- How to use a self join (`position + 1`) to connect each stop with the next stop
- Using `CASE WHEN` to put different methods in separate columns
- A simple rule like nearest first can look good but isn't always the best
- Trying every order only works for small problems. With 100 stops it would be impossible, so real routing needs smarter methods

## Data Source
Merchán, D., Arora, J., Pachon, J., Konduri, K., Winkenbach, M., Parks, S., & Noszek, J. (2022). *2021 Amazon Last Mile Routing Research Challenge: Data Set.* Transportation Science. https://doi.org/10.1287/trsc.2022.1173

Data: https://registry.opendata.aws/amazon-last-mile-challenges/ (CC BY-NC 4.0). I selected 4 routes, took 10 stops from each, and rounded travel times.
