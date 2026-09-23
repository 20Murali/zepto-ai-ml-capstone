import requests
from bs4 import BeautifulSoup
import math
import pandas as pd


def get_categories(URL):

    all_categories = []

    try:
        response = requests.get(URL, timeout=10)

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        categories = soup.select(".side_categories li li a")

        for category in categories:
            all_categories.append({
                "category": category.get_text(strip=True),
                "URL": category.get("href")
            })

    except requests.exceptions.RequestException as e:
        print("Error while requesting URL:", e)

    except Exception as e:
        print("Unexpected error:", e)

    return all_categories

def get_books_count(soup):
    books_count = soup.select_one("form.form-horizontal strong")
    return int(books_count.get_text(strip=True))


def scrape_books(url, category):
    
    all_books = []
    
    try:
        print(f"Scraping: {url}")

        response = requests.get(url, timeout=10)

        print("Status code:", response.status_code)

        response.raise_for_status()

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        total_books_count = get_books_count(soup)

        print("Total books:", total_books_count)

        pages_count = math.ceil(total_books_count / 20)

        print("Total pages:", pages_count)

        for page in range(1, pages_count + 1):

            print(f"Scraping page {page}...")
            
            if page == 1:
                page_soup = soup

            else:
                page_url = url.replace("index.html", f"page-{page}.html")
                response = requests.get(page_url, timeout=10)
                response.raise_for_status()
                page_soup = BeautifulSoup(response.text, "html.parser")

            books = page_soup.select("article.product_pod")

            print("Books found:", len(books))

            for book in books:
                
                title = book.h3.a["title"]
                price = book.select_one(".price_color").get_text(strip=True)
                rating = book.select_one("p.star-rating")["class"][1]
                availability = book.select_one(".availability").get_text(strip=True)

                all_books.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "availability": availability,
                    "category": category
                })

    except requests.exceptions.RequestException as e:
        print("Request error:", e)

    except Exception as e:
        print("Unexpected error:", e)

    return all_books

#Get all books
def get_all_books(BaseURL,category_limit=5):

    Categories = get_categories(BaseURL)

    all_books = []

    for category in Categories[:category_limit]:

        category_name = category["category"]

        category_url = BaseURL + category["URL"]

        books = scrape_books(category_url, category_name)

        all_books.extend(books)

    print("Total books scraped:", len(all_books))

    return all_books

#clean the data
def clean_data(all_books):

    df = pd.DataFrame(all_books)

    df["price_gbp"] = pd.to_numeric(
    df["price"].str.replace("Â£", ""),
    errors="coerce"
    )


    rating_map = {
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    df["rating"] = df["rating"].map(rating_map)

    df["in_stock"] = df["availability"].str.contains("In stock",case=False,na=False)
    #Capstone requirement: fixed conversion rate of 1 GBP = 105.50 INR.
    df["price_inr"] = df["price_gbp"] * 105.50
    df["price_inr"] = df["price_inr"].round(2)

    df["title"] = df["title"].str.encode("latin1").str.decode("utf-8")
    df = df.drop(columns=["price", "availability"])

    print(df.head())
    print(df.dtypes)
    print(len(df))
    print(df["category"].nunique())

    return df

def build_dataset(category_limit=5):
    URL = "https://books.toscrape.com/"
    all_books=get_all_books(URL,category_limit)
    df=clean_data(all_books)

    return df

if __name__ == "__main__":

    df = build_dataset()
    
    

    print("\nFinal dataset:")
    print(df.head())
    print("\nShape:")
    print(df.shape)
    