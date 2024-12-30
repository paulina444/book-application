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
        
        print("First user:")
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

        for prediction in predictions:
            print(f"{prediction}\n")

        with open(file_path, 'w',newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Book', "Rate"])

            for i in range(len(predictions)):
                writer.writerow([book_titles[i], predictions[i]])
      

        
        test_df2 = pd.read_csv(test_file2, encoding="utf-8", sep=';', header=None, skiprows=1)
        test_df2.columns = ['Author', 'Book', 'Review'] 

        test_texts2 = test_df2['Review'].tolist()  
        book_titles2 = test_df2['Book'].tolist()  

        print("Second user:")
        if not test_texts2:
            print("no texts to evaluate")
            exit()

        # Transformacja danych testowych na macierz TF-IDF
        X_test2 = vectorizer.transform(test_texts2)

        predictions2 = model.predict(X_test2)


        file_name = 'user2_predictions.csv'
        file_path = os.path.join(base_path, file_name)

        for prediction2 in predictions2:
                print(f"{prediction2}\n")

        with open(file_path, 'w', newline='') as file:   
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Book', "Rate"])

            for i in range(len(predictions2)):
                writer.writerow([book_titles2[i], predictions2[i]])

    def predict_users_rate():
        pass
