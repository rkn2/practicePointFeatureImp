import pandas as pd
import numpy as np
import random

# Set random seed for reproducibility
np.random.seed(42)
random.seed(42)

def generate_heritage_data(n_samples=200):
    data = {
        'Building_ID': [f'B{str(i).zfill(3)}' for i in range(1, n_samples + 1)],
        'District_ID': np.random.choice(['North', 'South', 'East', 'West', 'Central'], n_samples),
        'Construction_Year': np.random.randint(1800, 1950, n_samples),
        'Material_Type': np.random.choice(['Brick', 'Stone', 'Concrete', 'Wood'], n_samples, p=[0.4, 0.3, 0.2, 0.1]),
        'Foundation_Type': np.random.choice(['Shallow', 'Deep', 'Pile'], n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Generate correlated environmental and structural variables
    # Logic: 
    # - High Rainfall -> High Soil Moisture
    # - High Temp Range + Moisture -> High Crack Width
    # - Older buildings -> Worse condition
    
    # Environmental Variables
    df['Avg_Temp_C'] = np.random.normal(15, 5, n_samples)
    df['Temp_Range_C'] = np.random.normal(10, 3, n_samples) # Seasonal fluctuation
    df['Annual_Rainfall_mm'] = np.random.normal(800, 200, n_samples)
    df['Humidity_Percent'] = np.random.normal(60, 15, n_samples).clip(20, 100)
    df['Freeze_Thaw_Cycles'] = np.random.poisson(10, n_samples)
    
    # Derived/Correlated Variables
    # Soil moisture is correlated with rainfall and humidity
    df['Soil_Moisture_Index'] = (df['Annual_Rainfall_mm'] * 0.01 + df['Humidity_Percent'] * 0.1 + np.random.normal(0, 2, n_samples)).clip(0, 20)
    
    # Structural Variables
    # Crack width increases with age, temp range, and soil moisture
    age_factor = (2025 - df['Construction_Year']) / 100
    df['Crack_Width_mm'] = (0.5 * age_factor + 
                            0.1 * df['Temp_Range_C'] + 
                            0.2 * df['Soil_Moisture_Index'] + 
                            np.random.normal(0, 0.5, n_samples)).clip(0, 10)
    
    df['Salt_Deposition_g_m2'] = np.abs(np.random.normal(5, 2, n_samples))
    
    # Outcome Variables
    # Condition Rating (1=Good, 5=Poor)
    # Driven by Crack Width, Salt, and Freeze Thaw
    condition_score = (0.4 * df['Crack_Width_mm'] + 
                       0.2 * df['Salt_Deposition_g_m2'] + 
                       0.1 * df['Freeze_Thaw_Cycles'] + 
                       np.random.normal(0, 1, n_samples))
    
    # Normalize to 1-5 scale
    df['Condition_Rating'] = pd.qcut(condition_score, 5, labels=[1, 2, 3, 4, 5]).astype(int)
    
    # Intervention Urgency (0-100)
    df['Intervention_Urgency'] = (condition_score * 10 + np.random.normal(0, 5, n_samples)).clip(0, 100)
    
    # Introduce some missing values to make data prep interesting
    for col in ['Crack_Width_mm', 'Soil_Moisture_Index', 'Salt_Deposition_g_m2']:
        mask = np.random.random(n_samples) < 0.05 # 5% missing
        df.loc[mask, col] = np.nan
        
    return df

if __name__ == "__main__":
    df = generate_heritage_data()
    output_path = "heritage_data.csv"
    df.to_csv(output_path, index=False)
    print(f"Generated {output_path} with {len(df)} rows.")
