from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
import os

class GoodReadsReviewsScrapper:
    @staticmethod
    def scrape_user_reviews(user_id, user_name):

        chrome_options = Options()
        #chrome_options.add_argument("--headless")  # nie wiem czemu to nie działa lol

        service = Service(ChromeDriverManager().install()) # ChromeDriverManager().install() -pobranie wersji sterownika chromedriver dla google chrome # Service przekazanie lokalizacji sterownika do Selenium
        driver = webdriver.Chrome(service=service, options=chrome_options) # uruchomienie instancji przegladarki

        
        user_profile_url = f'https://www.goodreads.com/user/show/{str(user_id)}-{user_name}'
        driver.get(user_profile_url)

        # załadowanie strony
        time.sleep(5)

        # znalezienie recenzji
        reviews = driver.find_elements(By.XPATH, "//span[contains(@id, 'freeTextContainerreview')]") 
        authors = driver.find_elements(By.CSS_SELECTOR, "a.authorName")  
        titles = driver.find_elements(By.CSS_SELECTOR, "a.bookTitle")  


        base_path = 'reviews'
        file_name = user_name+'s_reviews.csv'
        file_path = os.path.join(base_path, file_name)

        with open(file_path, 'w', newline='',encoding = 'utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Book title', "Author", "Review"])
            for i in range(len(reviews)):
                writer.writerow([authors[i].text, titles[i].text, reviews[i].text])

        driver.quit()
