#!/usr/bin/env python3
"""
Quick reference: Which script generates which figure?
Run this to see the mapping.
"""

figures = {
    "condition_distribution.png": "generate_condition_distribution.py",
    "pairplot.png": "generate_pairplot.py",
    "correlation_heatmap.png": "generate_correlation_heatmap.py",
    "simple_regression.png": "generate_simple_regression.py",
    "multiple_regression.png": "generate_multiple_regression.py",
    "factor_loadings.png": "generate_factor_loadings.py",
    "factor_scores_risk.png": "generate_factor_scores_risk.py",
    "feature_importance.png": "generate_feature_importance.py",
    "permutation_importance.png": "generate_permutation_importance.py",
    "boxplot_condition_by_material.png": "generate_boxplot_condition_by_material.py",
    "groundwater_risk_map.png": "generate_groundwater_risk_map.py",
}

static_files = {
    "bldgs_condition.jpg": "Manual/external file (photos)",
    "workflow.jpg": "Manual/external file (diagram)",
}

print("=" * 70)
print("FIGURE GENERATION REFERENCE")
print("=" * 70)

print("\n📊 GENERATED FIGURES (11 total)")
print("-" * 70)
for i, (fig, script) in enumerate(figures.items(), 1):
    print(f"{i:2d}. {fig:40s} → {script}")

print("\n📷 STATIC FILES (2 total)")
print("-" * 70)
for fig, source in static_files.items():
    print(f"    {fig:40s} → {source}")

print("\n" + "=" * 70)
print("To generate all figures: python generate_all_figures.py")
print("To generate one figure:  python generate_<name>.py")
print("=" * 70)
