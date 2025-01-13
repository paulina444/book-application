from language_processing import *
from books_user_datasets import *
import requests
import sys

class API_BOOKS:

    def get_book_data(title, author):
        url = f"https://openlibrary.org/search.json?title={title}&author={author}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            title = ""
            author_name = ""
            motives = ""
            cover_id = ""

            if data['num_found'] > 0:
                book = data['docs'][0]
                
                title = book.get('title', '')
                author_name = ', '.join(book.get('author_name', ['']))
                motives = book.get('subject', 'No motives')
                cover_id = book.get('cover_i', None)
            
                if cover_id:
                    cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
                return title, author_name, motives, cover_id
            else:
                print("No books found that match your query.")
                return title, author_name, motives, cover_id
        else:
            print(f"Error while downloading data: {response.status_code}. Try again.")
            sys.exit(1)

    @staticmethod
    def get_books_by_motives(motives, limit=3, max_year=2024):
        database_books = IsBookInData.load_books_from_csv()

        motives_str = ','.join(motives)
        url = f"https://openlibrary.org/search.json?subject={motives_str}&sort=new"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()

            if data['num_found'] > limit:
                books = [
                    book for book in data['docs']
                    if any(year <= max_year for year in (book.get('first_publish_year', []) if isinstance(book.get('first_publish_year', []), list) else [book.get('first_publish_year')]))
                ]

                for book in books:
                    book_motives = book.get('subject', [])
                    book['matching_motives'] = [
                        motive for motive in motives if motive.lower() in [m.lower() for m in book_motives]
                    ]
                    book['match_count'] = len(book['matching_motives'])
                    book['all_motives'] = book_motives

                sorted_books = sorted(
                    books,
                    key=lambda b: (-b['match_count'], max((year for year in (b.get('first_publish_year', [0]) if isinstance(b.get('first_publish_year', [0]), list) else [b.get('first_publish_year')]) 
                    if year <= max_year), 
                    default=0))
                )

                books_with_all_motives = [
                    book for book in sorted_books if book['match_count'] == len(motives)
                ]

                top_books = (
                    books_with_all_motives[:limit]
                    if books_with_all_motives
                    else sorted_books[:limit]
                )

                result = []
                for book in top_books:
                    title = book.get('title', 'No title')
                    if not IsBookInData.is_book_in_database(title, database_books):
                        author_name = ', '.join(book.get('author_name', ['Unknown author']))
                        cover_id = book.get('cover_i', None)
                        cover_url = f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg" if cover_id else "No cover"
                        matching_motives = ', '.join(book.get('matching_motives', []))
                        all_motives = ', '.join(book.get('all_motives', []))

                        result.append({
                            "title": title,
                            "author": author_name,
                            "cover_url": cover_url,
                            "all_motives": all_motives,
                            "matching_motives": matching_motives,
                            "match_count": book['match_count'],
                        })

                return result
            else:
                result = API_BOOKS.get_books_by_motives(motives[:-1], limit, max_year=2024)
                
                if result == []:
                    return {"error": "No books found that match the themes."}
                else:
                    return result
        else:
            return {"error": f"Error while downloading data: {response.status_code}"}

