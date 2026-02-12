
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import shutil

def run():
    # Load data
    if os.path.exists('processed_data.csv'):
        df = pd.read_csv('processed_data.csv')
    else:
        print("Error: processed_data.csv not found.")
        return

    # Set style - remove grid
    sns.set_style("white")
    
    # Ensure Condition_Rating is sorted for the legend
    # Get unique values and sort them
    hue_order = sorted(df['Condition_Rating'].unique())
    
    # Create the pairplot
    # Explicitly turn off grid
    plt.grid(False)
    
    # Use vars to only plot the specific columns shown in the user's figure
    # effectively hiding Condition_Rating from the axes but using it for color
    colors = sns.color_palette("viridis", 5)

    g = sns.pairplot(df,
                 vars=['Crack_Width_mm', 'Soil_Moisture_Index'],
                 hue='Condition_Rating',
                 palette=colors,
                 hue_order=hue_order)
                 
    # Iterate over axes to ensure no grid
    for ax in g.axes.flatten():
        ax.grid(False)
        
    g.fig.suptitle('Pairwise Relationships', y=1.02)
    
    # Check if target directory exists
    if not os.path.exists('figures'):
        os.makedirs('figures')
        
    output_path = 'figures/pairplot.png'
    g.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved pairplot to {output_path}")
    plt.close()

    # Copy to revision folder
    revision_figs = 'revision/figures'
    if os.path.exists(revision_figs):
        shutil.copy(output_path, os.path.join(revision_figs, 'pairplot.png'))
        print(f"Copied to {revision_figs}/pairplot.png")

if __name__ == "__main__":
    run()
