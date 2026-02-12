
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import shutil

def run():
    # Load processed data
    if os.path.exists('processed_data.csv'):
        df = pd.read_csv('processed_data.csv')
    else:
        print("Error: processed_data.csv not found.")
        return

    # Use a style without grid
    sns.set_style("white")
    
    plt.figure(figsize=(8, 5))
    
    # Create the countplot
    # Explicitly turn off grid
    plt.grid(False)
    
    # Ensure strict color consistency
    # Get 5 colors from viridis
    colors = sns.color_palette("viridis", 5)
    
    sns.countplot(x='Condition_Rating', data=df, order=[1,2,3,4,5], palette=colors)
    plt.title('How many buildings are in each condition category?')
    plt.xlabel('Condition Rating (1=Good, 5=Poor)')
    plt.ylabel('Number of Buildings')


    # Save to main figures directory
    if not os.path.exists('figures'):
        os.makedirs('figures')
    
    output_path = 'figures/condition_distribution.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved update to {output_path}")
    plt.close()

    # Copy to revision/figures if it exists
    revision_figs = 'revision/figures'
    if os.path.exists(revision_figs):
        shutil.copy(output_path, os.path.join(revision_figs, 'condition_distribution.png'))
        print(f"Copied to {revision_figs}/condition_distribution.png")

if __name__ == "__main__":
    run()
