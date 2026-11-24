-- look at the data first

SELECT * FROM stops LIMIT 10;

SELECT * FROM travel LIMIT 10;

-- how many stops in each segment (should be 10)
SELECT segment, COUNT(*) AS num_stops
FROM stops
GROUP BY segment;

-- how many travel time rows in each segment (10 x 10 = 100)
SELECT segment, COUNT(*) AS num_rows
FROM travel
GROUP BY segment;

-- shortest and longest travel time (not counting a stop to itself)
SELECT segment, MIN(seconds) AS min_sec, MAX(seconds) AS max_sec, ROUND(AVG(seconds), 1) AS avg_sec
FROM travel
WHERE origin <> destination
GROUP BY segment;

-- check the visits table
SELECT * FROM visits WHERE segment = 1 ORDER BY method, position;
