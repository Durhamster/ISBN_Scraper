import json
import pandas as pd
import textwrap
import urllib.request

# Reads ISBNs into a list
isbns = pd.read_excel("Data/Test_Inventory.xlsx")
books = isbns["ISBN"].to_list()


"""Gets Book Info from Google APIs based on the ISBN

Args:
    isbn (str): ISBN Number

Returns:
    Book title (str), authors (str), public_domain (bool),
    page_count (int), language (str), summary (str)
"""


def get_book(isbn):
    base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

    with urllib.request.urlopen(base_api_link + isbn) as f:
        text = f.read()

    decoded_text = text.decode("utf-8")
    obj = json.loads(decoded_text)
    volume_info = obj["items"][0]
    book_authors = obj["items"][0]["volumeInfo"]["authors"]

    title = volume_info["volumeInfo"]["title"]
    authors = ", ".join(book_authors)
    public_domain = volume_info["accessInfo"]["publicDomain"]
    page_count = volume_info["volumeInfo"]["pageCount"]
    language = volume_info["volumeInfo"]["language"]
    summary = textwrap.fill(volume_info["searchInfo"]["textSnippet"], width=65)

    return title, authors, public_domain, page_count, language, summary


books_dict = dict()
final_book_df = pd.DataFrame(books_dict)
book_list = []

for book in books:
    title, authors, public_domain, page_count, language, summary = get_book(book)
    book_dict = dict(
        {
            "Title": title,
            "Authors": authors,
            "Public Domain": public_domain,
            "Page Count": page_count,
            "Language": language,
            "Summary": summary,
        }
    )
    book_df = pd.DataFrame(book_dict, index=[0])
    final_book_df = pd.concat([final_book_df, book_df], ignore_index=True)


final_book_df.reset_index()

print(final_book_df)
