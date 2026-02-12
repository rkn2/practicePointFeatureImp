"""
Generate condition_distribution.png
Shows distribution of building condition ratings in the dataset.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

def generate_condition_distribution():
    # Load processed data
    if os.path.exists('../../processed_data.csv'):
        df = pd.read_csv('../../processed_data.csv')
    elif os.path.exists('../processed_data.csv'):
        df = pd.read_csv('../processed_data.csv')
    else:
        print("Error: processed_data.csv not found.")
        return
    
    # Set style
    sns.set_style("white")
    
    plt.figure(figsize=(8, 5))
    plt.grid(False)
    
    # Get 5 colors from viridis for consistency
    colors = sns.color_palette("viridis", 5)
    
    # Create countplot
    sns.countplot(x='Condition_Rating', data=df, order=[1,2,3,4,5], palette=colors)
    plt.title('How many buildings are in each condition category?')
    plt.xlabel('Condition Rating (1=Good, 5=Poor)')
    plt.ylabel('Number of Buildings')
    
    # Save
    output_path = '../condition_distribution.png'
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    generate_condition_distribution()
