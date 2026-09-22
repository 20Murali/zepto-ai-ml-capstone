# Zepto Data & AI Platform

## Overview

This project is a complete AI/ML platform with three connected modules:

1. **Data Pipeline** — Scrapes and stores book data.
2. **Analytics Pipeline** — Analyzes the Titanic dataset and builds ML models.
3. **Support Assistant** — Uses Zepto policy documents to answer questions with RAG.

All three modules are inside one GitHub repository.

```text
project/
│
├── data_pipeline/
├── analytics/
├── support_assistant/
└── README.md
```

---

# Module 1 — Data Pipeline

## Description

This module scrapes book data from `books.toscrape.com`, cleans the data, converts GBP prices to INR, and stores the data in a SQLite database.

### Main Steps

```text
Scrape → Clean → Convert → Store → Query
```

### Data Collected

* Book title
* Price
* Rating
* Availability
* Category

The final dataset contains at least **60 books from at least 3 categories**.

### Data Cleaning

* GBP price is converted to `float`.
* Star ratings are converted to numbers from 1–5.
* Availability is converted to a boolean.
* Invalid values are handled according to the project requirements.

### Currency Conversion

The required fixed conversion rate is:

```text
1 GBP = 105.50 INR
```

```text
price_inr = price_gbp × 105.50
```

### Database

SQLite is used with two related tables:

```text
categories
    ↓
books
```

The tables use a primary key and foreign key relationship.

### SQL

The module includes at least 5 SQL queries covering:

* SELECT / WHERE
* ORDER BY
* LIMIT
* DISTINCT
* IN or BETWEEN
* JOIN

Some query results are also loaded into pandas using `pd.read_sql()` and reproduced using `pd.merge()`.

### Run

```bash
cd data_pipeline
pip install -r requirements.txt
python <pipeline_file>.py
```

---

# Module 2 — Analytics Pipeline

## Description

This module uses the Titanic dataset to perform data analysis, visualization, classification, and regression.

The dataset is loaded once and then used throughout the pipeline.

### Main Steps

```text
Load Data → Clean → EDA → Visualization → Modeling → Evaluation
```

### Data Analysis

The module includes:

* Dataset information
* Summary statistics
* Missing-value analysis
* Missing-value handling
* Age and fare analysis
* Outlier detection
* Survival-rate analysis
* Correlation analysis
* Data visualization

At least 4 charts are created with written interpretations.

### Machine Learning

Three classification models are trained:

* Logistic Regression
* Decision Tree
* Random Forest

The models are evaluated using:

* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix
* ROC Curve
* AUC

The Decision Tree is also visualized.

### Imbalance Handling

The module compares:

```text
Baseline
Class Weight = Balanced
SMOTE
```

SMOTE is applied only to the training data.

### Hyperparameter Tuning

`GridSearchCV` is used to tune the Random Forest.

The best parameters and OOB score are reported.

### Regression

A Linear Regression model is also used to predict `fare`.

The following metrics are reported:

* MAE
* RMSE
* R²
* Adjusted R²

A residual plot is also included.

### Model Pipeline

The preprocessing and final model are saved together using `joblib`.

This allows the saved pipeline to accept raw input and make predictions.

### Run

```bash
cd analytics
pip install -r requirements.txt
```

Run the notebooks or scripts used for the analysis and modeling.

---

# Module 3 — Support Assistant

## Description

This module creates a small Zepto support assistant using RAG (Retrieval-Augmented Generation).

The assistant uses Zepto policy documents as its knowledge base.

### Main Steps

```text
Documents → Embeddings → ChromaDB → Retrieval → Answer
```

### Documents

The project contains 8 policy documents covering:

* Delivery
* Returns and refunds
* Membership
* Order tracking
* Cancellation
* Damaged or missing items
* Gift cards
* Customer support

### Embeddings

The documents are embedded using:

```text
all-MiniLM-L6-v2
```

The embeddings are stored in ChromaDB.

### LangGraph

The assistant uses three main nodes:

```text
classify_intent
      ↓
 ┌────┴────┐
 ↓         ↓
policy    general
 ↓         ↓
retrieve  direct
and       answer
answer
```

Policy questions retrieve relevant information from ChromaDB.

General questions receive a fixed response in mock mode.

### Mock LLM

The required mode is:

```text
MOCK_LLM=1
```

or leaving `MOCK_LLM` unset.

This mode does not require an API key or external LLM service.

### API

The assistant is available through FastAPI:

```text
POST /ask
```

Example:

```json
{
  "query": "How long does delivery take?"
}
```

The response contains:

```json
{
  "answer": "...",
  "sources": ["..."],
  "confidence": 1.0
}
```

### Run

```bash
cd support_assistant
pip install -r requirements.txt
uvicorn main:app --reload
```

### Docker

Build:

```bash
docker build -t zepto
```
