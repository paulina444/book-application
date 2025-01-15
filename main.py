from API import API_BOOKS
from language_processing import Motives_list
from reviews_scrapper import *
from lightgbm_model import *
from model_bert import *
from book_matcher import *
from motives_list import *

def main():
    user1_name = input("\n\nEnter the nickname of the first user: ")   

    while True:
        user1_id = input("Enter the id of the first user: ")
        if user1_id.isdigit():  
            user1_id = int(user1_id) 
            break  
        else:
            print("Please, enter your id again, it must be a number.")

    user2_name = input("\nEnter the nickname of the second user: ") 

    while True:
        user2_id = input("Enter the id of the second user: ")
        if user2_id.isdigit():  
            user2_id = int(user2_id) 
            break  
        else:
            print("Please, enter your id again, it must be a number.")

    # dane do testów: 
 
    # user1_id = 185385208
    # user1_name = 'romcom'

        
    '''
    user2_id = 185382409
    user2_name = 'horror1995'
    '''

    # user2_id = 165736606
    # user2_name = 'lexi'



    '''
    user1_id = 185192685
    user1_name = 'paulina'
    '''

    ''' #jakiś user bez żadnej książki
    user2_id = 1702015
    user2_name = 'xsc'
    '''

    test_file1 = GoodReadsReviewsScrapper.scrape_user_reviews(user1_id, user1_name)
    test_file2 = GoodReadsReviewsScrapper.scrape_user_reviews(user2_id, user2_name)

    # Model.lightgbm_regression(test_file1, test_file2)
    # Model_Bert.train_bert()
    Model_Bert.bert(test_file1, test_file2)

    GoodReadsReviewsScrapper.join_files('user1',user1_id, user1_name)
    GoodReadsReviewsScrapper.join_files('user2',user2_id, user2_name)
    matcher = BookMatcher()
    motives_user1, motives_user2 = matcher.match_favorite_motives()

    fav_motive_user1 = GetFavouriteMotives.count_motives(motives_user1)
    fav_motive_user2 = GetFavouriteMotives.count_motives(motives_user2)

    motive_set = GetFavouriteMotives.get_motives_for_both(fav_motive_user1, fav_motive_user2)
    recommended_books = API_BOOKS.get_books_by_motives(motive_set, limit = 5)

   
    if isinstance(recommended_books, list):
         print(f"Your common favorite motifs {motive_set} \n")
         for idx, book in enumerate(recommended_books, start=1):
             print(f"Book {idx}:")
             print(f"Title: {book['title']}")
             print(f"Author: {book['author']}")
             print(f"Motifs in the book: {book['all_motives']}")
             print("-" * 40)
    else:
         print(recommended_books["error"])
    

if __name__ == "__main__":
    main()