# Figure Generation Scripts

This directory contains standalone Python scripts to generate all figures used in the paper `revision.tex`.

## Overview

Each script is self-contained and generates a single figure. All scripts:
- Load data from `processed_data.csv` (or `heritage_data.csv` as fallback)
- Use consistent styling (viridis color palette, white background, no grid)
- Save figures to the parent directory (`../`) at 300 DPI
- Can be run independently or all at once

## Quick Start

### Generate All Figures
```bash
cd revision/figures/scripts_final
python generate_all_figures.py
```

### Generate Individual Figures
```bash
python generate_condition_distribution.py
python generate_pairplot.py
# ... etc
```

## Figure Scripts

| Script | Output Figure | Description |
|--------|---------------|-------------|
| `generate_condition_distribution.py` | `condition_distribution.png` | Bar chart showing distribution of building condition ratings |
| `generate_pairplot.py` | `pairplot.png` | Pairwise scatter plots of key continuous variables |
| `generate_correlation_heatmap.py` | `correlation_heatmap.png` | Correlation matrix heatmap of all variables |
| `generate_simple_regression.py` | `simple_regression.png` | Simple linear regression: Crack Width → Condition Rating |
| `generate_multiple_regression.py` | `multiple_regression.png` | Multivariate regression: Actual vs Predicted values |
| `generate_factor_loadings.py` | `factor_loadings.png` | Factor analysis loadings heatmap |
| `generate_factor_scores_risk.py` | `factor_scores_risk.png` | Factor scores scatter: Environment vs Damage |
| `generate_feature_importance.py` | `feature_importance.png` | Random Forest feature importance ranking |
| `generate_permutation_importance.py` | `permutation_importance.png` | Permutation importance validation |
| `generate_boxplot_condition_by_material.py` | `boxplot_condition_by_material.png` | Boxplot of condition by material type |
| `generate_groundwater_risk_map.py` | `groundwater_risk_map.png` | Spatial map of building conditions |

## Requirements

All scripts require:
- pandas
- numpy
- matplotlib
- seaborn
- scikit-learn
- scipy

Install with:
```bash
pip install pandas numpy matplotlib seaborn scikit-learn scipy
```

## Data Requirements

Scripts expect to find `processed_data.csv` in one of these locations:
- `../../processed_data.csv` (two levels up from scripts_final)
- `../processed_data.csv` (one level up from scripts_final)

The data should contain columns like:
- `Condition_Rating`
- `Crack_Width_mm`
- `Soil_Moisture_Index`
- `Avg_Temp_C`
- `Annual_Rainfall_mm`
- etc.

## Customization

Each script is designed to be easily tweaked:
- **Colors**: Change `palette='viridis'` to other seaborn palettes
- **Figure size**: Modify `figsize=(width, height)` parameters
- **DPI**: Change `dpi=300` in `savefig()` calls
- **Variables**: Update feature lists in factor analysis and regression scripts

## Notes

- **Groundwater Risk Map**: Currently uses dummy coordinates. Replace with actual spatial data if available.
- **Factor Analysis**: Uses 3 components with Varimax rotation. Adjust `n_components` as needed.
- **Random Forest**: Uses 100 estimators. Increase for more stable results (slower).

## Troubleshooting

**"processed_data.csv not found"**
- Ensure the data file exists in the project root
- Check the relative path from scripts_final directory

**"Column not found" errors**
- Verify your data has the expected column names
- Update column names in the script to match your data

**Import errors**
- Install missing packages: `pip install <package_name>`

## Author
Generated for the practice point paper on machine learning in heritage preservation.
