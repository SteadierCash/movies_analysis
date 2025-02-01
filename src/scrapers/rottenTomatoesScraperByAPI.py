import time
import datetime
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

URL = "https://www.rottentomatoes.com/m/"


def get_movies_info(title):
    title = transform_to_rt_movie_title(title)

    response = requests.get(URL + title)

    if response.status_code == 200:
        soup = BeautifulSoup(requests.get(URL + title).content, "html.parser")

        critics_score = soup.find('rt-text', {'slot': 'criticsScore'})
        critics_score_text = critics_score.text.strip() if critics_score else None

        users_score = soup.find('rt-text', {'slot': 'audienceScore'})
        users_score_text = users_score.text.strip() if users_score else None

        return {
            'title': title,
            'critics_score': critics_score_text,
            'users_score': users_score_text,
        }

def transform_to_rt_movie_title(title):
    title = title.lower()
    title = re.sub(r"[^a-z0-9\s]", "", title)
    title = re.sub(r"\s+", "_", title)
    return title



if __name__ == "__main__":
    filmweb_movies_list = pd.read_csv("../data/filmweb_data_raw_ver3.csv")["originalTitle"].tolist()

    movies_info = []

    counter = 0

    movies_found = 0

    for movie in filmweb_movies_list:
        movie_info = get_movies_info(movie)
        counter += 1

        if movie_info is not None:
            movies_info.append(movie_info)
            movies_found += 1

        if counter % 10 == 0:
            print(datetime.datetime.now(), "All requests:", counter, "movies found:", movies_found)
            time.sleep(3)

    df = pd.DataFrame(movies_info)

    output_file = "rotten_tomatoes_api_data_raw.csv"
    df.to_csv("../data/" + output_file, index=False)

