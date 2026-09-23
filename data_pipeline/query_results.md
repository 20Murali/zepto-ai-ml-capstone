# SQL and Pandas Query Results

After loading the cleaned book data into the SQLite database, several SQL queries were executed to demonstrate filtering, sorting, limiting, distinct values, range-based filtering, and joining the normalized `books` and `categories` tables.

## 1. Books Above £40

**SQL query:**

```sql
SELECT title, price_gbp
FROM books
WHERE price_gbp > 40;
```

**Output:**

| Title                                                              | Price (GBP) |
| ------------------------------------------------------------------ | ----------: |
| It's Only the Himalayas                                            |       45.17 |
| Full Moon over Noah’s Ark: An Odyssey to Mount Ararat and Beyond   |       49.43 |
| See America: A Celebration of Our National Parks & Treasured Sites |       48.87 |
| A Summer In Europe                                                 |       44.34 |
| A Year in Provence (Provence #1)                                   |       56.88 |
| Sharp Objects                                                      |       47.82 |
| The Past Never Ends                                                |       56.50 |
| The Murder of Roger Ackroyd (Hercule Poirot #4)                    |       44.10 |
| The Last Mile (Amos Decker #2)                                     |       54.21 |
| A Time of Torment (Charlie Parker #14)                             |       48.35 |

The `WHERE` clause filters the database to books with a price greater than £40.

---

## 2. Top 10 Most Expensive Books

**SQL query:**

```sql
SELECT title, price_gbp
FROM books
ORDER BY price_gbp DESC
LIMIT 10;
```

**Output:**

| Rank | Title                                                            | Price (GBP) |
| ---: | ---------------------------------------------------------------- | ----------: |
|    1 | The Perfect Play (Play by Play #1)                               |       59.99 |
|    2 | Last One Home (New Beginnings #1)                                |       59.98 |
|    3 | Boar Island (Anna Pigeon #19)                                    |       59.48 |
|    4 | The Improbability of Love                                        |       59.45 |
|    5 | Listen to Me (Fusion #1)                                         |       58.99 |
|    6 | Candide                                                          |       58.63 |
|    7 | Miller's Valley                                                  |       58.54 |
|    8 | The Death of Humanity: and the Case for Life                     |       58.11 |
|    9 | The White Cat and the Monk: A Retelling of the Poem “Pangur Bán” |       58.08 |
|   10 | Digital Fortress                                                 |       58.00 |

This query uses `ORDER BY price_gbp DESC` to sort books from highest to lowest price and `LIMIT 10` to return only the ten most expensive books.

---

## 3. Distinct Ratings

**SQL query:**

```sql
SELECT DISTINCT rating
FROM books
ORDER BY rating;
```

**Output:**

| Rating |
| -----: |
|      1 |
|      2 |
|      3 |
|      4 |
|      5 |

The `DISTINCT` keyword removes duplicate values and returns the five unique rating levels present in the dataset.

---

## 4. Books Between £20 and £40

**SQL query:**

```sql
SELECT title, price_gbp
FROM books
WHERE price_gbp BETWEEN 20 AND 40
ORDER BY price_gbp;
```

**Output:**

| Title                                            | Price (GBP) |
| ------------------------------------------------ | ----------: |
| Run, Spot, Run: The Ethics of Keeping Pets       |       20.02 |
| Blood Defense (Samantha Brinkman #1)             |       20.30 |
| Keep Me Posted                                   |       20.46 |
| Love, Lies and Spies                             |       20.55 |
| Critique of Pure Reason                          |       20.75 |
| Between Shades of Gray                           |       20.79 |
| Delivering the Truth (Quaker Midwife Mystery #1) |       20.89 |
| Sit, Stay, Love                                  |       20.90 |
| Fruits Basket, Vol. 6 (Fruits Basket #6)         |       20.96 |
| Tuesday Nights in 1980                           |       21.04 |

The `BETWEEN` operator selects books whose `price_gbp` falls within the £20–£40 range. The results are ordered from the lowest to the highest price.

---

## 5. Top 10 Books With Categories

**SQL query:**

```sql
SELECT
    b.title,
    b.price_gbp,
    b.rating,
    c.category_name
FROM books AS b
JOIN categories AS c
    ON b.category_id = c.category_id
ORDER BY b.rating DESC
LIMIT 10;
```

**Output:**

| Title                                                                    | Price (GBP) | Rating | Category           |
| ------------------------------------------------------------------------ | ----------: | -----: | ------------------ |
| 1,000 Places to See Before You Die                                       |       26.08 |      5 | Travel             |
| A Time of Torment (Charlie Parker #14)                                   |       48.35 |      5 | Mystery            |
| What Happened on Beale Street (Secrets of the South Mysteries #2)        |       25.37 |      5 | Mystery            |
| The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1) |       52.30 |      5 | Mystery            |
| The Silkworm (Cormoran Strike #2)                                        |       23.05 |      5 | Mystery            |
| The Girl You Lost                                                        |       12.29 |      5 | Mystery            |
| A Flight of Arrows (The Pathfinders #2)                                  |       55.53 |      5 | Historical Fiction |
| Mrs. Houdini                                                             |       30.25 |      5 | Historical Fiction |
| The Passion of Dolssa                                                    |       28.32 |      5 | Historical Fiction |
| Voyager (Outlander #3)                                                   |       21.07 |      5 | Historical Fiction |

This query demonstrates the required SQL `JOIN`. The `books` table is joined with the `categories` table through the shared `category_id` foreign key.

---

# Pandas SQL Results

The SQL query results were also loaded into pandas DataFrames using `pd.read_sql()`.

## Books Above £40

```python
df_expensive = pd.read_sql(
    query_1,
    connection
)
```

**Result:**

| Title                                                              | Price (GBP) |
| ------------------------------------------------------------------ | ----------: |
| It's Only the Himalayas                                            |       45.17 |
| Full Moon over Noah’s Ark: An Odyssey to Mount Ararat and Beyond   |       49.43 |
| See America: A Celebration of Our National Parks & Treasured Sites |       48.87 |
| A Summer In Europe                                                 |       44.34 |
| A Year in Provence (Provence #1)                                   |       56.88 |
| Sharp Objects                                                      |       47.82 |
| The Past Never Ends                                                |       56.50 |
| The Murder of Roger Ackroyd (Hercule Poirot #4)                    |       44.10 |
| The Last Mile (Amos Decker #2)                                     |       54.21 |
| A Time of Torment (Charlie Parker #14)                             |       48.35 |

The pandas result matches the SQL query result for the books priced above £40.

---

# SQL JOIN Result in Pandas

The SQL JOIN was loaded into a pandas DataFrame using `pd.read_sql()`:

```python
df_join = pd.read_sql(
    query_2,
    connection
)
```

The resulting DataFrame contains **320 rows and 4 columns**:

```text
[320 rows x 4 columns]
```

The columns are:

* `title`
* `price_gbp`
* `rating`
* `category_name`

The first rows were:

| Title                                                                    | Price (GBP) | Rating | Category |
| ------------------------------------------------------------------------ | ----------: | -----: | -------- |
| 1,000 Places to See Before You Die                                       |       26.08 |      5 | Travel   |
| A Time of Torment (Charlie Parker #14)                                   |       48.35 |      5 | Mystery  |
| What Happened on Beale Street (Secrets of the South Mysteries #2)        |       25.37 |      5 | Mystery  |
| The Bachelor Girl's Guide to Murder (Herringford and Watts Mysteries #1) |       52.30 |      5 | Mystery  |
| The Silkworm (Cormoran Strike #2)                                        |       23.05 |      5 | Mystery  |

---

# Reproducing the SQL JOIN Using Pandas

The same relationship was reproduced using `pd.merge()` directly on the in-memory DataFrames:

```python
merged_df = pd.merge(
    books_df,
    categories_df,
    on="category_id",
    how="inner"
)
```

The resulting DataFrame was then reduced to the same four columns used by the SQL JOIN:

```python
merged_df[
    [
        "title",
        "price_gbp",
        "rating",
        "category_name"
    ]
].head(10)
```

The first ten rows of the pandas merge were:

| Title                                                               | Price (GBP) | Rating | Category |
| ------------------------------------------------------------------- | ----------: | -----: | -------- |
| It's Only the Himalayas                                             |       45.17 |      2 | Travel   |
| Full Moon over Noah’s Ark: An Odyssey to Mount Ararat and Beyond    |       49.43 |      4 | Travel   |
| See America: A Celebration of Our National Parks & Treasured Sites  |       48.87 |      3 | Travel   |
| Vagabonding: An Uncommon Guide to the Art of Long-Term World Travel |       36.94 |      2 | Travel   |
| Under the Tuscan Sun                                                |       37.33 |      3 | Travel   |
| A Summer In Europe                                                  |       44.34 |      2 | Travel   |
| The Great Railway Bazaar                                            |       30.54 |      1 | Travel   |
| A Year in Provence (Provence #1)                                    |       56.88 |      4 | Travel   |
| The Road to Little Dribbling: Adventures of an Uncommon Traveller   |       23.21 |      1 | Travel   |
| Neither Here nor There: Travels in Europe                           |       38.95 |      3 | Travel   |

---

# SQL JOIN vs Pandas Merge Validation

To verify that the SQL JOIN and pandas merge produce the same data, both results were selected using the same four columns, sorted by `title`, and their indexes were reset.

```python
sql_result = (
    df_join[
        [
            "title",
            "price_gbp",
            "rating",
            "category_name"
        ]
    ]
    .sort_values(by="title")
    .reset_index(drop=True)
)

pandas_result = (
    merged_df[
        [
            "title",
            "price_gbp",
            "rating",
            "category_name"
        ]
    ]
    .sort_values(by="title")
    .reset_index(drop=True)
)

results_are_equal = sql_result.equals(
    pandas_result
)
```

**Output:**

```text
SQL JOIN and pandas merge equivalent: True
```

### Interpretation

The comparison returned `True`, confirming that the SQL `JOIN` and pandas `merge()` generated equivalent results after aligning the selected columns and row ordering. This demonstrates that the normalized relational relationship between the `books` and `categories` tables can be reproduced correctly using pandas.

## Query Requirements Covered

| Requirement        | Query                            |
| ------------------ | -------------------------------- |
| `SELECT` / `WHERE` | Books above £40                  |
| `ORDER BY`         | Top 10 most expensive books      |
| `LIMIT`            | Top 10 most expensive books      |
| `DISTINCT`         | Distinct ratings                 |
| `BETWEEN`          | Books between £20 and £40        |
| `JOIN`             | Books with categories            |
| `pd.read_sql()`    | Expensive books and JOIN results |
| `pd.merge()`       | Reproduction of SQL JOIN         |
| Equality check     | SQL JOIN vs pandas merge         |

Overall, the executed queries cover all of the SQL operations required by the Module 1 specification, and the SQL JOIN has been independently reproduced using pandas.
