import json

# Fix 00_data_preparation.ipynb
with open("00_data_preparation.ipynb", "r") as f:
    data = json.load(f)

# The VIF section is a markdown cell about VIF and a commented out code cell.
# We will identify them and remove them.
new_cells = []
skip = False
for cell in data["cells"]:
    source_text = "".join(cell.get("source", []))
    if cell["cell_type"] == "markdown" and "Check for Multicollinearity (VIF)" in source_text:
        skip = True
        continue
    if skip and cell["cell_type"] == "code" and "MULTICOLLINEARITY CHECK (VIF)" in source_text:
        skip = False # Found the code cell, skip it and stop skipping
        continue
    
    if not skip:
        new_cells.append(cell)

data["cells"] = new_cells
with open("00_data_preparation.ipynb", "w") as f:
    json.dump(data, f, indent=1)

# Fix 01_simple_statistics.ipynb
with open("01_simple_statistics.ipynb", "r") as f:
    data2 = json.load(f)

new_cells2 = []
for cell in data2["cells"]:
    source_text = "".join(cell.get("source", []))
    if cell["cell_type"] == "code" and ("sns.pairplot" in source_text or "simple regression: Condition vs Crack Width" in source_text.lower() or "Condition vs Crack Width (simple regression)" in source_text):
        if "plt.savefig('figures/pairplot.png" in source_text or "plt.savefig('figures/simple_regression.png" in source_text:
            continue # skip these cells
    new_cells2.append(cell)

data2["cells"] = new_cells2
with open("01_simple_statistics.ipynb", "w") as f:
    json.dump(data2, f, indent=1)

print("Tasks done.")
