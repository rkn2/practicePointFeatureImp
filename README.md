# Interactive Tutorials: Machine Learning for Heritage Preservation

Welcome! This repository contains a series of interactive tutorials designed to help heritage professionals use machine learning techniques—specifically Factor Analysis and Feature Importance—to prioritize preservation decisions.

**Introductory Technical Barrier.** These tutorials are designed as a guided experience. While you don't need to be fluent in Python, a willingness to engage with script-based analysis, execute code cells, and follow built-in troubleshooting guides is necessary. These tutorials run in your web browser using Google Colab.

## 🚀 Getting Started

To use these tutorials, you need:
1.  A Google account (to run Google Colab).
2.  The sample dataset (`heritage_data.csv`).

### Step 1: Get the Data
First, you need to download the sample dataset to your computer.

1.  **[Click here to view heritage_data.csv on GitHub](https://github.com/rkn2/practicePointFeatureImp/blob/main/heritage_data.csv)**
2.  Click the **Download raw file** button (the icon that looks like a tray with a downward arrow) on the right side of the screen.
3.  Save the file to a known location on your computer (e.g., your Downloads folder or Desktop).

> **Note:** You will need to upload this file to Google Colab each time you start a new notebook.

---

## 📚 The Tutorials

Click the links below to open each tutorial directly in Google Colab. We recommend going through them in order.

### 1. Data Preparation
**[Open in Google Colab](https://colab.research.google.com/github/rkn2/practicePointFeatureImp/blob/main/00_data_preparation.ipynb)**
*   **What it does:** Teaches you how to "clean" your data so computers can understand it.
*   **Key skills:** Handling missing values, converting text categories (like "Brick" or "Stone") into numbers, and standardizing different units.
*   **Output:** A clean dataset ready for analysis.

### 2. Simple Statistical Methods
**[Open in Google Colab](https://colab.research.google.com/github/rkn2/practicePointFeatureImp/blob/main/01_simple_statistics.ipynb)**
*   **What it does:** Introduces basic statistical tools to explore your data before using complex models.
*   **Key skills:** Correlation analysis (seeing which variables move together) and simple regression.
*   **When to use:** When you have a small dataset (fewer than 50 buildings) or just a few variables.

### 3. Factor Analysis
**[Open in Google Colab](https://colab.research.google.com/github/rkn2/practicePointFeatureImp/blob/main/02_factor_analysis.ipynb)**
*   **What it does:** Finds hidden patterns in your data by grouping related variables.
*   **Key skills:** Identifying underlying drivers of deterioration (e.g., "Moisture Stress" vs. "Thermal Stress").
*   **Goal:** Simplify complex data into meaningful themes.

### 4. Feature Importance
**[Open in Google Colab](https://colab.research.google.com/github/rkn2/practicePointFeatureImp/blob/main/03_feature_importance.ipynb)**
*   **What it does:** Ranks your variables to see which ones best predict a specific outcome (like Condition Rating).
*   **Key skills:** Using machine learning models (Random Forest) to answer "Which factor matters most?"
*   **Goal:** Prioritize what to monitor or fix first.

### 5. Visualization
**[Open in Google Colab](https://colab.research.google.com/github/rkn2/practicePointFeatureImp/blob/main/04_visualization.ipynb)**
*   **What it does:** Generates publication-quality charts and graphs.
*   **Key skills:** Creating correlation heatmaps, boxplots, and scatter plots to communicate your findings.

---

## 🛠️ How to Use Google Colab

When you open a notebook link, follow these steps:

1.  **Connect**: Click the "Connect" button in the top right corner to start the server.
2.  **Upload Data**:
    *   Click the **Folder icon** 📁 on the left sidebar.
    *   Click the **Upload icon** (a paper with an up arrow) at the top of the sidebar.
    *   Select the `heritage_data.csv` file you downloaded in Step 1.
3.  **Run Code**:
    *   You can run each "cell" of code by clicking the **Play button** ▶️ next to it.
    *   Or, go to the top menu and select **Runtime > Run all** to run the entire analysis at once.

**Tip:** If you get an error saying `FileNotFoundError: [Errno 2] No such file or directory: 'heritage_data.csv'`, it means you haven't uploaded the data file yet! Just follow the "Upload Data" steps above and try again.
