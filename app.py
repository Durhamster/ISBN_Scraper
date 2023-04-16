import json
import pandas as pd
import textwrap
import urllib.request
from os import getcwd, startfile
from rich import print
from rich.console import Console
from rich.progress import Progress
from time import sleep, time

"""Gets Book Info from Google APIs based on the ISBN

Args:
    isbn (str): ISBN Number

Returns:
    Book title (str), authors (str), public_domain (bool),
    page_count (int), language (str), summary (str)
"""


def get_book(isbn):
    base_api_link = "https://www.googleapis.com/books/v1/volumes?q=isbn:"

    with urllib.request.urlopen(base_api_link + str(isbn)) as book:
        text = book.read()

    decoded_text = text.decode("utf-8")
    obj = json.loads(decoded_text)

    # Exception for incorrect ISBNs
    try:
        volume_info = obj["items"][0]
        book_authors = obj["items"][0]["volumeInfo"]["authors"]

        title = volume_info["volumeInfo"]["title"]
        authors = ", ".join(book_authors)
        public_domain = volume_info["accessInfo"]["publicDomain"]
        page_count = volume_info["volumeInfo"]["pageCount"]
        language = volume_info["volumeInfo"]["language"]
        summary = textwrap.fill(volume_info["searchInfo"]["textSnippet"], width=65)

    except KeyError:
        title, authors, public_domain, page_count, language, summary = (
            "N/A - Check ISBN Number",
            " ",
            " ",
            " ",
            " ",
            " ",
        )

    return title, authors, public_domain, page_count, language, summary


"""Converts seconds at the end to show how long the scraping and formatting process took
----------
seconds : raw seconds from time() - start_time
"""


def convert_time(seconds):

    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%d:%02d:%02d" % (hour, minutes, seconds)


if __name__ == "__main__":

    start_time = time()

    cwd = getcwd()
    console = Console()

    # Reads ISBNs into a list
    isbns = pd.read_csv("Data/Test_Inventory.csv")
    books = isbns["ISBN"].to_list()

    books_dict = dict()
    final_book_df = pd.DataFrame(books_dict)
    book_list = []

    print(f"[cyan]Fetching data for {len(books)} books...\n")

    with Progress() as progress:

        task = progress.add_task("[green]Fetching...[/green]", total=len(books))
        for book in books:
            if book == "":
                pass
            else:
                title, authors, public_domain, page_count, language, summary = get_book(
                    book
                )
                book_dict = dict(
                    {
                        "Title": title,
                        "Authors": authors,
                        "ISBN": book,
                        "Public Domain": public_domain,
                        "Page Count": page_count,
                        "Language": language,
                        "Summary": summary,
                    }
                )
                book_df = pd.DataFrame(book_dict, index=[0])
                final_book_df = pd.concat([final_book_df, book_df], ignore_index=True)
                progress.update(task, advance=1)

                # Pause to prevent too many HTTP Requests
                sleep(5)

    # Generates CSV file for final df
    final_book_df.reset_index()
    final_book_df.to_csv("Final_Inventory.csv", index=False)

    print("Job completed in", convert_time(round(time() - start_time, 2)), "⏰")
    print(f"File saved as {cwd+'/Final_Inventory.csv'}\n")

    openSheet = " "
    while (openSheet != "y") and (openSheet != "n"):
        openSheet = console.input(
            "\nDo you want to open the file? [cyan](y or n)[/cyan]: \n"
        ).lower()

    if openSheet == "y":
        startfile(f"{cwd}/{'Final_Inventory.csv'}")
        print("Opening file...\n")
        sleep(3)
    else:
        print("\n")
