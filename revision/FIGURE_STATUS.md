# Figure Status Report

## ✅ Required Figures (Referenced in revision.tex)

| Figure | Status | Location | Script |
|--------|--------|----------|--------|
| condition_distribution.png | ✅ Present | revision/figures/ | generate_condition_distribution.py |
| correlation_heatmap.png | ✅ Present | revision/figures/ | generate_correlation_heatmap.py |
| pairplot.png | ✅ Present | revision/figures/ | generate_pairplot.py |
| workflow.jpg | ✅ Present | revision/figures/ | (static file) |
| factor_loadings.png | ✅ Present | revision/figures/ | generate_factor_loadings.py |
| factor_scores_risk.png | ✅ Present | revision/figures/ | generate_factor_scores_risk.py |
| multiple_regression.png | ✅ Present | revision/figures/ | generate_multiple_regression.py |
| simple_regression.png | ✅ Present | revision/figures/ | generate_simple_regression.py |
| feature_importance.png | ✅ Present | revision/figures/ | generate_feature_importance.py |
| permutation_importance.png | ✅ Present | revision/figures/ | generate_permutation_importance.py |
| boxplot_condition_by_material.png | ✅ Present | revision/figures/ | generate_boxplot_condition_by_material.py |
| groundwater_risk_map.png | ✅ Present | revision/figures/ | generate_groundwater_risk_map.py |
| **bldgs_condition.jpg** | ⚠️ **MISSING** | - | **(external photo - needs to be added)** |

## 📋 Extra Figures (Not referenced in paper)

These are in `revision/figures/` but not used in the current version of the paper:

- factor_plot_options.png
- flowchart.png
- model_comparison.png
- prioritization_map_real.png

**Action**: These can be moved to `_trash/` or kept for future use.

## 🔴 Missing Figure

**bldgs_condition.jpg** is referenced in revision.tex (line 155) but not found anywhere.

This appears to be a photo showing:
> "Visual representation of the five-level building condition rating scale"

**You need to**:
1. Locate or create this image
2. Add it to `revision/figures/bldgs_condition.jpg`

## ✅ All Generation Scripts Ready

All 11 required figures can be regenerated using:
```bash
cd revision/figures/scripts_final
python generate_all_figures.py
```

Individual scripts:
- generate_condition_distribution.py
- generate_correlation_heatmap.py
- generate_pairplot.py
- generate_factor_loadings.py
- generate_factor_scores_risk.py
- generate_multiple_regression.py
- generate_simple_regression.py
- generate_feature_importance.py
- generate_permutation_importance.py
- generate_boxplot_condition_by_material.py
- generate_groundwater_risk_map.py

## 📊 Summary

- **Required figures**: 13 total
- **Present**: 12 ✅
- **Missing**: 1 ⚠️ (bldgs_condition.jpg)
- **Extra figures**: 4 (can be removed or kept)
- **Generation scripts**: 11 (all working)
