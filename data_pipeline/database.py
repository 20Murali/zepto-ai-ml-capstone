import sqlite3
from scrape_books import build_dataset
from pathlib import Path


DATABASE_NAME = Path(__file__).parent / "zepto_books.db"

if DATABASE_NAME.exists():
    DATABASE_NAME.unlink()

def create_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection


def create_tables(connection):

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS categories (
            category_id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_name TEXT NOT NULL UNIQUE
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            price_gbp REAL,
            price_inr REAL,
            rating INTEGER,
            in_stock BOOLEAN,
            category_id INTEGER,
            FOREIGN KEY (category_id)
            REFERENCES categories(category_id)
        )
    """)

    connection.commit()

def insert_categories(connection, df):

    cursor = connection.cursor()

    categories = df["category"].drop_duplicates()

    for category in categories:

        cursor.execute(
            """
            INSERT OR IGNORE INTO categories (category_name)
            VALUES (?)
            """,
            (category,)
        )

    connection.commit()


def insert_books(connection, df):

    cursor = connection.cursor()

    for _, book in df.iterrows():

        cursor.execute(
            """
            SELECT category_id
            FROM categories
            WHERE category_name = ?
            """,
            (book["category"],)
        )

        category_id = cursor.fetchone()[0]

        cursor.execute(
            """
            INSERT INTO books (
                title,
                price_gbp,
                price_inr,
                rating,
                in_stock,
                category_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                book["title"],
                book["price_gbp"],
                book["price_inr"],
                book["rating"],
                book["in_stock"],
                category_id
            )
        )

    connection.commit()

def verify_database(connection):

    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM books")
    book_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM categories")
    category_count = cursor.fetchone()[0]

    print("\nDatabase verification:")
    print("Books in database:", book_count)
    print("Categories in database:", category_count)

if __name__ == "__main__":

    print("Building dataset...")

    df = build_dataset(10)

    print(f"Books scraped: {len(df)}")
    print(f"Categories found: {df['category'].nunique()}")

    connection = create_connection()

    create_tables(connection)

    insert_categories(connection, df)

    insert_books(connection, df)

    print("Data inserted successfully.")

    verify_database(connection)

    connection.close()