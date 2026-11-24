-- calculate the total driving time for each method in each segment
-- I join each stop (v1) with the next stop (v2) by using position + 1
-- then I get the travel time between them from the travel table

DROP VIEW IF EXISTS route_times;

CREATE VIEW route_times AS
SELECT v1.segment,
       v1.method,
       SUM(t.seconds) AS total_seconds
FROM visits v1
JOIN visits v2
  ON v1.segment = v2.segment
 AND v1.method = v2.method
 AND v2.position = v1.position + 1
JOIN travel t
  ON t.segment = v1.segment
 AND t.origin = v1.stop
 AND t.destination = v2.stop
GROUP BY v1.segment, v1.method;

SELECT * FROM route_times;
