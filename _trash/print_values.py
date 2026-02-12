
import pandas as pd
import seaborn as sns
import matplotlib.colors as mcolors

def run():
    # 1. Load Data & Get Counts
    try:
        df = pd.read_csv('processed_data.csv')
        counts = df['Condition_Rating'].value_counts().sort_index()
        print("--- Condition Rating Counts (Figure 1: Bar Chart Data) ---")
        print(counts)
        print("\n")
    except Exception as e:
        print(f"Error reading data: {e}")

    # 2. Get Colors
    # We used sns.color_palette("viridis", 5) in both scripts
    colors = sns.color_palette("viridis", 5)
    
    print("--- Color Values (Used in Figure 1 & Figure 4) ---")
    print(f"{'Rating':<10} {'RGB':<30} {'Hex':<10}")
    print("-" * 50)
    
    for i, color in enumerate(colors):
        rating = i + 1
        rgb = tuple(round(c, 4) for c in color)
        hex_val = mcolors.to_hex(color)
        print(f"{rating:<10} {str(rgb):<30} {hex_val:<10}")

if __name__ == "__main__":
    run()
