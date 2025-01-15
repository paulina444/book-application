from transformers import BertTokenizer, BertForSequenceClassification
from transformers import Trainer, TrainingArguments
from pandas.errors import EmptyDataError
from datasets import Dataset
from reviews_scrapper import *
import pandas as pd
import torch
import sys
import os
import csv


class Model_Bert:

    def train_bert():
        data_file = './data_train/train2.xlsx' #lub train

        df = pd.read_excel(data_file)
        
        df.iloc[:, 0] = df.iloc[:, 0] - 1
        rates = df.iloc[:, 0].tolist()
        reviews = df.iloc[:, 1].tolist()

        data = {'text': reviews, 'label': rates}
        df = pd.DataFrame(data)

        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        def preprocess_function(examples):
            return tokenizer(examples['text'], truncation=True, padding=True, max_length=128)

        dataset = Dataset.from_pandas(df)
        dataset = dataset.map(preprocess_function, batched=True)
        dataset = dataset.train_test_split(test_size=0.2, seed=42)

        model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=5)

        training_args = TrainingArguments(
            output_dir='./results',
            eval_strategy="epoch",
            learning_rate=2e-5,
            per_device_train_batch_size=8,
            num_train_epochs=3,
            weight_decay=0.01
        )

        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=dataset['train'],
            eval_dataset=dataset['test']
        )
        trainer.train()

        model.save_pretrained('./saved_model')
        tokenizer.save_pretrained('./saved_model')

        return model, tokenizer


    def bert(test_file1, test_file2):
        model = BertForSequenceClassification.from_pretrained('./saved_model')
        tokenizer = BertTokenizer.from_pretrained('./saved_model')
        
        try:
            test_df = pd.read_csv(test_file1, encoding="utf-8", sep=';', header=None, skiprows=1)
        except EmptyDataError:
            print("The file is empty or contains no data to process.")
            sys.exit(1)
        except FileNotFoundError:
            print("File not found.")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)
        
        test_df.columns = ['Author', 'Book', 'Review']
        test_texts = test_df['Review'].tolist()
        book_titles = test_df['Book'].tolist()
        book_authors = test_df['Author'].tolist()

        if not test_texts:
            print("no texts to evaluate")
            exit()

        X_test = tokenizer(test_texts, return_tensors="pt", truncation=True, padding=True, max_length=128)

        with torch.no_grad():  
            outputs = model(**X_test)

        logits = outputs.logits
        predictions = torch.argmax(logits, dim=1).tolist()

        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        base_path = os.path.join(project_dir, 'prediction')

        file_name = 'user1_predictions.csv'
        file_path = os.path.join(base_path, file_name)

        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Author', 'Book', 'Rate'])

            for i in range(len(predictions)):
                writer.writerow([book_authors[i], book_titles[i], predictions[i] + 1])
        
        try: 
            test_df2 = pd.read_csv(test_file2, encoding="utf-8", sep=';', header=None, skiprows=1)
        except EmptyDataError:
            print("The file is empty or contains no data to process.")
            sys.exit(1)
        except FileNotFoundError:
            print("File not found.")
            sys.exit(1)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            sys.exit(1)

        test_df2.columns = ['Author', 'Book', 'Review']
        test_texts2 = test_df2['Review'].tolist()
        book_titles2 = test_df2['Book'].tolist()
        book_authors2 = test_df2['Author'].tolist()

        if not test_texts2:
            print("no texts to evaluate")
            exit()

        X_test2 = tokenizer(test_texts2, return_tensors="pt", truncation=True, padding=True, max_length=128)
 
        with torch.no_grad():  
            outputs2 = model(**X_test2)

        logits2 = outputs2.logits

        predictions2 = torch.argmax(logits2, dim=1).tolist()

        file_name = 'user2_predictions.csv'
        file_path = os.path.join(base_path, file_name)

        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Author', 'Book', 'Rate'])

            for i in range(len(predictions2)):
                writer.writerow([book_authors2[i], book_titles2[i], predictions2[i]+1])
        
        GoodReadsReviewsScrapper.delete_file(test_file1)
        GoodReadsReviewsScrapper.delete_file(test_file2)


