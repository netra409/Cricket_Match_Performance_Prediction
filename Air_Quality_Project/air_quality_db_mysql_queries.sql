CREATE DATABASE air_quality_db;

USE air_quality_db;

SHOW TABLES;

SELECT * FROM air_quality;

SELECT AVG(AQI) AS Average_AQI
FROM air_quality;

SELECT MAX(AQI) AS Maximum_AQI
FROM air_quality;

SELECT pollution_alert, COUNT(*) AS Total
FROM air_quality
GROUP BY pollution_alert;

SELECT hour, AVG(AQI) AS Avg_AQI
FROM air_quality
GROUP BY hour
ORDER BY hour;