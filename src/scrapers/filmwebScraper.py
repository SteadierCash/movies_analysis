import requests
from bs4 import BeautifulSoup
import re
import time
from src.logger.defaultLogger import logger
import pandas as pd

URL = "https://www.filmweb.pl/films/search?page="
PREFIX = "https://www.filmweb.pl"

def get_urls_from_page(page_number: int):
    urls = []

    response = requests.get(URL + str(page_number))

    if response.status_code != 200:
        logger.error("Error getting filmweb page: ", page_number, response.text)
        return urls


    soup = BeautifulSoup(response.content, "html.parser")

    films = soup.find_all("a", class_="preview__link")

    for film in films:
        urls.append(PREFIX + film.get("href"))

    return urls

def get_page_info(url: str):
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Error getting page: ", url, response.text)

    soup = BeautifulSoup(response.content, "html.parser")

    title_raw = soup.find("h1", class_="filmCoverSection__title")
    title = title_raw.text if title_raw else None

    original_title_raw = soup.find("div", class_="filmInfo__group filmInfo__group--originalTitle")
    original_title = original_title_raw.find("span", class_="filmInfo__info").text if original_title_raw else None

    duration_raw = soup.find("div", class_="filmCoverSection__titleDetails")
    duration = duration_raw.find("div", class_="filmCoverSection__duration").text if duration_raw else None

    premiere_year_raw = soup.find("div", class_="filmCoverSection__year")

    if not premiere_year_raw:
        premiere_year_raw = soup.find("h2", class_="filmCoverSection__year")

    premiere_year = premiere_year_raw.text if premiere_year_raw else None

    users_notes_raw = soup.find("span", class_="filmRating__rateValue")
    user_notes = users_notes_raw.text if users_notes_raw else None

    users_notes_number_raw = soup.find("span", class_="filmRating__count")
    user_notes_number = users_notes_number_raw.text.strip() if users_notes_number_raw else None

    critics_notes_number_raw = soup.find("div", class_="filmRating filmRating--filmCritic")

    critics_notes_raw = critics_notes_number_raw.find("span", class_="filmRating__rateValue") if critics_notes_number_raw else None
    critics_notes = critics_notes_raw.text if critics_notes_raw else None

    critics_notes_number = critics_notes_number_raw.find("span", class_="filmRating__count").text.strip() if critics_notes_number_raw else None

    director_scenario_raw = soup.find("div", class_="filmPosterSection__info filmInfo")

    director_raw = director_scenario_raw.find('a', {'itemprop': 'director'})
    director = director_raw.text if director_raw else None
    scenario_raw = director_scenario_raw.find('a', {'itemprop': 'creator'})
    scenario = scenario_raw.text if scenario_raw else None

    production_country_raw = soup.find("span", class_="filmInfo__info filmInfo__info--productionCountry")
    production_country = production_country_raw.text.strip() if production_country_raw else None

    actors = []
    actors_container = soup.find("div", class_="Crs crs crs--limited crs--roundedNavigation")
    actors_raw = actors_container.find_all("div", class_="crs__item") if actors_container else None

    if actors_raw:
        for actor in actors_raw:
            actors.append(actor.find("a", class_="simplePoster__title").text.strip())
    else:
        actors = None

    film_info = soup.find("div", class_="filmOtherInfoSection__group")
    premiere_raw_list = film_info.find_all("span", class_="block") if film_info else None
    premiere = None
    for premiere_raw in premiere_raw_list:
        p = premiere_raw.text.replace(",", " ")
        if "(Światowa)" in p:
            premiere = p.replace("(Światowa)", "").strip()
            break

    boxOfficeWorld = None
    boxOfficeUSA = None
    boxOfficeRestOfTheWorld = None
    budget = None
    boxOffice_raw = soup.find("div", class_="filmInfo__group filmInfo__group--filmBoxOffice")
    elements = boxOffice_raw.find_all("span", class_="filmInfo__info") if boxOffice_raw else None
    if elements:
        for element in elements:
            element_text = element.text

            if "na świecie" in element_text:

                for boxOffice in element_text.split("$"):
                    if "świecie" in boxOffice:
                        boxOfficeWorld = re.sub(r'\D+', '', boxOffice)
                    elif "w USA" in boxOffice:
                        boxOfficeUSA= re.sub(r'\D+', '', boxOffice)
                    elif "poza USA" in boxOffice:
                        boxOfficeRestOfTheWorld = re.sub(r'\D+', '', boxOffice)

            elif "USA" in element_text:
                boxOfficeUSA = element_text.replace(",", "").replace("$", "").replace(" ", "").replace("wUSA", "").strip()

            else:
                budget = element_text.replace(",", "").replace("$", "").replace(" ", "").strip()

    studios_raw_element = soup.find("div", class_="filmInfo__group filmInfo__group--studios")
    studios_raw = studios_raw_element.find("span", class_="filmInfo__info") if studios_raw_element else None
    studios = studios_raw.text.strip() if studios_raw else None

    return {
        "title": title,
        "originalTitle": original_title,
        "premiere": premiere,
        "premiereYear": premiere_year,
        "duration": duration,
        "boxOfficeWorld": boxOfficeWorld,
        "boxOfficeUSA": boxOfficeUSA,
        "boxOfficeRestOfTheWorld": boxOfficeRestOfTheWorld,
        "budget": budget,
        "studio": studios,
        "criticsNote": critics_notes.replace(",", ".") if critics_notes else None,
        "criticsNotesNumber": critics_notes_number,
        "usersNote": user_notes.replace(",", ".") if user_notes else None,
        "usersNotesNumber": user_notes_number,
        "productionCountry": production_country,
        "director": director,
        "scenario": scenario,
        "mainActor1": actors[0] if len(actors) > 0 else None,
        "mainActor2": actors[1] if len(actors) > 1 else None,
        "mainActor3": actors[2] if len(actors) > 2 else None,
        "mainActor4": actors[3] if len(actors) > 3 else None,
        "mainActor5": actors[4] if len(actors) > 4 else None,
        "mainActor6": actors[5] if len(actors) > 5 else None,
        "mainActor7": actors[6] if len(actors) > 6 else None,
        "mainActor8": actors[7] if len(actors) > 7 else None,
        "mainActor9": actors[8] if len(actors) > 8 else None,
    }



if __name__ == "__main__":
    result = []

    for i in range(1, 1001):
        logger.info(f"Getting data from page: {i}")
        page_urls = get_urls_from_page(i)

        for url in page_urls:
            try:
                info = get_page_info(url)
            except Exception as e:
                logger.error(f"Failed to get information: {e} for {url}")
            else:
                result.append(info)
        time.sleep(3)

    df = pd.DataFrame(result)

    output_file = "filmweb_data_raw_ver3.csv"
    df.to_csv("../data/" + output_file, index=False)

    logger.info(f"Data saved to {output_file}")
