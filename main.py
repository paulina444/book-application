from API import API_BOOKS
from language_processing import Motives_list
from reviews_scrapper import *
from linear_regression import Model
from book_matcher import *
from motives_list import *

def main():
    # user1_name = input("Enter the nickname of the first user: ")   

    # while True:
    #     user1_id = input("Enter the id of the first user: ")
    #     if user1_id.isdigit():  
    #         user1_id = int(user1_id) 
    #         break  
    #     else:
    #         print("Please, enter your id again, it must be a number.")

    # user2_name = input("\nEnter the nickname of the second user: ") 

    # while True:
    #     user2_id = input("Enter the id of the second user: ")
    #     ifgtg user2_id.isdigit():  
    #         user2_id = int(user2_id) 
    #         break  
    #     else:
    #         print("Please, enter your id again, it must be a number.")

    # TODO trzeba bedzie wstawic zmienne gdy użyjemy kodu co jest do góry 
    
    #test_file1 = GoodReadsReviewsScrapper.scrape_user_reviews(185172573,'agata')
    #test_file2 = GoodReadsReviewsScrapper.scrape_user_reviews(185192685, 'paulina')
    test_file3 = GoodReadsReviewsScrapper.scrape_user_reviews(185385208, 'romcom')
    test_file4 = GoodReadsReviewsScrapper.scrape_user_reviews(185382409, 'horror1995')

    Model.linear_regression(test_file3, test_file4)
     # TODO odpalic nowego scrappera i dopisac te ksiazki i oceny do predictions
    
    matcher = BookMatcher()
    motives_user1, motives_user2 = matcher.match_favorite_motives()

    fav_motive_user1 = GetFavouriteMotives.count_motives(motives_user1)
    #print("słownik motywów 1: " + str(fav_motive_user1))
    fav_motive_user2 = GetFavouriteMotives.count_motives(motives_user2)
    #print("słownik motywów 2: " + str(fav_motive_user2))

    motive_set = GetFavouriteMotives.get_motives_for_both(fav_motive_user1, fav_motive_user2)

    #recommended_books = API_BOOKS.get_books_by_motives(motive_set)
    
   
    recommended_books = API_BOOKS.get_books_by_motives(motive_set, limit = 5)

   
    if isinstance(recommended_books, list):
         for idx, book in enumerate(recommended_books, start=1):
             print(f"Book {idx}:")
             print(f"Tytuł: {book['title']}")
             print(f"Autor: {book['author']}")
             # print(f"Rok publikacji: {book['publish_year']}")
             # print(f"Okładka: {book['cover_url']}")
             print(f"Motives of book: {book['all_motives']}")
             print(book['matching_motives'])
             print("-" * 40)
    else:
         print(recommended_books["error"])
    
    

if __name__ == "__main__":
    main()