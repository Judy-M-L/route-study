# Amazon Delivery Route Analysis (SQL + Python)

## What I wanted to check
Is "always go to the nearest stop next" the fastest way to order delivery stops? I tested it on real Amazon delivery routes.

I compared 3 orders:
- **Driver:** the order the real Amazon driver used
- **Nearest:** always go to the closest stop not visited yet
- **Exact:** the fastest possible order, found by trying every order

## Data I used
- 2021 Amazon Last Mile Routing Research Challenge (public data on AWS). Real routes from 5 US cities in 2018.
- 4 routes, 10 stops from the middle of each. I kept it small so I could try every order (8 middle stops = 40,320 orders).
- First and last stop stay fixed for all 3 orders.
- `data/stops.csv`: stops and the driver's actual order
- `data/travel.csv`: Amazon's estimated travel time in seconds between every pair of stops

## Files
- `build.py`: loads the csv files into SQLite and makes the 3 orders
- `sql/01_explore.sql`: checking the data
- `sql/02_route_times.sql`: total time for each order
- `sql/03_compare.sql`: comparing the 3 orders
- `sql/04_cost.sql`: what the extra time costs

## What I found

| Segment | Driver (min) | Nearest (min) | Exact (min) |
|---|---:|---:|---:|
| 1 | 5.86 | 7.95 | 5.86 |
| 2 | 17.04 | 18.41 | 16.47 |
| 3 | 10.56 | 12.78 | 10.56 |
| 4 | 31.97 | 30.15 | 30.07 |
| **Total** | **65.43** | **69.28** | **62.96** |

- Nearest was slower than the driver in 3 of 4 segments. In segment 1 it was 35.5% slower than the best order.
- The driver already had the best order in segments 1 and 3.
- In segment 1, nearest and the driver match for the first 5 stops. After NY, nearest goes to TW (closest), the driver goes to OJ. Nearest has to come back for OJ later and ends up 125 seconds slower.
- At $30/hour (my assumption), the extra time vs the best order is about $3.16 for nearest and $1.24 for the driver. Small, because the sample is small.

## What this doesn't cover
- Only 4 segments of 10 stops. Not enough to say how often this happens across Amazon.
- Driving time only. No parking, delivery time, or delivery time windows.
- $30/hour is my assumption, not Amazon's real cost.

## Tools
- SQLite
- Python (csv, sqlite3, itertools)

## How to run
```
python3 build.py
sqlite3 -header -column routes.sqlite < sql/03_compare.sql
sqlite3 -header -column routes.sqlite < sql/04_cost.sql
```

## What I used in this project
- Self join on `position + 1` to pair each stop with the next one
- `CASE WHEN` to put the 3 orders in separate columns
- A view (`route_times`) so the other queries can reuse the totals
- `itertools.permutations` in Python to try every order

## Next
- Use full routes instead of 10 stops. Trying every order won't work there (100 stops is way too many), so I'd need a different method.
- Run more routes to see how often nearest loses.

## Data source
Merchán, D., Arora, J., Pachon, J., Konduri, K., Winkenbach, M., Parks, S., & Noszek, J. (2022). *2021 Amazon Last Mile Routing Research Challenge: Data Set.* Transportation Science. https://doi.org/10.1287/trsc.2022.1173

Data: https://registry.opendata.aws/amazon-last-mile-challenges/ (CC BY-NC 4.0). I selected 4 routes, took 10 stops from each, and rounded travel times.
