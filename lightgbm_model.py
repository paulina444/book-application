from sklearn.feature_extraction.text import TfidfVectorizer
import os
import csv
import numpy as np
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
import lightgbm as lgb
from pandas.errors import EmptyDataError
import sys
from reviews_scrapper import *

class Model:

    def lightgbm_regression(test_file1, test_file2):
        data_file = './data_train/train.xlsx'

        df = pd.read_excel(data_file)

        rates = df.iloc[:, 0].tolist()
        reviews = df.iloc[:, 1].tolist()

        # model językowy spaCy
        nlp = spacy.load("en_core_web_sm")

        # tokenizacja przy użyciu spaCy
        def preprocess_and_tokenize(text):
            doc = nlp.make_doc(text.lower())
            return [token.text for token in doc if not token.is_stop and not token.is_punct]

        vectorizer = TfidfVectorizer(
            max_features=2000,
            min_df=5,
            tokenizer=preprocess_and_tokenize,
            token_pattern=None
        )

        X_train = vectorizer.fit_transform(reviews)
        y_train = np.array(rates)

        # Konwersja macierzy na LightGBM Dataset
        train_data = lgb.Dataset(X_train, label=y_train)

        # Parametry LightGBM
        params = {
            'objective': 'regression',
            'metric': 'rmse',
            'boosting_type': 'gbdt',
            'learning_rate': 0.1,
            'num_leaves': 31,
            'max_depth': -1,
            'verbosity': 0,  # Wycisz komunikaty
        }

        # Trening modelu
        model = lgb.train(params, train_data, num_boost_round=100)

        # przetwarzanie pierwszego pliku testowego
        try:
            test_df = pd.read_csv(test_file1, encoding="utf-8", sep=';', header=None, skiprows=1)
        except EmptyDataError:
            print("Plik jest pusty lub nie zawiera danych do przetworzenia.")
            sys.exit(1)
        except FileNotFoundError:
            print("Plik nie został znaleziony. Sprawdź ścieżkę.")
            sys.exit(1)
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")
            sys.exit(1)
        
        test_df.columns = ['Author', 'Book', 'Review']
        test_texts = test_df['Review'].tolist()
        book_titles = test_df['Book'].tolist()
        book_authors = test_df['Author'].tolist()

        #print("First user:")
        if not test_texts:
            print("no texts to evaluate")
            exit()

        # transformacja danych testowych na macierz TF-IDF
        X_test = vectorizer.transform(test_texts)
        predictions = model.predict(X_test)

        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        base_path = os.path.join(project_dir, 'prediction')

        file_name = 'user1_predictions.csv'
        file_path = os.path.join(base_path, file_name)

        # for prediction in predictions:
        #     print(f"{prediction}\n")

        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Author', 'Book', 'Rate'])

            for i in range(len(predictions)):
                writer.writerow([book_authors[i], book_titles[i], predictions[i]])
        try: 
            test_df2 = pd.read_csv(test_file2, encoding="utf-8", sep=';', header=None, skiprows=1)
        except EmptyDataError:
            print("Plik jest pusty lub nie zawiera danych do przetworzenia.")
            sys.exit(1)
        except FileNotFoundError:
            print("Plik nie został znaleziony. Sprawdź ścieżkę.")
            sys.exit(1)
        except Exception as e:
            print(f"Wystąpił nieoczekiwany błąd: {e}")
            sys.exit(1)

        test_df2.columns = ['Author', 'Book', 'Review']
        test_texts2 = test_df2['Review'].tolist()
        book_titles2 = test_df2['Book'].tolist()
        book_authors2 = test_df2['Author'].tolist()

        #print("Second user:")
        if not test_texts2:
            print("no texts to evaluate")
            exit()

        # Transformacja danych testowych na macierz TF-IDF
        X_test2 = vectorizer.transform(test_texts2)
        predictions2 = model.predict(X_test2)

        file_name = 'user2_predictions.csv'
        file_path = os.path.join(base_path, file_name)

        # for prediction2 in predictions2:
        #     print(f"{prediction2}\n")

        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Author', 'Book', 'Rate'])

            for i in range(len(predictions2)):
                writer.writerow([book_authors2[i], book_titles2[i], predictions2[i]])
        
        GoodReadsReviewsScrapper.delete_file(test_file1)
        GoodReadsReviewsScrapper.delete_file(test_file2)

'''
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import spacy
import os
import csv

class Model:
    def linear_regression(test_file1, test_file2):
        data_file = './data_train/train.xlsx'
        #test_file1 = './reviews/agatas_reviews.csv'

        df = pd.read_excel(data_file)

        rates = df.iloc[:, 0].tolist()
        reviews = df.iloc[:, 1].tolist()

        # model językowy spaCy
        nlp = spacy.load("en_core_web_sm")

        # tokenizacja przy użyciu spaCy
        def preprocess_and_tokenize(text):
            doc = nlp.make_doc(text.lower()) 
            return [token.text for token in doc if not token.is_stop and not token.is_punct]

        # Tworzenie wektoryzatora TF-IDF
        vectorizer = TfidfVectorizer(
            max_features=2000,        # Maksymalna liczba tokenów w słowniku
            min_df=5,                 # Tokeny muszą występować w co najmniej 5 dokumentach
            tokenizer=preprocess_and_tokenize,  
            token_pattern=None        # wyłączone używanie token_pattern, ponieważ mamy własny tokenizer
        )

        X_train = vectorizer.fit_transform(reviews)

        y_train = np.array(rates)

        model = LinearRegression()
        model.fit(X_train, y_train)


        test_df = pd.read_csv(test_file1, encoding="utf-8", sep=';', header=None, skiprows=1)
        test_df.columns = ['Author', 'Book', 'Review'] 

        test_texts = test_df['Review'].tolist() 
        book_titles = test_df['Book'].tolist()
        book_authors = test_df['Author'].tolist()
        
        #print("First user:")
        if not test_texts:
            print("no texts to evaluate")
            exit()

        # Transformacja danych testowych na macierz TF-IDF
        X_test = vectorizer.transform(test_texts)

        predictions = model.predict(X_test)


        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        base_path = os.path.join(project_dir, 'prediction')

        file_name = 'user1_predictions.csv'
        file_path = os.path.join(base_path, file_name)

        # for prediction in predictions:
        #     print(f"{prediction}\n")

        with open(file_path, 'w',newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Author','Book', "Rate"])

            for i in range(len(predictions)):
                writer.writerow([book_authors[i], book_titles[i], predictions[i]])
      

        
        test_df2 = pd.read_csv(test_file2, encoding="utf-8", sep=';', header=None, skiprows=1)
        test_df2.columns = ['Author', 'Book', 'Review'] 

        test_texts2 = test_df2['Review'].tolist()  
        book_titles2 = test_df2['Book'].tolist()
        book_authors2 = test_df2['Author'].tolist()

        #print("Second user:")
        if not test_texts2:
            print("no texts to evaluate")
            exit()

        # Transformacja danych testowych na macierz TF-IDF
        X_test2 = vectorizer.transform(test_texts2)

        predictions2 = model.predict(X_test2)


        file_name = 'user2_predictions.csv'
        file_path = os.path.join(base_path, file_name)

        # for prediction2 in predictions2:
        #         print(f"{prediction2}\n")

        with open(file_path, 'w', newline='') as file:   
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Author','Book', "Rate"])

            for i in range(len(predictions2)):
                writer.writerow([book_authors2[i], book_titles2[i], predictions2[i]])
'''