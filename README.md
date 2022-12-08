# ISBN Scraper 📚

![GitHub Pipenv locked Python version](https://img.shields.io/github/pipenv/locked/python-version/Durhamster/ISBN_Scraper?color=blue&style=for-the-badge)
![License](https://img.shields.io/github/license/Durhamster/ISBN_Scraper?style=for-the-badge)

Scrape the title, author(s), public domain info, page count, language, & brief summary for a list of books based on their ISBNs.

To use this script, install the required libraries, add a list of ISBNs, and run app.py.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the required libraries.

```bash
pip install -r requirements.txt
```

or

Using [pipenv](https://pipenv.pypa.io/en/latest/):

```bash
pipenv install
```

## Usage

To scrape your list of ISBNs, you must do the following:

1. Add your list as a CSV file in 'Data' directory.
2. Open app.py and change the name of the file on line 81.

```bash
   isbns = pd.read_csv("<YourISBNsGoHere.csv>")
```

3. Run app.py. The final output will be saved as 'Final_Inventory.csv'.
