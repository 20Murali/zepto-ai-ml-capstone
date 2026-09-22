import sqlite3
from pathlib import Path
import pandas as pd

DATABASE_NAME = Path(__file__).parent / "zepto_books.db"

def create_connection():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        return conn
    except sqlite3.Error as e:
        print("Error while connecting to database:", e)
        return None

def query_expensive_books(connection):
    query = "SELECT title, price_gbp FROM books WHERE price_gbp > 40;"
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    return results

def query_top_10_expensive_books(connection):

    query = """
        SELECT title, price_gbp
        FROM books
        ORDER BY price_gbp DESC
        LIMIT 10
    """
    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    return results

def query_distinct_ratings(connection):

    query = """
        SELECT DISTINCT rating
        FROM books
        ORDER BY rating
    """

    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    return results

def query_books_in_price_range(connection):

    query = """
        SELECT title, price_gbp
        FROM books
        WHERE price_gbp BETWEEN 20 AND 40
        ORDER BY price_gbp
    """

    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    return results

def query_books_with_categories(connection):

    query = """
        SELECT
            b.title,
            b.price_gbp,
            b.rating,
            c.category_name
        FROM books AS b
        JOIN categories AS c
            ON b.category_id = c.category_id
        ORDER BY b.rating DESC
        LIMIT 10
    """

    cursor = connection.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    return results

def pandas_sql_queries(connection):

    query_1 = """
        SELECT title, price_gbp
        FROM books
        WHERE price_gbp > 40
    """

    query_2 = """
        SELECT
            b.title,
            b.price_gbp,
            b.rating,
            c.category_name
        FROM books AS b
        JOIN categories AS c
            ON b.category_id = c.category_id
        ORDER BY b.rating DESC
    """

    df_expensive = pd.read_sql(
        query_1,
        connection
    )

    df_join = pd.read_sql(
        query_2,
        connection
    )

    return df_expensive, df_join

def pandas_merge(connection):

    books_df = pd.read_sql(
        """
        SELECT
            book_id,
            title,
            price_gbp,
            price_inr,
            rating,
            in_stock,
            category_id
        FROM books
        """,
        connection
    )

    categories_df = pd.read_sql(
        """
        SELECT
            category_id,
            category_name
        FROM categories
        """,
        connection
    )

    merged_df = pd.merge(
        books_df,
        categories_df,
        on="category_id",
        how="inner"
    )

    return merged_df

if __name__ == "__main__":

    connection = create_connection()

    if connection is None:
        print("Could not connect to database.")
        exit()

    # --------------------------------------------------
    # 1. Run SQL queries
    # --------------------------------------------------

    print("\nBooks above £40:")
    results = query_expensive_books(connection)

    for row in results[:10]:
        print(row)


    print("\nTop 10 most expensive books:")
    results = query_top_10_expensive_books(connection)

    for row in results:
        print(row)


    print("\nDistinct ratings:")
    results = query_distinct_ratings(connection)

    for row in results:
        print(row)


    print("\nBooks between £20 and £40:")
    results = query_books_in_price_range(connection)

    for row in results[:10]:
        print(row)


    print("\nTop 10 books with categories:")
    results = query_books_with_categories(connection)

    for row in results:
        print(row)


    # --------------------------------------------------
    # 2. Read SQL results using pandas
    # --------------------------------------------------

    df_expensive, df_join = pandas_sql_queries(connection)

    print("\nPandas - Books above £40:")
    print(df_expensive.head(10))


    print("\nPandas - SQL JOIN result:")
    print(df_join)


    # --------------------------------------------------
    # 3. Reproduce SQL JOIN using pandas merge
    # --------------------------------------------------

    merged_df = pandas_merge(connection)

    print("\nPandas merge result:")
    print(
        merged_df[
            [
                "title",
                "price_gbp",
                "rating",
                "category_name"
            ]
        ].head(10)
    )


    # --------------------------------------------------
    # 4. Compare SQL JOIN and pandas merge
    # --------------------------------------------------

    sql_result = df_join[
        [
            "title",
            "price_gbp",
            "rating",
            "category_name"
        ]
    ].copy()

    pandas_result = merged_df[
        [
            "title",
            "price_gbp",
            "rating",
            "category_name"
        ]
    ].copy()


    # Sort both results so row order does not
    # affect the comparison

    sql_result = (
        sql_result
        .sort_values(by="title")
        .reset_index(drop=True)
    )

    pandas_result = (
        pandas_result
        .sort_values(by="title")
        .reset_index(drop=True)
    )


    results_are_equal = sql_result.equals(
        pandas_result
    )


    print(
        "\nSQL JOIN and pandas merge equivalent:",
        results_are_equal
    )


    connection.close()