from API import API_BOOKS
from language_processing import Motives_list
from reviews_scrapper import *

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
    #     if user2_id.isdigit():  
    #         user2_id = int(user2_id) 
    #         break  
    #     else:
    #         print("Please, enter your id again, it must be a number.")

    # TODO trzeba bedzie wstawic zmienne gdy użyjemy kodu co jest do góry 
    GoodReadsReviewsScrapper.scrape_user_reviews(185172573,'agata')
    GoodReadsReviewsScrapper.scrape_user_reviews(185192685, 'paulina')





    # title = "The Atlas Six"
    # author = "Olivie Blake"

    # title, author, motives, cover = API_BOOKS.get_book_data(title, author)

    # motives = Motives_list.m_list(motives)
    # print(f"Tytuł: {title}")
    # print(f"Autor: {author}")
    # print(f"Motywy: {motives}")


if __name__ == "__main__":
    main()