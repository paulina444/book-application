from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv

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

        with open(user_name+'s_reviews.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user_name+"""'s reviews:"""])
            for review in reviews:
                writer.writerow([review.text])

        driver.quit()
