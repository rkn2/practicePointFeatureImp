import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
import os

# Set output directory
FIG_DIR = '../figures'
DATA_FILE = '../../extracted_cad_data.csv'

def run_case_study(grid_size=100.0, num_runs=25):
    if not os.path.exists(FIG_DIR):
        os.makedirs(FIG_DIR)
        
    print(f"--- Running Eastern State Case Study Analysis ---")
    
    # 1. Load Data
    df = pd.read_csv(DATA_FILE)
    df['layer'] = df['layer'].str.upper()
    df['grid_x'] = (df['x'] // grid_size).astype(int)
    df['grid_y'] = (df['y'] // grid_size).astype(int)
    df['cell_id'] = df['filename'] + "_" + df['grid_x'].astype(str) + "_" + df['grid_y'].astype(str)
    
    master_grid = df.groupby(['cell_id', 'layer']).size().unstack(fill_value=0)
    master_grid = (master_grid > 0).astype(int)
    
    # 2. Symmetric Heatmap
    print("Generating Symmetric Heatmap...")
    corr = master_grid.corr()
    fig_size = max(15, len(corr.columns) * 0.3)
    plt.figure(figsize=(fig_size, fig_size))
    sns.heatmap(corr, cmap='coolwarm', center=0, vmin=-1, vmax=1, square=True, 
                linewidths=0.5, linecolor='black', cbar_kws={'shrink': .8})
    plt.title(f"Symmetric Spatial Correlation Matrix (Grid={grid_size})", fontsize=20)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, 'case_study_correlation.png'), dpi=300)
    plt.close()

    # 3. Model Prep
    targets = ['W-CRCK', 'C-CRCK']
    all_layers = master_grid.columns.tolist()
    technical_layers = ['DEFPOINTS', '0', 'A-ANNO-COLCTR', 'A-ANNO-COLNO', 'A-ANNO-CUTLINE', 'BOUNDBOX_C', 'BOUNDBOX_I', 'BOUNDBOX_O']
    features = [l for l in all_layers if l not in targets and l not in technical_layers]
    X = master_grid[features]
    
    # 4. Stability Analysis & Confusion Matrix
    for target in [t for t in targets if t in all_layers]:
        print(f"Analyzing {target}...")
        y = master_grid[target]
        
        # Stability Run
        all_importances = []
        for i in range(num_runs):
            clf = RandomForestClassifier(n_estimators=100, random_state=i, class_weight='balanced')
            clf.fit(X, y)
            all_importances.append(clf.feature_importances_)
            
        imp_df = pd.DataFrame(all_importances, columns=features)
        summary = pd.DataFrame({'feature': features, 'mean': imp_df.mean(), 'std': imp_df.std()})
        summary = summary.sort_values('mean', ascending=False).head(10)
        
        plt.figure(figsize=(10, 6))
        plt.barh(summary['feature'], summary['mean'], xerr=summary['std'], color='teal', capsize=5)
        plt.gca().invert_yaxis()
        plt.title(f"Feature Importance Stability: {target} (N={num_runs})")
        plt.xlabel("Mean Importance (Standard Deviation bars)")
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, f'stability_{target}.png'))
        plt.close()
        
        # Confusion Matrix (Single Stratified Split)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
        clf = RandomForestClassifier(n_estimators=100, random_state=42, class_weight='balanced')
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        
        plt.figure(figsize=(6, 5))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                    xticklabels=['No Crack', 'Crack'], yticklabels=['No Crack', 'Crack'])
        plt.title(f"Confusion Matrix: {target}")
        plt.tight_layout()
        plt.savefig(os.path.join(FIG_DIR, f'confusion_{target}.png'))
        plt.close()

    print("Analysis complete. Figures saved to revision/figures/")

if __name__ == "__main__":
    run_case_study()
