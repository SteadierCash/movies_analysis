import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import pandas as pd
import re

def film_release_by_year_plot(df):
    plt.figure(figsize=(12, 8))

    film_sorted = df.sort_values(by='premiereYear')
    sns.countplot(data=film_sorted, x='premiereYear', color='skyblue')


    plt.xlabel('Year of Release', fontsize=14)
    plt.ylabel('Number of Movies Released', fontsize=14)
    xticks = plt.gca().get_xticks()
    xticks = [int(tick) for tick in xticks]
    interval = 5
    xticks_filtered = xticks[::interval]
    plt.xticks(xticks_filtered, rotation=45, fontsize=12)

    plt.tight_layout()

    return plt

def films_by_year_month_plot(df, year):
    plt.figure(figsize=(12, 6))

    df_year = df.dropna(subset=['premiere'])

    df_year = df_year[
        (df_year['premiere'] != "") & (~df_year['premiere'].isnull())]

    if year != "ALL":
        df_year = df_year[df_year['premiereYear'] == year]

    df_year['month'] = df_year['premiere'].astype(str).apply(lambda x: re.sub(r"\d+", "", x).strip())

    df_year = df_year[df_year['month'] != ""]

    df_year['month'].value_counts().sort_index().plot(kind='bar', color='green')
    plt.title('Distribution of Movie Releases by Month')
    plt.xlabel('Month')
    plt.ylabel('Number of Movies')
    plt.xticks(ticks=range(0, 12),
               labels=['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], rotation=45)

    return plt



def user_critics_notes_plot(df, measure):
    by_what = measure.replace(" ", "").strip()
    by_what = by_what[0].lower() + by_what[1:]

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    sns.scatterplot(x=df[by_what], y=df['criticsNote'], color='red', ax=axes[0])
    axes[0].set_title(measure + ' vs Critics Ratings')
    axes[0].set_xlabel(measure)
    axes[0].set_ylabel('Critics Ratings')

    sns.scatterplot(x=df[by_what], y=df['usersNote'], color='orange', ax=axes[1])
    axes[1].set_title(measure + ' vs Users Ratings')
    axes[1].set_xlabel(measure)
    axes[1].set_ylabel('Users Ratings')

    plt.tight_layout()

    return plt

def who_the_most_popular_actor_plot(df):

    short_df = df.head(10)

    plt.figure(figsize=(10, 6))
    plt.barh(short_df['actor'], short_df['count'], color='skyblue')

    for index, value in enumerate(short_df['count']):
        plt.text(value + 1, index, str(value), va='center', fontsize=12)

    plt.title('Most Films by Actor', fontsize=16)
    plt.xlabel('Number of Movies', fontsize=12)
    plt.ylabel('Actor', fontsize=12)

    plt.tight_layout()

    return plt


def who_the_most_popular_plot(df, measure):

    if measure == "Director":
        by_what = "director"
    else:
        by_what = "scenario"

    top = df[by_what].value_counts().reset_index(drop=False)

    top_sorted = top.sort_values(by='count', ascending=False).head(10)

    plt.figure(figsize=(10, 6))
    plt.barh(top_sorted[by_what], top_sorted['count'], color='skyblue')

    for index, value in enumerate(top_sorted['count']):
        plt.text(value + 1, index, str(value), va='center', fontsize=12)

    plt.title('Most Films by ' + measure, fontsize=16)
    plt.xlabel('Number of Movies', fontsize=12)
    plt.ylabel(measure, fontsize=12)

    plt.tight_layout()

    return plt

def rating_comparison_plot(df):
    local_df = df.head(10)

    local_df.set_index('Title', inplace=True)

    colors = sns.color_palette("Set2", len(local_df.columns))

    ax = local_df.plot(kind='barh', figsize=(10, 6), width=0.8, color=colors)

    plt.title('Movie Ratings by Source', fontsize=16)
    plt.xlabel('Rating', fontsize=12)
    plt.ylabel('Movie Title', fontsize=12)

    plt.xticks(rotation=0)

    plt.legend(loc='upper left', bbox_to_anchor=(1, 1), title='Rating Sources')

    plt.tight_layout()

    return plt

if __name__ == '__main__':
    filmweb = pd.read_csv("../data/filmweb_data_raw_ver3.csv")
    df_long = filmweb.melt(id_vars=['title'],
                      value_vars=['mainActor1', 'mainActor2', 'mainActor3', 'mainActor4', 'mainActor5',
                                  'mainActor6', 'mainActor7', 'mainActor8', 'mainActor9'], var_name='actor_column',
                      value_name='actor')

    top_actors = df_long['actor'].value_counts().reset_index(drop=False)

    top_actors_sorted = top_actors.sort_values(by='count', ascending=False).head(100)

    top_actors_sorted.to_csv("../data/actors_data.csv")

