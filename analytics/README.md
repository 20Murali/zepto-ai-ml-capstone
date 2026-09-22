# Titanic Survival Prediction — Module 2

## Project Overview

This module performs exploratory data analysis (EDA), data cleaning, visualization, preprocessing, classification, model evaluation, and inference using the Titanic dataset.

The project uses three classification models:

* Logistic Regression
* Decision Tree
* Random Forest

The final saved model is a complete preprocessing and Random Forest pipeline stored as `best_model.joblib`.

---

## Project Structure

```text
analytics/
├── 01_eda.ipynb
├── titanic.csv
├── best_model.joblib
└── README.md
```

### Files

**`01_eda.ipynb`**

Contains the complete analysis, including:

* Dataset profiling
* Missing-value analysis and cleaning
* Outlier analysis
* Univariate analysis
* Bivariate analysis
* Correlation analysis
* Multivariate visualizations
* Standardization sanity check
* Train/test split
* ML preprocessing
* Model training
* Model evaluation
* ROC comparison
* Feature importance
* Model saving
* Inference testing

**`titanic.csv`**

Offline copy of the raw Titanic dataset used by the notebook.

**`best_model.joblib`**

Saved machine-learning pipeline containing the preprocessing steps and Random Forest classifier.

---

## Requirements

Install the required Python packages:

```bash
pip install pandas numpy seaborn matplotlib scikit-learn joblib jupyter
```

---

## Running the Notebook

From the project directory, start Jupyter:

```bash
jupyter notebook
```

Then open:

```text
analytics/01_eda.ipynb
```

Run the notebook cells from top to bottom.

The notebook first loads the Titanic dataset and saves an offline copy as:

```text
titanic.csv
```

The remaining analysis and modeling steps use the prepared dataset.

---

## Data Cleaning

Missing values were analyzed before cleaning.

The original missing percentages were:

| Column        | Missing Percentage |
| ------------- | -----------------: |
| `age`         |           19.8653% |
| `embarked`    |            0.2245% |
| `deck`        |           77.2166% |
| `embark_town` |            0.2245% |

The cleaning strategy was:

* `age`: median imputation
* `embarked`: remove rows with missing values
* `embark_town`: remove rows with missing values
* `deck`: drop the column because of very high missingness

After cleaning, the dataset contained **889 rows and 14 columns**.

IQR outliers were identified for `age` and `fare` but were not removed.

---

## Exploratory Data Analysis

The analysis includes:

* Age distribution histogram
* Age box plot
* Fare distribution histogram
* Fare box plot
* Survival rate by sex
* Survival rate by passenger class
* Survival rate by sex and passenger class
* Correlation heatmap
* Multivariate charts
* Age and fare standardization

The two strongest correlations by absolute correlation magnitude were:

| Feature Pair        | Correlation |
| ------------------- | ----------: |
| `pclass` and `fare` |   -0.548193 |
| `sibsp` and `parch` |    0.414542 |

---

## Machine Learning Approach

The target variable is:

```text
survived
```

The data was split using an 80/20 stratified train/test split.

The resulting datasets were:

```text
Training: 711 rows
Testing: 178 rows
```

Stratification preserved the target-class proportions across the training and testing sets.

### Numerical Features

```text
age
sibsp
parch
fare
```

Numerical preprocessing:

1. Median imputation
2. StandardScaler

### Categorical Features

```text
sex
embarked
```

Categorical preprocessing:

1. Most-frequent imputation
2. One-hot encoding

The preprocessing was placed inside a scikit-learn `Pipeline` and `ColumnTransformer` so that preprocessing parameters were learned from the training data only.

---

## Models

Three classifiers were evaluated:

1. Logistic Regression
2. Decision Tree
3. Random Forest

The models were evaluated on the same held-out test set.

### Model Results

| Model               | Accuracy | Precision |   Recall |       F1 |      AUC |
| ------------------- | -------: | --------: | -------: | -------: | -------: |
| Logistic Regression | 0.780899 |  0.754386 | 0.632353 | 0.688000 | 0.826471 |
| Decision Tree       | 0.814607 |  0.786885 | 0.705882 | 0.744186 | 0.820655 |
| Random Forest       | 0.820225 |  0.810345 | 0.691176 | 0.746032 | 0.825535 |

The models were compared using accuracy, precision, recall, F1 score, and ROC-AUC.

---

## Model Evaluation

Evaluation includes:

* Accuracy
* Precision
* Recall
* F1 score
* ROC-AUC
* Confusion matrices
* Classification reports
* ROC curve comparison
* Random Forest feature importance

The ROC plot compares all three classifiers on the same test set.

---

## Saved Model

The final model pipeline is saved as:

```text
best_model.joblib
```

The saved artifact contains both:

* preprocessing
* Random Forest classifier

This allows raw input data to be passed directly to the saved pipeline without manually performing encoding or scaling.

---

## Running Inference

The saved model can be loaded using Joblib:

```python
import joblib

model = joblib.load("best_model.joblib")
```

Create a raw passenger record:

```python
import pandas as pd

sample_passenger = pd.DataFrame({
    "pclass": [1],
    "sex": ["female"],
    "age": [30],
    "sibsp": [0],
    "parch": [0],
    "fare": [80],
    "embarked": ["C"]
})
```

Generate a prediction:

```python
prediction = model.predict(sample_passenger)
probability = model.predict_proba(sample_passenger)

print("Prediction:", prediction[0])
print("Probability:", probability[0])
```

The tested sample produced:

```text
Prediction: 1
Probability: [0.03483235 0.96516765]
```

where:

```text
0 = Did not survive
1 = Survived
```

The saved pipeline therefore predicted `Survived` for this sample.

---

## Reproducibility

The modeling workflow uses fixed random seeds where applicable, including:

```text
random_state=42
```

The same train/test split and preprocessing workflow are used for model comparison.

---

## Conclusion

This module demonstrates an end-to-end Titanic classification workflow, beginning with exploratory data analysis and cleaning and continuing through leakage-safe preprocessing, classification, model evaluation, model persistence, and raw-input inference.
