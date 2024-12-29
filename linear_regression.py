from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
import spacy

class Model:
    def linear_regression(test_file1, test_file2):
        data_file = './data_train/train.xlsx'
        #test_file1 = './reviews/agatas_reviews.csv'

        df = pd.read_excel(data_file)

        opinie_cyfrowe = df.iloc[:, 0].tolist()
        opinie_tekstowe = df.iloc[:, 1].tolist()

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

        X_train = vectorizer.fit_transform(opinie_tekstowe)

        y_train = np.array(opinie_cyfrowe)

        model = LinearRegression()
        model.fit(X_train, y_train)


        test_df = pd.read_csv(test_file1, encoding="utf-8", sep=';', header=None, skiprows=1)
        test_df.columns = ['Book', 'Author', 'Review'] 

        test_texts = test_df['Review'].tolist()  
        
        print("First user:")
        if not test_texts:
            print("no texts to evaluate")
            exit()

        # Transformacja danych testowych na macierz TF-IDF
        X_test = vectorizer.transform(test_texts)

        predictions = model.predict(X_test)

        for prediction in predictions:
            print(f"{prediction}\n")

        
        test_df2 = pd.read_csv(test_file2, encoding="utf-8", sep=';', header=None, skiprows=1)
        test_df2.columns = ['Book', 'Author', 'Review'] 

        test_texts2 = test_df2['Review'].tolist()  

        print("Second user:")
        if not test_texts2:
            print("no texts to evaluate")
            exit()

        # Transformacja danych testowych na macierz TF-IDF
        X_test2 = vectorizer.transform(test_texts2)

        predictions2 = model.predict(X_test2)

        for prediction2 in predictions2:
            print(f"{prediction2}\n")
