import json

notebooks = ["01_simple_statistics.ipynb", "02_factor_analysis.ipynb", "03_feature_importance.ipynb"]

for nb_file in notebooks:
    with open(nb_file, "r") as f:
        data = json.load(f)
    
    for cell in data["cells"]:
        if cell["cell_type"] == "code":
            source = "".join(cell["source"])
            if "# Drop spatial coordinates for analysis" in source:
                # Fix the awful unindented mess by simply using regex or replacing exact bad lines
                bad_snippet = """    df = pd.read_csv('processed_data.csv')

# Drop spatial coordinates for analysis
if 'Latitude' in df.columns:
    df = df.drop(columns=['Latitude', 'Longitude'])"""
                
                good_snippet = """    df = pd.read_csv('processed_data.csv')
    
    # Drop spatial coordinates for analysis
    if 'Latitude' in df.columns:
        df = df.drop(columns=['Latitude', 'Longitude'])"""
                
                source = source.replace(bad_snippet, good_snippet)
                cell["source"] = [line + "\n" for line in source.split("\n")]
                cell["source"][-1] = cell["source"][-1].rstrip("\n")
                
    with open(nb_file, "w") as f:
        json.dump(data, f, indent=1)

print("Notebook indentation fixed.")
