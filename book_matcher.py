import os
import pandas as pd
import math
from language_processing import *
from API import *

class BookMatcher:
    def match_favorite_motives(self):
        fav_motives_user1 = []
        favorite_books_user1, favorite_books_user2 = self.extract_favorite_books()

        favorite_titles_user1 = favorite_books_user1['Book'].tolist()
        favorite_authors_user1 = favorite_books_user1['Author'].tolist()

        for i in range(len(favorite_titles_user1)):
            title, author, motives, cover = API_BOOKS.get_book_data(favorite_titles_user1[i], favorite_authors_user1[i]) 
            #print(title)
            if title == '' or author == '':
                continue
            if motives != 'No motives': 
                fav_motives_user1.append(Motives_list.m_list(motives))
        

        fav_motives_user2 = []
        favorite_titles_user2 = favorite_books_user2['Book'].tolist()
        favorite_authors_user2 = favorite_books_user2['Author'].tolist()
        
        for i in range(len(favorite_titles_user2)):
            title, author, motives, cover = API_BOOKS.get_book_data(favorite_titles_user2[i], favorite_authors_user2[i]) 
            #print(title)
            if title == '' or author == '':
                continue
            if motives != 'No motives': 
                fav_motives_user2.append(Motives_list.m_list(motives))

        return fav_motives_user1, fav_motives_user2


    def extract_favorite_books(self): 
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        base_path = os.path.join(project_dir, 'prediction')

        file1_name = 'user1_predictions.csv'
        file_path = os.path.join(base_path, file1_name)

        user1_data = pd.read_csv(file_path, encoding="utf-8", sep=';', header=None, skiprows=1)
        user1_data.columns = ['Author','Book','Rate'] 
        num_of_read_books = len(user1_data)
        num_of_fav_books = math.ceil(0.2 * num_of_read_books) 
        user1_sorted_data = user1_data.sort_values("Rate", ascending=False)
        favorite_books_user1 = user1_sorted_data.head(num_of_fav_books)
    

        file2_name = 'user2_predictions.csv'
        file_path = os.path.join(base_path, file2_name)

        user2_data = pd.read_csv(file_path, encoding="utf-8", sep=';', header=None, skiprows=1)
        user2_data.columns = ['Author','Book', 'Rate'] 
        num_of_read_books = len(user2_data)
        num_of_read_books = len(user2_data)
        num_of_fav_books = math.ceil(0.2 * num_of_read_books)
        user2_sorted_data = user2_data.sort_values("Rate", ascending=False)
        favorite_books_user2 = user2_sorted_data.head(num_of_fav_books)

        return favorite_books_user1, favorite_books_user2
   

