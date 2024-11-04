# Anomaly_Detection

<img width="640" alt="Screenshot 2024-11-04 at 1 15 36 PM" src="https://github.com/user-attachments/assets/e3650660-54e7-4d77-b06c-f18d1ab8578f">

This Python script simulates a data stream with regular patterns, seasonality, random noise, and occasional anomalies. It incorporates real-time visualization of the data stream and detects anomalies using two methods: rolling Z-score and Holt-Winters forecasting.

## Features

- Simulates a continuous data stream with:
  - Regular sine wave patterns
  - Seasonal variations
  - Random noise
  - Anomalies injected with a specified probability
- Real-time visualization of the data stream
- Anomaly detection using:
  - Rolling Z-score method
  - Holt-Winters seasonal forecasting method
- Interactive plot updating dynamically as new data is generated

## Requirements

To run this script, you will need:

- Python 3.6 or higher
- The following Python packages:
  - `numpy`
  - `matplotlib`
  - `statsmodels`

You can install the required packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

To execute the script, simply run:

```bash
python3 main.py
```

## Data Stream Simulation Function

The ```data_stream_simulator``` function is a generator designed to simulate a data stream comprising regular patterns, seasonal variations, random noise, and occasional anomalies.

**Functionality**:

- **Regular Patterns**: The function generates a base sine wave pattern that represents a regular oscillation over time, scaled by a factor of 0.1.
- **Seasonality**: A seasonal component is added, represented by a sine wave with a longer period (scaled by 0.01) and amplified by a factor of 10 to simulate periodic trends.
- **Random Noise**: Random Gaussian noise is introduced to add variability to the data, making it more realistic and simulating real-world conditions.
- **Anomalies**: With a specified probability (anomaly_chance), the function randomly injects anomalies into the data. These anomalies are generated from a normal distribution centered around 15 with a standard deviation of 5, making them significantly deviant from the normal data points.
  
**Usage**:

The generator yields each simulated value sequentially, allowing for efficient memory usage and real-time data processing in applications like anomaly detection, forecasting, and time series analysis.

## Algorithms Used

### Rolling Z-Score

**Overview**:
The rolling Z-score method is a statistical technique used for detecting anomalies in time series data. It measures how many standard deviations a data point is from the mean of a specified window of data.

**Z-Score Calculation**

  ![7dd2138496f193151c4f652bf41689f3ed81bc95](https://github.com/user-attachments/assets/ebb041bb-b063-4322-bbe6-7abbf06efb53)


**Usage**:
In the script, ```the rolling_z_score``` function checks if the Z-score of the latest data point (within a defined rolling window) exceeds a certain threshold. It takes the following parameters:

  - ```data```: The input data stream
  - ```window_size```: The size of the window over which the mean and standard deviation are calculated
  - ```threshold```: The Z-score value above which a point is considered an anomaly.

**Application in Anomaly Detection**:
If the calculated Z-score of a data point exceeds the specified threshold (commonly set to 3), it is flagged as an anomaly, indicating that it is significantly different from the previous values in the rolling window.

### Holt-Winters Forecast

**Overview**:
The Holt-Winters method, also known as triple exponential smoothing, is a statistical technique used for forecasting time series data that exhibit both trend and seasonality. It extends simple exponential smoothing to capture seasonality in the data.

**Components**:
- Level: The smoothed value of the series at the current time.
- Trend: The smoothed estimate of the trend at the current time.
- Seasonality: The smoothed seasonal component, adjusted for periodic fluctuations.

**Usage**:
- In the script, ```the holt_winters_forecast``` function employs the Holt-Winters method to forecast the next data point based on historical data. The function takes the following parameters:
  - ```data```: The input time series data for forecasting. 
  - ```seasonal_periods```: The number of observations that make up one season (e.g., for daily data with weekly seasonality, this would be 7).

**Application in Anomaly Detection**:
The forecasted value is compared to the actual incoming data point. If the absolute difference between the two exceeds a specified threshold (in this case, a multiple of the       standard deviation of the data), the current point is flagged as an anomaly.




