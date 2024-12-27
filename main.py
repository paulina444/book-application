from API import API_BOOKS
from language_processing import Motives_list
from scrapper_reviews import *

# title = "The Atlas Six"
# author = "Olivie Blake"

# title, author, motives, cover = API_BOOKS.get_book_data(title, author)

# motives = Motives_list.m_list(motives)
# print(f"Tytuł: {title}")
# print(f"Autor: {author}")
# print(f"Motywy: {motives}")


#####
GoodReadsReviewsScrapper.scrape_user_reviews(185172573,'agata')
GoodReadsReviewsScrapper.scrape_user_reviews(185192685, 'paulina')

# https://www.goodreads.com/review/list/185192685-paulina?shelf=read