import json

with open("00_data_preparation.ipynb", "r") as f:
    data = json.load(f)

for cell in data["cells"]:
    if cell["cell_type"] == "code":
        source = "".join(cell["source"])
        if "df_processed['Building_ID'] = df['Building_ID'].values" in source:
            source = source.replace(
                "df_processed['Intervention_Urgency'] = df['Intervention_Urgency'].values",
                "df_processed['Intervention_Urgency'] = df['Intervention_Urgency'].values\n\n# Also pass through coordinates if present\nif 'Latitude' in df.columns:\n    df_processed['Latitude'] = df['Latitude'].values\nif 'Longitude' in df.columns:\n    df_processed['Longitude'] = df['Longitude'].values"
            )
            # update cell
            cell["source"] = [line + "\n" for line in source.split("\n")]
            # remove last spurious newline
            cell["source"][-1] = cell["source"][-1].rstrip("\n")

with open("00_data_preparation.ipynb", "w") as f:
    json.dump(data, f, indent=1)

