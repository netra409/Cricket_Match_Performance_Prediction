
CREATE DATABASE agriculture_db;

USE agriculture_db;

CREATE TABLE crop_yield_predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    actual_yield FLOAT,
    predicted_yield FLOAT
);

SELECT * FROM crop_yield_predictions;

SELECT COUNT(*) AS total_records
FROM crop_yield_predictions;

SELECT AVG(actual_yield) AS avg_actual_yield
FROM crop_yield_predictions;

SELECT AVG(predicted_yield) AS avg_predicted_yield
FROM crop_yield_predictions;

SELECT 
    actual_yield,
    predicted_yield,
    ABS(actual_yield - predicted_yield) AS prediction_error
FROM crop_yield_predictions;

SELECT MAX(predicted_yield) AS highest_prediction
FROM crop_yield_predictions;

SELECT MIN(predicted_yield) AS lowest_prediction
FROM crop_yield_predictions;