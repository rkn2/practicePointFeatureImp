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

# In[1]:


import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Load the dataset
# We use pandas, a powerful library for working with data tables (like Excel sheets)
df = pd.read_csv('heritage_data.csv')

# .head() shows us the first 5 rows so we can see what the data looks like
print(f"Dataset shape: {df.shape} (Rows, Columns)")
df.head()


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

# In[2]:


# Check for missing values
# This counts how many blank cells are in each column
print("Missing values per column:")
print(df.isnull().sum())


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

# In[3]:


# Let's see how this works manually on one column first
example_col = df['Avg_Temp_C'].head()
print("Original Values:")
print(example_col)

# Manual Calculation: (Value - Mean) / Standard Deviation
scaled_col = (example_col - example_col.mean()) / example_col.std()
print("\nScaled Values (Manual):")
print(scaled_col)

# You can see they are now small numbers centered around 0.


# ## Putting it all together: The Pipeline
# 
# Doing that math manually for every column is tedious. In Python, we use a **Pipeline** to automate it. This ensures that every piece of data goes through the exact same cleaning process.

# In[4]:


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
df_processed['Building_ID'] = df['Building_ID']
df_processed['Condition_Rating'] = df['Condition_Rating']
df_processed['Intervention_Urgency'] = df['Intervention_Urgency']

print("Done! Processed Data Shape:", df_processed.shape)
df_processed.head()


# ## Saving the Result
# Now that our data is clean, filled, and scaled, we save it to a new file. We will use this `processed_data.csv` for all our analysis in the next notebooks.

# In[5]:


df_processed.to_csv('processed_data.csv', index=False)
print("Saved processed_data.csv")

