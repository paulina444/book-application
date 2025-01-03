import requests

class API_BOOKS:
    def get_book_data(title, author):
        url = f"https://openlibrary.org/search.json?title={title}&author={author}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # sprawdza czy znaleziono książki
            if data['num_found'] > 0:
                # pierwsza książka z wyników
                book = data['docs'][0]
                
                # informacje o książce
                title = book.get('title', '')
                author_name = ', '.join(book.get('author_name', ['']))
                motives = book.get('subject', 'No motives')
                cover_id = book.get('cover_i', None)
            
                # Jeśli istnieje cover_id, można pobrać okładkę
                if cover_id:
                    cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                return title, author_name, motives, cover_id
            else:
                print("Nie znaleziono książek pasujących do zapytania.")
        else:
            print(f"Błąd podczas pobierania danych: {response.status_code}")



    @staticmethod
    def get_books_by_motive(motive, limit=3, max_year=2024):
        url = f"https://openlibrary.org/search.json?subject={motive}&sort=new"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            # sprawdza, czy znaleziono książki
            if data['num_found'] > 0:
                # filtr książek z rokiem publikacji - domyślnie <= 2024, ale można wybrać
                books = [
                    book for book in data['docs']
                    if any(year <= max_year for year in book.get('publish_year', []))
                ]

                # Sort książek według najnowszego roku publikacji (maksymalny rok w publish_year)
                sorted_books = sorted(
                    books,
                    key=lambda b: max((y for y in b.get('publish_year', [0]) if y <= max_year), default=0),
                    reverse=True
                )

                # określoną liczbę książek (limit)
                top_books = sorted_books[:limit]

                #  listę informacji o książkach
                result = []
                for book in top_books:
                    title = book.get('title', 'Brak tytułu')
                    author_name = ', '.join(book.get('author_name', ['Nieznany autor']))
                    publish_year = max((y for y in book.get('publish_year', [0]) if y <= max_year), default=0)
                    cover_id = book.get('cover_i', None)
                    cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else "Brak okładki"

                    result.append({
                        "title": title,
                        "author": author_name,
                        "publish_year": publish_year,
                        "cover_url": cover_url,
                    })

                return result
            else:
                return {"error": "Nie znaleziono książek pasujących do podanego motywu."}
        else:
            return {"error": f"Błąd podczas pobierania danych: {response.status_code}"}

