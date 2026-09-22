# Data Pipeline

## Overview

This module scrapes book data from Books to Scrape, cleans the collected data using Python and pandas, and stores the final dataset in a relational SQLite database.

The pipeline collects books from multiple categories and stores the cleaned data with prices in both GBP and INR.

## Technologies Used

* Python
* Requests
* BeautifulSoup
* pandas
* SQLite

## Data Collection

The scraper uses `requests` to download web pages and BeautifulSoup to parse the HTML.

The following fields are collected:

* `title`
* `price`
* `rating`
* `availability`
* `category`

Books are collected from multiple categories and their paginated pages.

## Data Cleaning

The raw scraped data is transformed into the following fields:

| Field       | Description                |
| ----------- | -------------------------- |
| `title`     | Book title                 |
| `price_gbp` | Numeric price in GBP       |
| `price_inr` | Price converted to INR     |
| `rating`    | Numeric rating from 1 to 5 |
| `in_stock`  | Boolean stock status       |
| `category`  | Book category              |

The GBP price is converted to INR using the required fixed conversion rate:

**1 GBP = 105.50 INR**

Invalid or non-numeric values are handled during the cleaning process.

## Database Design

The cleaned data is stored in SQLite using two related tables.

### `categories`

Stores unique book categories.

* `category_id` — Primary Key
* `category_name` — Unique category name

### `books`

Stores the book information.

* `book_id` — Primary Key
* `title`
* `price_gbp`
* `price_inr`
* `rating`
* `in_stock`
* `category_id` — Foreign Key referencing `categories.category_id`

The relationship is:

```text
categories
    |
    | 1-to-many
    |
books
```

Each book belongs to a category.

## SQL Queries

The module demonstrates the following SQL operations:

* `SELECT`
* `WHERE`
* `ORDER BY`
* `LIMIT`
* `DISTINCT`
* `BETWEEN`
* `JOIN`

The query module executes multiple queries, including:

1. Books costing more than £40.
2. The 10 most expensive books.
3. Distinct book ratings.
4. Books priced between £20 and £40.
5. Books joined with their category information.

## Pandas and SQL

The module uses `pd.read_sql()` to retrieve SQL query results into pandas DataFrames.

It also reproduces the SQL `JOIN` using `pd.merge()`.

The SQL JOIN and pandas merge results are compared after applying the same filtering, sorting, and row limit.

The comparison confirms that both approaches produce equivalent results.

## Running the Module

From the project root:

```bash
python data_pipeline/database.py
```

This builds the dataset and stores it in the SQLite database.

To run the SQL queries:

```bash
python data_pipeline/queries.py
```

The database file is stored as:

```text
data_pipeline/zepto_books.db
```
