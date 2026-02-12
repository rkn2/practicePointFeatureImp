#!/usr/bin/env python
# coding: utf-8

# # Results Visualization
# 
# ## Introduction
# You have cleaned the data, found the factors, and identified the important features. But if you can't show your results to a stakeholder (like a site manager or funding agency), the analysis is useless.
# 
# **Visualization** is the bridge between complex math and human understanding. 
# 
# In this notebook, we will create three types of plots that are essential for preservation reports:
# 1. **Correlation Heatmap**: A color-coded grid to spot relationships instantly.
# 2. **Boxplots**: To compare groups (e.g., "Is the crack width worse in buildings with poor ratings?").
# 3. **Pairplots**: To see everything at once.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Load processed data
df = pd.read_csv('processed_data.csv')

# Set plot style to make it look professional
sns.set(style="whitegrid")
print("Data loaded and plotting style set.")


# ## 1. Correlation Heatmap
# 
# This is one of the most popular charts in data science. It shows the correlation (relationship) between every pair of variables.
# 
# **How to read it:**
# - **Red (Positive correlation)**: As one goes up, the other goes up. (e.g., Rainfall and Soil Moisture).
# - **Blue (Negative correlation)**: As one goes up, the other goes down.
# - **White/Light (Zero correlation)**: No relationship.
# 
# Look for the dark squares!

# In[2]:


plt.figure(figsize=(12, 10))
# Select numerical columns for correlation
corr_cols = ['Avg_Temp_C', 'Temp_Range_C', 'Annual_Rainfall_mm', 
             'Humidity_Percent', 'Soil_Moisture_Index', 'Crack_Width_mm', 
             'Salt_Deposition_g_m2', 'Condition_Rating']

corr = df[corr_cols].corr()

# Create the heatmap
sns.heatmap(corr, annot=True, cmap='coolwarm', fmt=".2f", linewidths=.5)
plt.title('Correlation Matrix: What is related to what?')
plt.show()


# ## 2. Distribution of Condition Ratings
# 
# Before we dive deeper, let's just see: How many buildings are in good condition vs. bad condition?
# This is a simple **Count Plot**.

# In[3]:


plt.figure(figsize=(8, 5))
sns.countplot(x='Condition_Rating', data=df, palette='viridis')
plt.title('How many buildings are in each condition category?')
plt.xlabel('Condition Rating (1=Good, 5=Poor)')
plt.ylabel('Number of Buildings')
plt.show()


# ## 3. Boxplots: Comparing Groups
# 
# Boxplots are fantastic for answering questions like: **"Do buildings in worse condition have wider cracks?"**
# 
# **How to read a Boxplot:**
# - The **Box** holds the middle 50% of the data.
# - The **Line** in the middle is the Median (the typical value).
# - The **Whiskers** (lines sticking out) show the range of normal data.
# - The **Dots** are Outliers (unusual cases).
# 
# If the boxes move up as you go from Rating 1 to 5, it means there is a clear trend.

# In[4]:


fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Crack Width vs Condition
sns.boxplot(x='Condition_Rating', y='Crack_Width_mm', data=df, ax=axes[0], palette='Reds')
axes[0].set_title('Trend: Crack Width vs. Condition')

# Plot 2: Salt Deposition vs Condition
sns.boxplot(x='Condition_Rating', y='Salt_Deposition_g_m2', data=df, ax=axes[1], palette='Blues')
axes[1].set_title('Trend: Salt Deposition vs. Condition')

plt.tight_layout()
plt.show()


# ## 4. Pairplot
# 
# Finally, let's look at multiple variables at once. A **Pairplot** creates a grid of scatterplots.
# 
# We color the dots by `Condition_Rating`. 
# - If you see distinct clusters of colors, it means those variables are good at separating good buildings from bad ones.
# - If the colors are all mixed up, it means the relationship is messy.

# In[5]:


sns.pairplot(df[['Crack_Width_mm', 'Soil_Moisture_Index', 'Condition_Rating']], 
             hue='Condition_Rating', palette='viridis')
plt.show()


# ## Conclusion
# 
# Congratulations! You have completed the entire workflow:
# 1. **Prepared Data**: Cleaned and scaled.
# 2. **Factor Analysis**: Found the hidden themes.
# 3. **Feature Importance**: Found the drivers of damage.
# 4. **Visualization**: Communicated the results.
# 
# You are now ready to apply these techniques to your own heritage datasets!
