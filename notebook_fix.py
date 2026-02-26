import json

notebooks = ["01_simple_statistics.ipynb", "02_factor_analysis.ipynb", "03_feature_importance.ipynb", "04_visualization.ipynb"]

for nb_file in notebooks:
    with open(nb_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 1. Add os.makedirs at the top
    has_makedirs = False
    for cell in data['cells']:
        if cell['cell_type'] == 'code' and "os.makedirs('figures', exist_ok=True)" in "".join(cell['source']):
            has_makedirs = True
            break
            
    if not has_makedirs:
        setup_cell = {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "import os\n",
                "# Create a directory to save figures if it doesn't exist\n",
                "os.makedirs('figures', exist_ok=True)\n",
                "print(\"Directory 'figures/' is ready.\")"
            ]
        }
        # Find first code cell to insert after, or just after the first markdown cell
        insert_idx = 0
        for i, cell in enumerate(data['cells']):
            if cell['cell_type'] == 'code':
                insert_idx = i
                break
        
        # Insert before the first code cell
        data['cells'].insert(insert_idx, setup_cell)

    # 2. Make sure Latitude/Longitude are explicitly dropped in the numerical columns extraction in 01_simple_statistics
    if "01_simple" in nb_file:
        for cell in data['cells']:
            if cell['cell_type'] == 'code':
                source = "".join(cell['source'])
                if "numerical_cols = [col for col in numerical_cols if 'ID' not in col.upper()]" in source:
                    if "Latitude" not in source:
                        new_source = source.replace(
                            "numerical_cols = [col for col in numerical_cols if 'ID' not in col.upper()]",
                            "numerical_cols = [col for col in numerical_cols if 'ID' not in col.upper() and col not in ['Latitude', 'Longitude']]"
                        )
                        cell['source'] = [line + '\n' for line in new_source.split('\n')]
                        cell['source'][-1] = cell['source'][-1].rstrip('\n')

    with open(nb_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=1)

print("done")
