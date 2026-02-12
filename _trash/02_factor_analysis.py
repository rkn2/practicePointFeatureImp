#!/usr/bin/env python
# coding: utf-8

# # Factor Analysis for Heritage Preservation
# 
# ## Introduction
# Imagine you walk into a historic library and see thousands of books scattered on the floor. To organize them, you wouldn't pick them up one by one and memorize every title. Instead, you would look for **themes**: "These are all history books," "These are all science books."
# 
# **Factor Analysis** does exactly this for your data. 
# 
# If you have 20 different variables (Temperature, Humidity, Rainfall, Soil Moisture, etc.), Factor Analysis looks for the hidden "themes" or **Factors** that connect them. It might tell you:
# > "Hey, Rainfall, Humidity, and Soil Moisture all tend to go up and down together. Let's just call this group **'Moisture Stress'**."
# 
# This simplifies your life. Instead of tracking 20 variables, you only need to track 3 or 4 main factors.
# 
# In this notebook, we will:
# 1. **Check Suitability**: Is our data actually related enough to find patterns? (Bartlett & KMO Tests)
# 2. **Determine Number of Factors**: How many "themes" are there? (Scree Plot)
# 3. **Extract Factors**: Run the math to group the variables.
# 4. **Interpret Results**: Give names to our new factors.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_bartlett_sphericity
from factor_analyzer.factor_analyzer import calculate_kmo

# Load the processed data from the previous step
df = pd.read_csv('processed_data.csv')

# We only use the numerical environmental/structural variables for this analysis
# We exclude IDs (because they are just labels) and Outcomes (because we want to understand the *causes*)
fa_cols = ['Construction_Year', 'Avg_Temp_C', 'Temp_Range_C', 
           'Annual_Rainfall_mm', 'Humidity_Percent', 'Freeze_Thaw_Cycles', 
           'Soil_Moisture_Index', 'Crack_Width_mm', 'Salt_Deposition_g_m2']

X = df[fa_cols]
print("Data loaded for Factor Analysis.")
X.head()


# ## 1. Suitability Tests
# 
# Before we start, we need to ask: "Are there actually any patterns here?"
# 
# If every variable is completely random and unrelated to the others, Factor Analysis won't work. We use two tests to check this:
# 
# 1. **Bartlett's Test**: Checks if variables are correlated. We want the p-value to be **less than 0.05** (statistically significant).
# 2. **KMO Test (Kaiser-Meyer-Olkin)**: Measures how much overlap there is between variables. We want a score **above 0.6**.

# In[2]:


# Bartlett's Test
chi_square_value, p_value = calculate_bartlett_sphericity(X)
print(f"Bartlett's Test p-value: {p_value}")

if p_value < 0.05:
    print("✅ GOOD: The variables are related. We can proceed.")
else:
    print("❌ WARNING: The variables might not be related enough.")

# KMO Test
kmo_all, kmo_model = calculate_kmo(X)
print(f"KMO Score: {kmo_model:.2f}")

if kmo_model > 0.6:
    print("✅ GOOD: Data adequacy is sufficient.")
else:
    print("⚠️ CAUTION: KMO score is low, results might be less reliable.")


# ## 2. Determining the Number of Factors (The Scree Plot)
# 
# How many factors should we look for? 2? 5? 10?
# 
# We use a **Scree Plot** to decide. 
# - The Y-axis (Eigenvalue) represents how much information a factor captures.
# - We look for the "elbow" of the curve—the point where the line flattens out.
# - **Rule of Thumb**: Any factor with an Eigenvalue > 1 is usually worth keeping.

# In[3]:


fa = FactorAnalyzer(rotation=None)
fa.fit(X)
ev, v = fa.get_eigenvalues()

plt.figure(figsize=(8, 5))
plt.scatter(range(1, X.shape[1]+1), ev)
plt.plot(range(1, X.shape[1]+1), ev)
plt.title('Scree Plot')
plt.xlabel('Factor Number')
plt.ylabel('Eigenvalue (Information Captured)')
plt.grid()
# Draw a red line at 1.0
plt.axhline(y=1, color='r', linestyle='--', label='Cutoff (1.0)')
plt.legend()
plt.show()


# ## 3. Running Factor Analysis
# 
# Based on the plot above, let's say we see 3 factors above the red line. We will now tell the computer: "Group these variables into 3 main themes."
# 
# We use a technique called **Varimax Rotation**. Imagine rotating a map so that North is up—it makes it easier to read. Varimax rotates the mathematical factors so they are easier to interpret.
# 
# **Note on Rotation**: We use `varimax` which assumes the factors are independent (orthogonal). If you suspect your factors are strongly related (e.g. moisture and temperature often go together), you might try `rotation='promax'` (oblique rotation) in advanced analyses.

# In[4]:


n_factors = 3
fa = FactorAnalyzer(n_factors=n_factors, rotation='varimax')
fa.fit(X)

# Get Factor Loadings
# Loadings show the correlation between the variable and the factor.
# High number (positive or negative) = Strong relationship.
# Near zero = No relationship.
loadings = pd.DataFrame(fa.loadings_, index=X.columns, columns=[f'Factor_{i+1}' for i in range(n_factors)])

plt.figure(figsize=(10, 8))
sns.heatmap(loadings, annot=True, cmap='coolwarm', center=0, vmin=-1, vmax=1)
plt.title('Factor Loadings (The "Themes")')
plt.show()


# ## 4. Interpretation: Naming the Factors
# 
# This is where your expertise comes in! Look at the heatmap above.
# 
# **How to read it:**
# Look at each column (Factor). Which variables have high numbers (dark red or dark blue)?
# 
# **Example Interpretation:**
# - **Factor 1**: If it has high numbers for `Rainfall`, `Humidity`, and `Soil_Moisture`, we might name it **"Moisture Exposure"**.
# - **Factor 2**: If it has high numbers for `Temp_Range` and `Freeze_Thaw`, we might name it **"Thermal Stress"**.
# - **Factor 3**: If it has high numbers for `Crack_Width` and `Age`, we might name it **"Structural Aging"**.
# 
# Once you name them, you can use these 3 factors instead of the original 9 variables for reporting!

# In[5]:


# We can calculate the score for each building on these new factors
factor_scores = pd.DataFrame(fa.transform(X), columns=[f'Factor_{i+1}' for i in range(n_factors)])

# Combine with Building ID to see which buildings have high stress
df_factors = pd.concat([df[['Building_ID']], factor_scores], axis=1)
print("Factor Scores for the first 5 buildings:")
df_factors.head()

