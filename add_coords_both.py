import pandas as pd
import numpy as np

# Use seed for consistency
np.random.seed(42)

for csv_file in ['heritage_data.csv', 'processed_data.csv']:
    try:
        df = pd.read_csv(csv_file)
        if 'Latitude' not in df.columns:
            # e.g., somewhere in PA, ~40.8, -77.8
            df['Latitude'] = 40.8 + np.random.randn(len(df)) * 0.1
            df['Longitude'] = -77.8 + np.random.randn(len(df)) * 0.1
            df.to_csv(csv_file, index=False)
            print(f"Added Latitude and Longitude to {csv_file}")
        else:
            print(f"{csv_file} already has spatial coordinates")
    except Exception as e:
        print(f"Failed to process {csv_file}: {e}")

