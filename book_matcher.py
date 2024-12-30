import os
import pandas as pd
class BookMatcher:
    def match_favorite_motives():
        pass

    def match_favorite_books(user_id, user_name): # potrzebujej jak moj model nadal oceny moim opinia (ksiazka - opinia)
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        base_path = os.path.join(project_dir, 'reviews')

        file_name = user_name + 's_'+ str(user_id) + '_reviews.csv'
        file_path = os.path.join(base_path, file_name)

        user_data = pd.read_csv(file_path, encoding="utf-8", sep=';', header=None, skiprows=1)
        user_data.columns = ['Book', 'Author', 'Review'] 
        reviews = test_df['Review'].tolist()  
     
   

