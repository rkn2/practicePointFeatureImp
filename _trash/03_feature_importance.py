#!/usr/bin/env python
# coding: utf-8

# # Feature Importance Analysis
# 
# ## Introduction
# In the previous notebook, we found *groups* of variables (Factors). Now, we want to answer a more direct question: **"What is causing the damage?"**
# 
# If we have a building in poor condition, is it because of the rain? The age? The salt?
# 
# **Feature Importance** helps us rank these suspects. We use Machine Learning models to predict the condition of a building based on its data. Then, we ask the model: "Which variable helped you the most in making that prediction?"
# 
# We will use two powerful algorithms:
# 1. **Random Forest**: Imagine asking a committee of 100 experts for their opinion and taking the average. It's very stable and reliable.
# 2. **Gradient Boosting**: Imagine a student taking a test, then studying *only* the questions they got wrong, and taking it again. It learns from mistakes and can be very accurate.
# 
# In this notebook, we will:
# 1. **Split the Data**: Separate our data into "Study Material" (Train) and "Exam Questions" (Test).
# 2. **Train Models**: Teach the computer to predict building condition.
# 3. **Extract Importance**: Find out which variables matter most.

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error

# Load processed data
df = pd.read_csv('processed_data.csv')

# Define Target and Features
# Target (y): What we want to predict -> 'Condition_Rating'
# Features (X): The data we use to predict it -> Everything else (except IDs)
target = 'Condition_Rating'
drop_cols = ['Building_ID', 'Condition_Rating', 'Intervention_Urgency']

X = df.drop(columns=drop_cols)
y = df[target]

print("Features (X):", X.columns.tolist())
print("Target (y):", target)


# ## 1. Train-Test Split
# 
# If we teach the computer using *all* our data, it might just memorize the answers. This is called **overfitting**.
# 
# To test if it actually *learned* the patterns, we hide some data from it.
# - **Training Set (80%)**: The computer studies this data to learn the rules.
# - **Testing Set (20%)**: We use this to test the computer. It has never seen these buildings before.
# 
# It's exactly like a teacher holding back some questions from the textbook to use on the final exam.
# 
# > **Pro Tip on Data Leakage**: In this tutorial, we scaled our data *before* splitting it. In a strict professional environment, you should split the data first, then scale it. Why? Because calculating the average of the *whole* dataset gives the training set a tiny "peek" at the test set's data. For learning purposes here, pre-scaling is fine, but keep this in mind for production systems!

# In[2]:


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Total Buildings: {len(df)}")
print(f"Training with: {X_train.shape[0]} buildings")
print(f"Testing on: {X_test.shape[0]} buildings")


# ## 2. Random Forest Model
# 
# We create a **Random Forest Regressor**. 
# - `n_estimators=100`: We are creating a "forest" of 100 decision trees.
# - `random_state=42`: Ensures we get the same result every time we run this code.
# 
# After training (`.fit()`), we ask it to predict the condition of the test buildings (`.predict()`).
# 
# **Evaluating the Model**:
# - **R-squared ($R^2$)**: How well the model explains the variance (0 to 1). 1.0 is perfect.
# - **Mean Absolute Error (MAE)**: On average, how far off is our prediction? If MAE is 0.5, it means if the real rating is 3.0, our model might guess 2.5 or 3.5. Lower is better.

# In[3]:


rf = RandomForestRegressor(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

# Evaluate
y_pred_rf = rf.predict(X_test)
score_rf = r2_score(y_test, y_pred_rf)
mae_rf = mean_absolute_error(y_test, y_pred_rf)

print(f"Random Forest Accuracy (R2): {score_rf:.3f}")
print(f"Random Forest Error (MAE): {mae_rf:.3f} points")


# ## 3. Gradient Boosting Model
# 
# Now we try a different student: **Gradient Boosting**. It often performs better but can be more sensitive to noise.

# In[4]:


gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb.fit(X_train, y_train)

# Evaluate
y_pred_gb = gb.predict(X_test)
score_gb = r2_score(y_test, y_pred_gb)
mae_gb = mean_absolute_error(y_test, y_pred_gb)

print(f"Gradient Boosting Accuracy (R2): {score_gb:.3f}")
print(f"Gradient Boosting Error (MAE): {mae_gb:.3f} points")


# ## 4. Visualizing Feature Importance
# 
# This is the most important part! We ask the models: **"What was the most useful variable?"**
# 
# The bar chart below ranks the variables. 
# - **Tall bars**: These variables are the main drivers of deterioration.
# - **Short bars**: These variables don't matter much for this specific problem.
# 
# **Interpretation Tip**: If "Crack Width" is the top bar, it means existing damage is the best predictor of future rating (which makes sense!). If "Rainfall" is the top bar, it means the environment is the main driver.

# In[5]:


def plot_importance(model, feature_names, title):
    importances = model.feature_importances_
    # Sort the feature importance in descending order
    indices = np.argsort(importances)[::-1]
    
    plt.figure(figsize=(10, 6))
    plt.title(title)
    plt.bar(range(X.shape[1]), importances[indices], align="center", color='teal')
    plt.xticks(range(X.shape[1]), [feature_names[i] for i in indices], rotation=90)
    plt.ylabel("Importance Score (0-1)")
    plt.tight_layout()
    plt.show()

plot_importance(rf, X.columns, "Random Forest: What drives Condition Rating?")
plot_importance(gb, X.columns, "Gradient Boosting: What drives Condition Rating?")

