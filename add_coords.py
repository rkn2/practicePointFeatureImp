import pandas as pd
import numpy as np

# Load heritage data
df = pd.read_csv('heritage_data.csv')

# Add Latitude and Longitude (e.g., somewhere in PA, ~40.8, -77.8)
np.random.seed(42)
df['Latitude'] = 40.8 + np.random.randn(len(df)) * 0.1
df['Longitude'] = -77.8 + np.random.randn(len(df)) * 0.1

# Save back to CSV
df.to_csv('heritage_data.csv', index=False)
print("Added Latitude and Longitude to heritage_data.csv")
