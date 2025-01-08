from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import csv
import os
import re 

#TODO zrobic nowego scrappera ktory bdzie pobieral gwiazdki tam gdzie nie ma zadnej recenzji
class GoodReadsReviewsScrapper:
    @staticmethod
    def scrape_user_reviews(user_id, user_name):
        service = Service(ChromeDriverManager().install()) # ChromeDriverManager().install() -pobranie wersji sterownika chromedriver dla google chrome # Service przekazanie lokalizacji sterownika do Selenium
        driver = webdriver.Chrome(service=service) # uruchomienie instancji przegladarki

        user_profile_url = f'https://www.goodreads.com/review/list/{str(user_id)}-{user_name}?utf8=%E2%9C%93&utf8=%E2%9C%93&shelf=read&title={user_name}&per_page=infinite'
        driver.get(user_profile_url)

        time.sleep(3)

        # przycisk settings
        settings_button = driver.find_element(By.ID, "shelfSettingsLink")
        settings_button.click()
        time.sleep(1)

        # przycisk review
        review_button = driver.find_element(By.ID, "review_field")
        review_button.click()
        time.sleep(1)

        # przyciski more - w celu rozwinięcia opinii
        more_buttons = driver.find_elements(By.XPATH, "//a[contains(text(), '...more')]")
        for button in more_buttons:
            driver.execute_script("arguments[0].click();", button)
            time.sleep(1)

                                                    # opinie bez rozwinięcia                         # pomija opinie, które mają rozwinięcie (none)  # opinie z rozwinięciem                                                                 # przeczytane książki ale bez opini               
        reviews = driver.find_elements(By.XPATH, "//span[starts-with(@id, 'freeTextContainerreview') and not(contains(@style, 'display: none'))] | //span[starts-with(@id, 'freeTextreview') and not(contains(@style, 'display: none'))] | //td[@class='field review']//span[@class='greyText' and text()='None']")
        authors = driver.find_elements(By.XPATH, "//td[@class='field author']//a")
        titles = driver.find_elements(By.XPATH, "//td[@class='field title']//a")
        GoodReadsReviewsScrapper.scrape_user_starts(driver)
        
        # oczyszczenie tytułów z napisów w nawiasach (napis która część książki)
        cleaned_titles = []
        cleaned_titles = GoodReadsReviewsScrapper.clean_titles(titles)

        # oczyszczenie z znaków nowej lini 
        cleaned_reviews = []
        cleaned_reviews = GoodReadsReviewsScrapper.clean_reviews(reviews)

        
        project_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(project_dir)
        base_path = os.path.join(project_dir, 'reviews')
        file_name = user_name + 's_'+ str(user_id) + '_reviews.csv'
        file_path = os.path.join(base_path, file_name)

        with open(file_path, 'w', newline='',encoding = 'utf-8') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Author', "Book title", "Review"])

            # for review in reviews:
            #     print(review.text)
            # for title in titles:
            #     print(title.text)
            # for author in authors:
            #     print(author.text)s

            for i in range(len(reviews)):
                if reviews[i].text != "None":
                    writer.writerow([authors[i].text, cleaned_titles[i], cleaned_reviews[i]])

        driver.quit()
        return file_path

    @staticmethod
    def clean_titles(titles):
        cleaned_titles = []
        for title in titles:
            title_text = title.text
            cleaned_title = re.sub(r"\s*\(.*?\)\s*", "", title_text)
            cleaned_titles.append(cleaned_title)
        return cleaned_titles
    
    @staticmethod
    def clean_reviews(reviews):
        cleaned_reviews = []
        for review in reviews:
            raw_text = review.text
            cleaned_text = raw_text.replace('\n', ' ')
            cleaned_reviews.append(cleaned_text)
        return cleaned_reviews
    
    @staticmethod
    def scrape_user_starts(driver):
        # trzeba jakos skipnac te ktore maja opinie
        star_elements = driver.find_elements(By.CSS_SELECTOR, "span.staticStars.notranslate")
        reviews = driver.find_elements(By.XPATH, "//span[starts-with(@id, 'freeTextContainerreview') and not(contains(@style, 'display: none'))] | //span[starts-with(@id, 'freeTextreview') and not(contains(@style, 'display: none'))]")

        star_dict = {
            "it was amazing" : 5,
            "really liked it" : 4,
            "liked it" : 3,
            "it was ok" : 2,
            "did not like it" : 1
        }

        star_elements_num = []
        for star in star_elements:
            for key, value in star_dict.items():
                if star.text == key:
                    star_elements_num.append(value) 

        print(star_elements_num)





