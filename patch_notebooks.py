import json

notebooks = ["01_simple_statistics.ipynb", "02_factor_analysis.ipynb", "03_feature_importance.ipynb"]

for nb_file in notebooks:
    with open(nb_file, "r") as f:
        data = json.load(f)
    
    for cell in data["cells"]:
        if cell["cell_type"] == "code":
            source = "".join(cell["source"])
            if "df = pd.read_csv('processed_data.csv')" in source:
                # Add a line to drop coordinates
                replacement = "df = pd.read_csv('processed_data.csv')\n\n# Drop spatial coordinates for analysis\nif 'Latitude' in df.columns:\n    df = df.drop(columns=['Latitude', 'Longitude'])"
                source = source.replace("df = pd.read_csv('processed_data.csv')", replacement)
                cell["source"] = [line + "\n" for line in source.split("\n")]
                cell["source"][-1] = cell["source"][-1].rstrip("\n")
                
    with open(nb_file, "w") as f:
        json.dump(data, f, indent=1)

print("Notebooks patched to ignore Latitude and Longitude.")
