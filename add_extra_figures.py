import json, os

# Helper to append a code cell to a notebook

def append_code_cell(nb_path, source_lines):
    with open(nb_path, 'r') as f:
        nb = json.load(f)
    # Create cell structure
    cell = {
        "cell_type": "code",
        "metadata": {},
        "source": source_lines,
        "outputs": [],
        "execution_count": None
    }
    nb['cells'].append(cell)
    with open(nb_path, 'w') as f:
        json.dump(nb, f, indent=4)
    print(f"Appended cell to {nb_path}")

# 1. 01_simple_statistics.ipynb – pairplot and simple regression
pairplot_src = [
    "import seaborn as sns, matplotlib.pyplot as plt\n",
    "# Pairplot of key continuous variables\n",
    "sns.pairplot(df[['Avg_Temp_C','Temp_Range_C','Annual_Rainfall_mm','Humidity_Percent','Soil_Moisture_Index','Crack_Width_mm','Condition_Rating']])\n",
    "plt.savefig('figures/pairplot.png', dpi=300, bbox_inches='tight')\n",
    "plt.close()\n"
]
append_code_cell('01_simple_statistics.ipynb', pairplot_src)

simple_reg_src = [
    "import matplotlib.pyplot as plt\n",
    "# Simple regression: Condition vs Crack Width\n",
    "plt.scatter(df['Crack_Width_mm'], df['Condition_Rating'], alpha=0.6)\n",
    "plt.xlabel('Crack Width (mm)')\n",
    "plt.ylabel('Condition Rating')\n",
    "plt.title('Condition vs Crack Width (simple regression)')\n",
    "plt.savefig('figures/simple_regression.png', dpi=300, bbox_inches='tight')\n",
    "plt.close()\n"
]
append_code_cell('01_simple_statistics.ipynb', simple_reg_src)

# 2. 02_factor_analysis.ipynb – factor scores scatter
factor_scatter_src = [
    "import matplotlib.pyplot as plt\n",
    "# Factor scores scatter (first two factors)\n",
    "scores = fa.transform(df[fa_vars])  # assuming fa and fa_vars defined earlier\n",
    "plt.scatter(scores[:,0], scores[:,1], c=df['District_ID'].astype('category').cat.codes, cmap='viridis', alpha=0.7)\n",
    "plt.xlabel('Factor 1')\n",
    "plt.ylabel('Factor 2')\n",
    "plt.title('Factor Scores by District')\n",
    "plt.colorbar(label='District')\n",
    "plt.savefig('figures/factor_scores_scatter.png', dpi=300, bbox_inches='tight')\n",
    "plt.close()\n"
]
append_code_cell('02_factor_analysis.ipynb', factor_scatter_src)

# 3. 03_feature_importance.ipynb – permutation importance plot
perm_imp_src = [
    "import matplotlib.pyplot as plt, seaborn as sns\n",
    "# Permutation importance (requires trained model 'model')\n",
    "from sklearn.inspection import permutation_importance\n",
    "result = permutation_importance(model, X_test, y_test, n_repeats=10, random_state=42)\n",
    "importances = result.importances_mean\n",
    "indices = np.argsort(importances)[::-1]\n",
    "plt.figure(figsize=(8,5))\n",
    "sns.barplot(x=importances[indices], y=[X_test.columns[i] for i in indices], palette='viridis')\n",
    "plt.title('Permutation Importance')\n",
    "plt.xlabel('Mean Decrease in Score')\n",
    "plt.tight_layout()\n",
    "plt.savefig('figures/permutation_importance.png', dpi=300, bbox_inches='tight')\n",
    "plt.close()\n"
]
append_code_cell('03_feature_importance.ipynb', perm_imp_src)

# 4. 04_visualization.ipynb – boxplot by material and spatial map
boxplot_src = [
    "import seaborn as sns, matplotlib.pyplot as plt\n",
    "# Boxplot of Condition Rating by Material Type\n",
    "sns.boxplot(x='Material_Type', y='Condition_Rating', data=df, palette='viridis')\n",
    "plt.title('Condition Rating by Material Type')\n",
    "plt.savefig('figures/boxplot_condition_by_material.png', dpi=300, bbox_inches='tight')\n",
    "plt.close()\n"
]
append_code_cell('04_visualization.ipynb', boxplot_src)

spatial_map_src = [
    "import matplotlib.pyplot as plt\n",
    "# Simple spatial map (using dummy X/Y coordinates)\n",
    "df['x'] = np.random.rand(len(df))*100\n",
    "df['y'] = np.random.rand(len(df))*100\n",
    "plt.scatter(df['x'], df['y'], c=df['Condition_Rating'], cmap='viridis', s=40)\n",
    "plt.colorbar(label='Condition Rating')\n",
    "plt.title('Spatial Distribution of Condition Rating')\n",
    "plt.xlabel('X coordinate')\n",
    "plt.ylabel('Y coordinate')\n",
    "plt.savefig('figures/spatial_map.png', dpi=300, bbox_inches='tight')\n",
    "plt.close()\n"
]
append_code_cell('04_visualization.ipynb', spatial_map_src)

print('All cells appended')
