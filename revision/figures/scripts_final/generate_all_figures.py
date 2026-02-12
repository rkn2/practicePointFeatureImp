"""
Master script to generate all figures for the paper.
Run this to regenerate all figures at once.
"""
import os
import sys

# Add the scripts directory to path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)

# Import all generation functions
from generate_condition_distribution import generate_condition_distribution
from generate_pairplot import generate_pairplot
from generate_correlation_heatmap import generate_correlation_heatmap
from generate_simple_regression import generate_simple_regression
from generate_multiple_regression import generate_multiple_regression
from generate_factor_loadings import generate_factor_loadings
from generate_factor_scores_risk import generate_factor_scores_risk
from generate_feature_importance import generate_feature_importance
from generate_permutation_importance import generate_permutation_importance
from generate_boxplot_condition_by_material import generate_boxplot_condition_by_material
from generate_groundwater_risk_map import generate_groundwater_risk_map

def generate_all_figures():
    """Generate all figures for the paper."""
    print("=" * 70)
    print("GENERATING ALL FIGURES FOR PAPER")
    print("=" * 70)
    
    figures = [
        ("Condition Distribution", generate_condition_distribution),
        ("Pairplot", generate_pairplot),
        ("Correlation Heatmap", generate_correlation_heatmap),
        ("Simple Regression", generate_simple_regression),
        ("Multiple Regression", generate_multiple_regression),
        ("Factor Loadings", generate_factor_loadings),
        ("Factor Scores Risk", generate_factor_scores_risk),
        ("Feature Importance", generate_feature_importance),
        ("Permutation Importance", generate_permutation_importance),
        ("Boxplot by Material", generate_boxplot_condition_by_material),
        ("Groundwater Risk Map", generate_groundwater_risk_map),
    ]
    
    for i, (name, func) in enumerate(figures, 1):
        print(f"\n[{i}/{len(figures)}] Generating {name}...")
        print("-" * 70)
        try:
            func()
            print(f"✓ {name} completed successfully")
        except Exception as e:
            print(f"✗ Error generating {name}: {str(e)}")
    
    print("\n" + "=" * 70)
    print("FIGURE GENERATION COMPLETE")
    print("=" * 70)
    print(f"All figures saved to: {os.path.abspath('../')}")

if __name__ == "__main__":
    generate_all_figures()
