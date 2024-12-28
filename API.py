import requests

class API_BOOKS:
    def get_book_data(title, author):
        # zapytanie do API
        url = f"https://openlibrary.org/search.json?title={title}&author={author}"
        
        # Wysyłanie zapytania
        response = requests.get(url)
        
        # Sprawdza, czy odpowiedź jest poprawna (status kod 200)
        if response.status_code == 200:
            data = response.json()
            
            # sprawdza czy znaleziono książki
            if data['num_found'] > 0:
                # pierwsza książka z wyników
                book = data['docs'][0]
                
                # Wydobywamy informacje o książce
                title = book.get('title', 'Brak tytułu')
                author_name = ', '.join(book.get('author_name', ['Brak autora']))
                motives = book.get('subject', 'Brak motywów')
                cover_id = book.get('cover_i', None)
                
                #print(f"Tytuł: {title}")
                #print(f"Autor: {author_name}")
                #print(f"Motywy: {motives}")
                
                # Jeśli istnieje cover_id, można pobrać okładkę
                if cover_id:
                    cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                    #print(f"Okładka książki: {cover_url}")
                return title, author_name, motives, cover_id
            else:
                print("Nie znaleziono książek pasujących do zapytania.")
        else:
            print(f"Błąd podczas pobierania danych: {response.status_code}")
