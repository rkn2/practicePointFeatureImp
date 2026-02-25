#!/usr/bin/env python
# coding: utf-8

# # Data Preparation for Heritage Analysis
# 
# ## Introduction
# Welcome to the first step of your data-driven preservation journey! 
# 
# Before we can use advanced algorithms to find patterns or predict deterioration, we must first "clean" and prepare our data. Think of this like preparing a historic surface before applying a conservation treatment: if you don't remove the dirt and loose material first, the treatment won't work.
# 
# In this notebook, we will cover three essential steps:
# 1. **Handling Missing Values**: What do we do when our records are incomplete? (Imputation)
# 2. **Encoding Categories**: How do we translate words like "Brick" or "Stone" into numbers the computer understands? (One-Hot Encoding)
# 3. **Standardization**: How do we compare variables with different units, like temperature (degrees) and crack width (millimeters)? (Scaling)
# 
# ---

# ## Step 0: Upload Your Data (Google Colab Users)
# 
# If you're running this in **Google Colab**, you need to upload the `heritage_data.csv` file first.
# 
# **Option 1: Manual Upload**
# 1. Click the folder icon 📁 on the left sidebar
# 2. Click the upload button and select `heritage_data.csv`
# 
# **Option 2: Use the code below** (Uncomment and run if needed)

# ### Real-World Example: Why Data Preparation Matters
# 
# #### The Scenario
# 
# Imagine you have data on 200 historic buildings:
# - **Building A**: Year built = 1850, Material = "Brick", Condition = 3.5
# - **Building B**: Year built = 1920, Material = "Stone", Condition = ??? (missing!)
# - **Building C**: Year built = 1875, Material = "brick" (lowercase!), Condition = 4.2
# 
# #### Problems You'll Encounter
# 
# **1. Missing Data**
# - Building B has no condition rating
# - **Solution**: Fill with average, or remove that row
# 
# **2. Inconsistent Formatting**
# - "Brick" vs. "brick" — computer sees these as different!
# - **Solution**: Standardize to lowercase
# 
# **3. Different Scales**
# - Year built: 1800-2000 (range = 200)
# - Condition: 1-5 (range = 4)
# - **Problem**: Models think "year" is 50x more important just because numbers are bigger!
# - **Solution**: Standardize (make all variables comparable)
# 
# **4. Categorical Variables**
# - Material = "Brick", "Stone", "Wood"
# - **Problem**: Models need numbers, not words
# - **Solution**: One-hot encoding (create dummy variables)
# 
# #### What This Notebook Does
# 
# We'll walk through each problem with **concrete examples** and **ready-to-use code**:
# 
# | Step | What It Fixes | Example |
# |------|---------------|----------|
# | **1. Load Data** | Get your spreadsheet into Python | CSV → DataFrame |
# | **2. Check Missing** | Find gaps in your data | "15 buildings missing moisture data" |
# | **3. Handle Missing** | Fill or remove gaps | Fill with average moisture |
# | **4. Encode Categories** | Convert text to numbers | "Brick" → Material_Brick=1 |
# | **5. Standardize** | Make scales comparable | Year 1850 → -1.2, Year 2000 → +1.8 |
# | **6. Save Clean Data** | Export for next steps | processed_data.csv |
# 
# #### Before vs. After
# 
# **Before (raw data)**:
# ```
# Building_ID | Year | Material | Moisture | Condition
# 001         | 1850 | Brick    | 45.2     | 3.5
# 002         | 1920 | Stone    | ???      | 4.1
# 003         | 1875 | brick    | 67.8     | 2.9
# ```
# 
# **After (clean data)**:
# ```
# Building_ID | Year_Std | Material_Brick | Material_Stone | Moisture_Std | Condition
# 001         | -1.2     | 1              | 0              | -0.5         | 3.5
# 002         | 0.3      | 0              | 1              | 0.0 (filled) | 4.1
# 003         | -0.8     | 1              | 0              | 1.2          | 2.9
# ```
# 
# Now the data is ready for analysis!
# 
# Let's get started:

# In[1]:


# Uncomment the lines below if you want to upload via code
# from google.colab import files
# uploaded = files.upload()
# print("File uploaded successfully!")


# In[2]:


import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the dataset with error handling
try:
    df = pd.read_csv('heritage_data.csv')
    print(f"✅ Dataset loaded successfully!")
    print(f"Dataset shape: {df.shape} (Rows, Columns)")
except FileNotFoundError:
    print("❌ ERROR: 'heritage_data.csv' not found.")
    print("Please upload the file using the instructions above.")
    raise


# ## Exploring the Data
# 
# Before we clean anything, let's understand what we have.

# In[3]:


# Show the first few rows
print("First 5 rows of the dataset:")
display(df.head())


# ### Data Dictionary
# 
# Here's what each column means:
# 
# | Column Name | Description | Units/Type |
# |------------|-------------|------------|
# | `Building_ID` | Unique identifier for each building | Text (e.g., B001) |
# | `District_ID` | Geographic district | Category (North, South, East, West, Central) |
# | `Construction_Year` | Year the building was constructed | Year |
# | `Material_Type` | Primary construction material | Category (Brick, Stone, Concrete, Wood) |
# | `Foundation_Type` | Type of foundation | Category (Shallow, Deep, Pile) |
# | `Avg_Temp_C` | Average annual temperature | Degrees Celsius |
# | `Temp_Range_C` | Seasonal temperature variation | Degrees Celsius |
# | `Annual_Rainfall_mm` | Total annual rainfall | Millimeters |
# | `Humidity_Percent` | Average relative humidity | Percentage (0-100) |
# | `Freeze_Thaw_Cycles` | Number of freeze-thaw events per year | Count |
# | `Soil_Moisture_Index` | Composite measure of ground moisture | Index (0-20) |
# | `Crack_Width_mm` | Maximum observed crack width | Millimeters |
# | `Salt_Deposition_g_m2` | Salt accumulation on surfaces | Grams per square meter |
# | `Condition_Rating` | Overall condition assessment | Scale 1-5 (1=Good, 5=Poor) |
# | `Intervention_Urgency` | Priority score for intervention | Scale 0-100 |

# In[4]:


# Summary statistics for numerical columns
print("Summary Statistics:")
display(df.describe())

# Data types and non-null counts
print("\nData Types and Missing Values:")
print(df.info())


# ## 1. Handling Missing Values
# 
# ### The Problem
# Real-world heritage data is rarely perfect. You might have missing sensor readings due to a power outage, or a condition survey where some fields were left blank. Machine learning algorithms generally cannot handle blank spaces—they need a number for every input.
# 
# ### The Solution: Imputation
# Instead of throwing away valuable data just because one number is missing, we can make an educated guess to fill in the gap. This is called **imputation**.
# - For **numerical** data (like temperature), we often fill gaps with the **average (mean)** of that column.
# - For **categorical** data (like material type), we often fill gaps with the **most frequent** value (the mode).
# 
# Think of this like retouching a small loss in a painting: you use the surrounding colors to infer what should be there, rather than leaving a white hole.

# In[5]:


# Check for missing values
print("Missing values per column:")
missing_counts = df.isnull().sum()
print(missing_counts[missing_counts > 0])

if missing_counts.sum() == 0:
    print("\n✅ No missing values found!")
else:
    print(f"\n⚠️ Total missing values: {missing_counts.sum()}")


# ## 2. Encoding Categories
# 
# ### The Problem
# Computers are excellent at math, but they don't understand words. If we feed the word "Brick" into a mathematical equation, it will fail. We need to convert these text labels into numbers.
# 
# ### The Solution: One-Hot Encoding
# We could just assign numbers (Brick=1, Stone=2, Wood=3), but that implies an order (is Wood "greater" than Brick?). Instead, we use **One-Hot Encoding**.
# 
# This creates a new column for each category. 
# - Is_Brick: 1 if yes, 0 if no
# - Is_Stone: 1 if yes, 0 if no
# 
# It's like a switchboard where only the relevant light is turned on.

# ## 3. Standardization (Scaling)
# 
# ### The Problem
# Imagine comparing "Annual Rainfall" (e.g., 800 mm) with "Crack Width" (e.g., 0.5 mm). The rainfall number is huge compared to the crack width! If we don't fix this, the algorithm might think rainfall is 1600 times more important just because the number is bigger.
# 
# ### The Solution: Scaling
# We **standardize** the data so that every variable is on the same playing field. We adjust the values so that the average is 0 and the spread (standard deviation) is 1. 
# - A value of +1 means "somewhat higher than average".
# - A value of -2 means "much lower than average".
# 
# This ensures that a 10% change in humidity is treated with the same importance as a 10% change in crack width.

# In[6]:


# Let's see how this works manually on one column first
example_col = df['Avg_Temp_C'].head()
print("Original Values:")
print(example_col)

# Manual Calculation: (Value - Mean) / Standard Deviation
scaled_col = (example_col - example_col.mean()) / example_col.std()
print("\nScaled Values (Manual):")
print(scaled_col)

print("\n💡 Notice: The values are now small numbers centered around 0.")


# ## Putting it all together: The Pipeline
# 
# Doing that math manually for every column is tedious. In Python, we use a **Pipeline** to automate it. This ensures that every piece of data goes through the exact same cleaning process.

# In[7]:


# Define which columns are which
numeric_features = ['Construction_Year', 'Avg_Temp_C', 'Temp_Range_C', 
                    'Annual_Rainfall_mm', 'Humidity_Percent', 'Freeze_Thaw_Cycles', 
                    'Soil_Moisture_Index', 'Crack_Width_mm', 'Salt_Deposition_g_m2']

categorical_features = ['District_ID', 'Material_Type', 'Foundation_Type']

# Create transformers (the "workers" that will process the data)

# For numbers: Fill missing with Mean -> Scale to standard range
numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
])

# For categories: Fill missing with Most Frequent -> Convert to One-Hot numbers
categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('encoder', OneHotEncoder(handle_unknown='ignore', sparse_output=False))
])

# Combine them into one master processor
preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

# Apply the transformation
print("Processing data...")
X_processed = preprocessor.fit_transform(df)

# Get the new column names (especially for the one-hot encoded categories)
ohe = preprocessor.named_transformers_['cat']['encoder']
cat_feature_names = ohe.get_feature_names_out(categorical_features)
feature_names = numeric_features + list(cat_feature_names)

# Create a nice clean DataFrame with the results
df_processed = pd.DataFrame(X_processed, columns=feature_names)

# Add back the ID and Outcome variables (we don't scale outcomes usually)
df_processed['Building_ID'] = df['Building_ID'].values
df_processed['Condition_Rating'] = df['Condition_Rating'].values
df_processed['Intervention_Urgency'] = df['Intervention_Urgency'].values

print("✅ Done! Processed Data Shape:", df_processed.shape)
display(df_processed.head())


# ## Saving the Result
# Now that our data is clean, filled, and scaled, we save it to a new file. We will use this `processed_data.csv` for all our analysis in the next notebooks.

# In[8]:


df_processed.to_csv('processed_data.csv', index=False)
print("✅ Saved processed_data.csv")
print(f"   - Original columns: {len(df.columns)}")
print(f"   - Processed columns: {len(df_processed.columns)}")
print(f"   - Rows: {len(df_processed)}")


# ## Optional: Check for Multicollinearity (VIF)
# 
# Before moving to analysis, it's good practice to check if your variables are highly correlated with each other. This is called **multicollinearity**.
# 
# ### Why Check Now?
# 
# - **Early warning**: Identify potential issues before analysis
# - **Data quality**: Part of understanding your dataset
# - **Plan ahead**: Know if you'll need to handle correlated variables
# 
# ### What is VIF?
# 
# **Variance Inflation Factor (VIF)** measures how much each variable correlates with others:
# - **VIF < 5**: Low correlation (good!)
# - **VIF 5-10**: Moderate correlation (watch out)
# - **VIF > 10**: High correlation (problematic for regression)
# 
# **Common in heritage data**: Environmental variables often correlate (rainfall ↔ humidity ↔ soil moisture)
# 
# Let's check:

# In[9]:


# OPTIONAL: Check for multicollinearity using VIF
# Uncomment to run

# from statsmodels.stats.outliers_influence import variance_inflation_factor
# 
# # Select only numerical columns (VIF only works on numbers)
# numerical_cols = df.select_dtypes(include=[np.number]).columns.tolist()
# 
# # Remove ID columns and target variable if present
# numerical_cols = [col for col in numerical_cols if 'ID' not in col.upper() 
#                   and col not in ['Condition_Rating', 'Intervention_Urgency']]
# 
# if len(numerical_cols) > 1:
#     print("="*70)
#     print("MULTICOLLINEARITY CHECK (VIF)")
#     print("="*70)
#     print(f"\nChecking {len(numerical_cols)} numerical variables\n")
#     
#     # Prepare data (remove any missing values)
#     X_vif = df[numerical_cols].dropna()
#     
#     # Calculate VIF
#     vif_data = pd.DataFrame()
#     vif_data["Variable"] = numerical_cols
#     vif_data["VIF"] = [variance_inflation_factor(X_vif.values, i) 
#                        for i in range(len(numerical_cols))]
#     
#     # Sort by VIF
#     vif_data = vif_data.sort_values('VIF', ascending=False)
#     
#     # Add interpretation
#     def interpret_vif(vif):
#         if vif < 5:
#             return "✓ Low"
#         elif vif < 10:
#             return "⚠ Moderate"
#         else:
#             return "✗ High"
#     
#     vif_data["Status"] = vif_data["VIF"].apply(interpret_vif)
#     
#     print(vif_data.to_string(index=False))
#     
#     # Summary
#     high_vif = vif_data[vif_data["VIF"] > 10]
#     if len(high_vif) > 0:
#         print(f"\n⚠ WARNING: {len(high_vif)} variable(s) with VIF > 10 (high multicollinearity)")
#         print("   → These variables are highly correlated with others")
#         print("   → May cause issues in regression analysis (Notebook 01)")
#         print("   → Consider: Factor Analysis (Notebook 02) or Tree models (Notebook 03)")
#     else:
#         print("\n✓ No severe multicollinearity detected (all VIF < 10)")
#     
#     # Save for reference
#     vif_data.to_csv('vif_check.csv', index=False)
#     print("\n✓ VIF results saved to 'vif_check.csv'")
# else:
#     print("Not enough numerical variables for VIF check.")


# ## Real-World Challenge: Imbalanced Data
# 
# ### The Scenario
# Our synthetic dataset is "perfectly balanced" (roughly equal numbers of buildings in each condition). In the real world, heritage data is often **imbalanced**:
# - **95%** of your buildings might be in "Good" condition.
# - Only **5%** might be in "Poor" condition.
# 
# ### The Problem
# If you train a model on this, it gets lazy! It learns to just guess "Good" for every single building.
# - **Result**: It achieves **95% accuracy** (wow!).
# - **Reality**: It misses **100% of the problems** (useless!).
# 
# ### What To Do (If You Have This Problem)
# 
# We won't cover the code here to keep things simple, but here are the keywords to search for when you encounter this:
# 
# 1. **Resampling**: Changing your dataset to be more balanced.
#    - **Oversampling**: Duplicating the rare examples (or creating synthetic ones using a tool called **SMOTE**).
#    - **Undersampling**: Using fewer of the abundant examples.
# 
# 2. **Better Metrics**: Never trust "Accuracy" alone for imbalanced data.
#    - Use **Precision** and **Recall** (we'll discuss these in Notebook 3).
#    - A model with 80% accuracy that finds half the defects is better than a 95% accurate model that finds none!
# 
# **Key Takeaway**: If your data is highly imbalanced, don't just run the standard analysis. Look up "handling imbalanced data with SMOTE".

# ## Troubleshooting
# 
# **Common Issues:**
# 
# 1. **FileNotFoundError**: Make sure `heritage_data.csv` is uploaded to your workspace.
# 2. **KeyError (column not found)**: Check that your CSV has the expected column names.
# 3. **Memory Error**: If your dataset is very large (>10,000 rows), you may need more RAM. Try using a smaller sample.
# 
# **Need Help?** Check that:
# - Your CSV file is properly formatted
# - Column names match exactly (case-sensitive)
# - There are no special characters in the data

# ## Next Steps
# 
# Now that your data is prepared, you can proceed to:
# 
# 1. **Notebook 2: Factor Analysis** - Identify hidden patterns and group related variables
# 2. **Notebook 3: Feature Importance** - Determine which variables drive deterioration
# 3. **Notebook 4: Visualization** - Create publication-ready charts
# 
# Remember to use the `processed_data.csv` file you just created!
