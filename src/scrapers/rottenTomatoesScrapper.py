from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd
import time


URL = "https://www.rottentomatoes.com/browse/movies_at_home/"


def click_load_more(driver):
    try:
        load_more_button = driver.find_element(By.CSS_SELECTOR, value="#main-page-content > div > div.discovery__actions > button")
        print("clicking load more")
        load_more_button.click()
        return True
    except Exception as e:
        print("No more 'Load More' button found or error occurred:", e)
        return False


def load_pages(driver, pages):
    for counter in range(1, pages):
        try:
            click_load_more(driver)
            print("waiting " + str(counter * 5) + "s")
            time.sleep(counter * 5)
        except Exception as e:
            print("Error occurred:", e)
            break


def get_movies_info(driver):

    movies_info = []
    soup = BeautifulSoup(driver.page_source, "html.parser")

    for item in soup.find_all('a', {'data-qa':'discovery-media-list-item-caption'}):
        critics_score = item.find('rt-text', {'slot':'criticsScore'})
        critics_score_text = critics_score.text.strip() if critics_score else None

        users_score = item.find('rt-text', {'slot':'audienceScore'})
        users_score_text = users_score.text.strip() if users_score else None

        title = item.find('span', {'data-qa':'discovery-media-list-item-title'})
        title_text = title.text.strip() if title else None

        movies_info.append({
            'title': title_text,
            'critics_score': critics_score_text,
            'users_score': users_score_text,
        })

    return movies_info



if __name__ == "__main__":
    driver = webdriver.Chrome()
    driver.get(URL)

    deny_cookies = driver.find_element(By.CSS_SELECTOR, value="#onetrust-reject-all-handler")
    deny_cookies.click()
    time.sleep(2)

    load_pages(driver, 30)

    movies_info = get_movies_info(driver)

    df = pd.DataFrame(movies_info)

    output_file = "rotten_tomatoes_data_raw.csv"
    df.to_csv("../data/" + output_file, index=False)

    driver.quit()

