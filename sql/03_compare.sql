-- Q1. total driving minutes for each method in each segment
SELECT segment, method, ROUND(total_seconds / 60.0, 2) AS minutes
FROM route_times
ORDER BY segment, method;

-- Q2. put the 3 methods side by side
SELECT segment,
       ROUND(SUM(CASE WHEN method = 'Driver' THEN total_seconds END) / 60.0, 2) AS driver_min,
       ROUND(SUM(CASE WHEN method = 'Nearest' THEN total_seconds END) / 60.0, 2) AS nearest_min,
       ROUND(SUM(CASE WHEN method = 'Exact' THEN total_seconds END) / 60.0, 2) AS exact_min
FROM route_times
GROUP BY segment
ORDER BY segment;

-- Q3. total for all 4 segments
SELECT method, ROUND(SUM(total_seconds) / 60.0, 2) AS total_minutes
FROM route_times
GROUP BY method
ORDER BY total_minutes;

-- Q4. how much slower is nearest first compared to the best order
SELECT segment,
       ROUND(SUM(CASE WHEN method = 'Nearest' THEN total_seconds END)
           - SUM(CASE WHEN method = 'Exact' THEN total_seconds END), 1) AS extra_seconds,
       ROUND((SUM(CASE WHEN method = 'Nearest' THEN total_seconds END)
           - SUM(CASE WHEN method = 'Exact' THEN total_seconds END)) * 100.0
           / SUM(CASE WHEN method = 'Exact' THEN total_seconds END), 1) AS pct_slower
FROM route_times
GROUP BY segment
ORDER BY segment;
