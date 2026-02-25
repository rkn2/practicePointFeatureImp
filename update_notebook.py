import nbformat as nbf
import json
import os

NOTEBOOK_PATH = "04_visualization.ipynb"

# Load notebook
with open(NOTEBOOK_PATH, 'r') as f:
    nb = nbf.read(f, as_version=4)

# Check if the map section already exists
has_map = any("groundwater risk map" in str(cell.source).lower() for cell in nb.cells)

if not has_map:
    # Add markdown
    md_cell = nbf.v4.new_markdown_cell("""## 4. Spatial Distribution (Groundwater Risk Map)
This map visualization correlates building condition with geographic locations, creating a groundwater risk map similar to the one presented in our paper. We use generated coordinates simulating sites across Pennsylvania.""")
    
    # Add code cell for map
    code_cell = nbf.v4.new_code_cell("""# Spatial Distribution of Condition Rating
import matplotlib.pyplot as plt
import seaborn as sns

plt.figure(figsize=(10, 8))
plt.grid(False)

# Make sure we have the coordinates
if 'Latitude' in df.columns and 'Longitude' in df.columns:
    scatter = plt.scatter(df['Longitude'], df['Latitude'], 
                         c=df['Condition_Rating'], 
                         cmap='viridis', 
                         s=100, 
                         alpha=0.7,
                         edgecolor='black',
                         linewidth=0.5)
    
    plt.colorbar(scatter, label='Condition Rating (1=Good, 5=Poor)')
    plt.title('Spatial Distribution of Building Condition\\n(Groundwater Risk Correlation)', 
              fontsize=14, fontweight='bold')
    plt.xlabel('Longitude', fontsize=12)
    plt.ylabel('Latitude', fontsize=12)
    plt.tight_layout()
    plt.show()
else:
    print("Spatial data (Latitude/Longitude) not found in the dataset.")""")
    
    nb.cells.extend([md_cell, code_cell])
    
    # Write notebook
    with open(NOTEBOOK_PATH, 'w') as f:
        nbf.write(nb, f)
    print("Notebook updated.")
else:
    print("Notebook already has the map section.")
