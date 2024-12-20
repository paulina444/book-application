from API import API_BOOKS
from language_processing import Motives_list

title = "The Atlas Six"
author = "Olivie Blake"

title, author, motives, cover = API_BOOKS.get_book_data(title, author)

motives = Motives_list.m_list(motives)
print(f"Tytuł: {title}")
print(f"Autor: {author}")
print(f"Motywy: {motives}")
