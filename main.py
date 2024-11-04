import numpy as np
import matplotlib.pyplot as plt
from collections import deque
from matplotlib.animation import FuncAnimation
from statsmodels.tsa.holtwinters import ExponentialSmoothing

# Data Stream Simulation
def data_stream_simulator(num_points=1000, anomaly_chance=0.01):
    """
    Generator function that simulates a data stream with regular patterns,
    seasonality, random noise, and occasional anomalies.
    """
    for t in range(num_points):
        # Regular sine pattern with seasonality and noise
        base_pattern = np.sin(t * 0.1)
        seasonal_pattern = np.sin(t * 0.01) * 10
        noise = np.random.normal(0, 0.5)
        value = base_pattern + seasonal_pattern + noise

        # Anomaly injection with a small probability
        if np.random.rand() < anomaly_chance:
            value += np.random.normal(15, 5)

        yield value

# Anomaly Detection
# Rolling Z-Score for Quick Anomaly Detection
def rolling_z_score(data, window_size=50, threshold=3):
    if len(data) < window_size:
        return False  # Not enough data yet
    window = list(data)[-window_size:]  # Convert deque to list for slicing
    mean, std = np.mean(window), np.std(window)
    z_score = abs((data[-1] - mean) / std)
    return z_score > threshold

# Holt-Winters Seasonal Model for Seasonal Anomaly Detection
def holt_winters_forecast(data, seasonal_periods=10):
    if len(data) < seasonal_periods * 2:
        return data[-1]  # Not enough data for seasonality
    model = ExponentialSmoothing(data, trend="add", seasonal="add", seasonal_periods=seasonal_periods)
    model_fit = model.fit()
    forecast = model_fit.forecast(1)
    return forecast[0]

# Combined Anomaly Detection Function
def detect_anomalies(stream, window_size=50, z_threshold=3, seasonal_periods=10):
    data = deque(maxlen=window_size * 2)
    for value in stream:
        data.append(value)

        # Detect anomalies using rolling z-score and Holt-Winters forecast
        z_score_anomaly = rolling_z_score(data, window_size, z_threshold)
        forecast_value = holt_winters_forecast(list(data), seasonal_periods)
        holt_winters_anomaly = abs(value - forecast_value) > z_threshold * np.std(data)

        yield value, z_score_anomaly, holt_winters_anomaly

# Real-Time Visualization
def plot_stream(num_points=500, window_size=50, z_threshold=3, seasonal_periods=10, anomaly_chance=0.01):
    """
    Visualize the data stream and detected anomalies in real-time.
    """
    stream = data_stream_simulator(num_points=num_points, anomaly_chance=anomaly_chance)
    detector = detect_anomalies(stream, window_size=window_size, z_threshold=z_threshold, seasonal_periods=seasonal_periods)

    data = deque(maxlen=num_points)
    anomalies = deque(maxlen=num_points)

    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2, label="Data Stream")
    anomaly_points, = ax.plot([], [], "ro", markersize=5, label="Anomalies")  # Red dots for all anomalies
    ax.legend(loc="upper right")

    def init():
        ax.set_xlim(0, num_points)
        ax.set_ylim(-20, 40)
        return line, anomaly_points

    def update(frame):
        try:
            value, z_score_anomaly, holt_winters_anomaly = next(detector)
        except StopIteration:
            return line, anomaly_points  # Stop if stream is exhausted

        data.append(value)

        # If any type of anomaly is detected, add to anomalies deque
        if z_score_anomaly or holt_winters_anomaly:
            anomalies.append((len(data) - 1, value))

        # Update line and anomaly points
        line.set_data(range(len(data)), data)
        
        # Update anomaly points if there are any
        if anomalies:
            anomaly_x, anomaly_y = zip(*anomalies)
            anomaly_points.set_data(anomaly_x, anomaly_y)
        else:
            anomaly_points.set_data([], [])

        # Dynamically adjust y-limits based on current data
        ax.set_ylim(min(data) - 5, max(data) + 5)

        return line, anomaly_points

    ani = FuncAnimation(fig, update, frames=num_points, init_func=init, blit=True, interval=50)
    plt.show()


# Running the Simulation and Detection
if __name__ == "__main__":
    plot_stream(num_points=500, window_size=50, z_threshold=3, seasonal_periods=10, anomaly_chance=0.02)
