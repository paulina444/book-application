import csv

class IsBookInData:
    def load_books_from_csv(files):
        books = []
        for file in files:
            try:
                with open(file, newline="", encoding="utf-8") as f:
                    # Ustawienie średnika jako separatora
                    reader = csv.DictReader(f, delimiter=';')
                    for row in reader:
                        title = row.get("Book title", "").strip()
                        if title:
                            books.append(title)  # Dodajemy tytuł książki
            except FileNotFoundError:
                print(f"File {file} not found, skipping.")
        return books

    def is_book_in_database(book_title, database_books):
        return book_title in database_books