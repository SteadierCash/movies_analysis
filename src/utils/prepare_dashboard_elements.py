import sys
sys.path.append('src')

import pandas as pd

def prepare_studio_dropdown(df, measure):
    local_df = explode_df(df)

    studios_count = local_df['studio_split'].value_counts()

    if measure == "Count":
        studios_count = studios_count.reset_index(drop=False)
        studios_count.columns = ['Studio', 'Count']
        return studios_count

    elif "Box" in measure:

        by_what = measure.replace(" ", "").strip()
        by_what = by_what[0].lower() + by_what[1:]

        studio_box_office = local_df.groupby('studio_split')[by_what].sum().reset_index()
        top_studios = studio_box_office.sort_values(by=by_what, ascending=False)

        top_studios = pd.merge(top_studios, studios_count, on='studio_split', how='left')

        top_studios = top_studios[["studio_split", by_what, "count"]]

    else:
        by_what = measure.replace("Average", "").replace(" ", "").replace("Rating", "Note").strip()
        by_what = by_what[0].lower() + by_what[1:]

        studio_box_office = local_df.groupby('studio_split')[by_what].mean().reset_index()
        top_studios = studio_box_office.sort_values(by=by_what, ascending=False)

        top_studios = pd.merge(top_studios, studios_count, on='studio_split', how='left')

        top_studios = top_studios[["studio_split", by_what, "count"]]

        top_studios = top_studios[top_studios["count"] >= 10]

    top_studios.columns = ['Studio', measure, 'Count']

    return top_studios.reset_index(drop=True)

def measures_for_studios(df, measure, studio):

    column_names = ['Title', 'Original Title', 'Premiere', 'Duration', "Box Office World", "Box Office USA",
                              "Box Office Rest Of The World", 'Budget', 'Studio',
           'Critics Note', 'Critics Notes Number', 'Users Note', 'Users Notes Number',
           'Production Country', 'Director', 'Scenario', 'MainActor1', 'MainActor2',
           'MainActor3', 'MainActor4', 'MainActor5', 'MainActor6', 'MainActor7',
           'MainActor8', 'MainActor9']



    if studio != "ALL":
        local_df = explode_df(df)

        local_df = local_df[local_df['studio_split'] == studio]

    else:
        local_df = df.copy()

    local_df['duration'] = local_df['duration'].apply(convert_to_minutes)

    by_what = measure.replace(" ", "").replace("Rating", "Note").strip()
    by_what = by_what[0].lower() + by_what[1:]

    top_movies = local_df.sort_values(by=by_what, ascending=False)

    if studio != "ALL":
        top_movies = top_movies.drop("studio_split", axis=1)

    top_movies = top_movies.drop("premiereYear", axis=1)

    top_movies.columns = column_names

    return top_movies.reset_index(drop=True)

def convert_to_minutes(duration):
    import re
    match = re.match(r'(?:(\d+)h)?\s?(?:(\d+)m)?', duration)
    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    return hours * 60 + minutes

def explode_df(df):
    df_local = df.copy()
    df_local['studio'] = df_local['studio'].str.replace(
        r'(więcej|\(przedstawia\)|\(produkcja\)|\(współudział\)|\(koprodukcja\)|\(niewymienione w czołówce\)|\(udział\)|\(wsparcie\)|\(postprodukcja\)|\(produkcja wykonawcza\))',
        '', regex=True)
    df_local['studio_split'] = df_local['studio'].str.split(' / ')

    df_local_exploded = df_local.explode('studio_split').reset_index(drop=True)
    df_local_exploded['studio_split'] = df_local_exploded['studio_split'].str.strip()
    df_local_exploded = df_local_exploded[df_local_exploded["studio_split"] != ""]

    return df_local_exploded

def prepare_ratings_table(df):
    ratings = df[["title_x", "criticsNote", "usersNote", "averageRating", "critics_score", "users_score"]]
    ratings["critics_score"] = ratings["critics_score"].astype(str).replace("%", "", regex=True).astype(float) / 10
    ratings["users_score"] = ratings["users_score"].astype(str).replace("%", "", regex=True).astype(float) / 10

    ratings.columns = ["Title", "filmweb_critics", "filmweb_users", "imdb", "rotten_tomatoes_critic",
                       "rotten_tomatoes_users"]

    return ratings.drop_duplicates(inplace=False)


def get_studios(df):
    df_local = explode_df(df)
    df_local = df_local['studio_split'].value_counts().reset_index()
    df_local = df_local.sort_values(by="count", ascending=False)
    return df_local['studio_split'].tolist()