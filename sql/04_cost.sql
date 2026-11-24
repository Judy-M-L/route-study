-- how much is the extra time worth?
-- assumption: driver costs $30 per hour (just an example, not real Amazon data)

SELECT method,
       ROUND((SUM(total_seconds) - (SELECT SUM(total_seconds) FROM route_times WHERE method = 'Exact')) / 60.0, 2) AS extra_minutes,
       ROUND((SUM(total_seconds) - (SELECT SUM(total_seconds) FROM route_times WHERE method = 'Exact')) / 3600.0 * 30, 2) AS extra_cost_usd
FROM route_times
GROUP BY method
ORDER BY extra_minutes DESC;
