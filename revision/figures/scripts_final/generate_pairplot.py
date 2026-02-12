"""
Generate pairplot.png
Shows pairwise relationships among key continuous variables.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generate_pairplot():
    # Load data
    if os.path.exists('../../processed_data.csv'):
        df = pd.read_csv('../../processed_data.csv')
    elif os.path.exists('../processed_data.csv'):
        df = pd.read_csv('../processed_data.csv')
    else:
        print("Error: processed_data.csv not found.")
        return
    
    # Set style
    sns.set_style("white")
    plt.grid(False)
    
    # Ensure Condition_Rating is sorted for the legend
    hue_order = sorted(df['Condition_Rating'].unique())
    
    # Use viridis colors for consistency
    colors = sns.color_palette("viridis", 5)
    
    # Create pairplot with specific variables
    g = sns.pairplot(df,
                     vars=['Crack_Width_mm', 'Soil_Moisture_Index'],
                     hue='Condition_Rating',
                     palette=colors,
                     hue_order=hue_order)
    
    # Turn off grid for all subplots
    for ax in g.axes.flatten():
        ax.grid(False)
    
    g.fig.suptitle('Pairwise Relationships', y=1.02)
    
    # Save
    output_path = '../pairplot.png'
    g.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    generate_pairplot()
