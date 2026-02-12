import json
import os

def fix_notebook_02():
    nb_path = '02_factor_analysis.ipynb'
    if not os.path.exists(nb_path):
        print(f"{nb_path} not found.")
        return

    with open(nb_path, 'r') as f:
        nb = json.load(f)

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = cell['source']
            new_source = []
            skip_next = False
            for i, line in enumerate(source):
                if skip_next:
                    skip_next = False
                    continue
                
                # Fix the specific messed up lines in 02
                if "plt.title('Factor Loadings: Which variables belong to which factor?')" in line and "plt.savefig" in line:
                     # It might be one line or split weirdly in the list
                     pass # Handle below
                
                # Clean up the specific cell with factor loadings
                if "sns.heatmap" in line:
                    new_source.append(line)
                    # Check if next lines are the messed up ones
                    # We will just reconstruct the end of this cell
                    # But we need to be careful not to duplicate if it's already correct
                    continue
                
                # Detect the messed up block
                if "plt.title('Factor Loadings: Which variables belong to which factor?')" in line:
                     # Skip this and the savefig line if they look wrong
                     continue
                if "plt.savefig('figures/factor_loadings.png'" in line:
                     continue
                if "plt.title('Factor Loadings (The \"Themes\")')" in line:
                     continue
                
                new_source.append(line)
            
            # If this was the heatmap cell, append the correct lines at the end (before plt.show)
            # This is a bit risky if I don't identify the cell precisely.
            # Let's try a string replacement approach on the whole source list content
            
            full_source = "".join(source)
            if "sns.heatmap" in full_source and "factor_loadings.png" in full_source:
                # Reconstruct this specific cell's source
                new_cell_source = []
                for line in source:
                    if "sns.heatmap" in line:
                        new_cell_source.append(line)
                        new_cell_source.append("plt.title('Factor Loadings: Which variables belong to which factor?')\n")
                        new_cell_source.append("plt.savefig('figures/factor_loadings.png', dpi=300, bbox_inches='tight')\n")
                    elif "plt.title" in line or "plt.savefig" in line:
                        continue # Skip existing title/save lines to avoid dupes
                    else:
                        new_cell_source.append(line)
                cell['source'] = new_cell_source
            
            # Also fix scree plot if needed
            if "plt.title('Scree Plot')" in full_source and "scree_plot.png" in full_source:
                 # Ensure savefig is correctly placed
                 pass

    with open(nb_path, 'w') as f:
        json.dump(nb, f, indent=4)
    print(f"Fixed {nb_path}")

def fix_notebook_03():
    nb_path = '03_feature_importance.ipynb'
    if not os.path.exists(nb_path):
        print(f"{nb_path} not found.")
        return

    with open(nb_path, 'r') as f:
        nb = json.load(f)

    for cell in nb['cells']:
        if cell['cell_type'] == 'code':
            source = cell['source']
            full_source = "".join(source)
            
            # Fix Feature Importance Plot
            if "plt.bar" in full_source and "feature_importance.png" in full_source:
                new_source = []
                for line in source:
                    if "plt.tight_layout()" in line:
                        new_source.append(line)
                        # Add savefig with correct indentation (4 spaces based on previous view)
                        new_source.append("    plt.savefig('figures/feature_importance.png', dpi=300, bbox_inches='tight')\n")
                    elif "plt.savefig('figures/feature_importance.png'" in line:
                        continue # Skip the bad line
                    else:
                        new_source.append(line)
                cell['source'] = new_source
            
            # Add Model Comparison Plot save if missing
            if "Model Performance Comparison" in full_source and "plt.bar" not in full_source:
                 # This might be the wrong cell. The comparison plot might be in a different cell.
                 # Let's look for where 'comparison' dataframe is displayed or plotted.
                 # In the file view, cell 6 creates 'comparison' df and displays it.
                 # It doesn't seem to plot it?
                 # Wait, the user wanted 'model_comparison.png'.
                 # If there is no plot, I need to add code to plot it.
                 pass

    # We need to find the cell that displays the comparison and add plotting code
    for cell in nb['cells']:
        if cell['cell_type'] == 'code' and "display(comparison)" in "".join(cell['source']):
            # Add plotting code to this cell
            source = cell['source']
            # Check if plotting code already exists
            if "plt.figure" not in "".join(source):
                source.append("\n")
                source.append("# Visualize Model Comparison\n")
                source.append("plt.figure(figsize=(8, 5))\n")
                source.append("sns.barplot(x='Model', y='R2 Score', data=comparison, palette='viridis')\n")
                source.append("plt.title('Model Comparison: R2 Score')\n")
                source.append("plt.ylim(0, 1)\n")
                source.append("plt.savefig('figures/model_comparison.png', dpi=300, bbox_inches='tight')\n")
                source.append("plt.show()\n")
            cell['source'] = source

    with open(nb_path, 'w') as f:
        json.dump(nb, f, indent=4)
    print(f"Fixed {nb_path}")

if __name__ == "__main__":
    fix_notebook_02()
    fix_notebook_03()
