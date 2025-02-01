import streamlit as st
import pandas as pd
from utils.plots import (film_release_by_year_plot, user_critics_notes_plot, films_by_year_month_plot,
                         who_the_most_popular_plot, who_the_most_popular_actor_plot, rating_comparison_plot)

from utils.prepare_dashboard_elements import (prepare_studio_dropdown, get_studios,
                                              measures_for_studios, prepare_ratings_table)


def main():
    st.title("🎬 Movie Data Analysis")

    filmweb = pd.read_csv("data/filmweb_data_raw_ver3.csv")
    actors_data = pd.read_csv("data/actors_data.csv")
    merged_data = pd.read_csv("data/merged_data.csv")

    st.subheader("Dataset Preview")
    st.write(filmweb.head())

    st.subheader("Films Releases by Year")
    film_release_by_year_plt = film_release_by_year_plot(filmweb)
    st.pyplot(film_release_by_year_plt)



    st.subheader("User vs Critics Notes")
    measure_3 = ["Box Office World", "Box Office USA", "Box Office Rest Of The World",
                 "Duration", "Budget"]
    selected_measure_3 = st.selectbox("Select measure", measure_3)


    user_critics_notes_plt = user_critics_notes_plot(filmweb, selected_measure_3)
    st.pyplot(user_critics_notes_plt)



    st.subheader("Release by Month")
    measure_4 = sorted(filmweb["premiereYear"].unique().tolist(), reverse=True)
    selected_measure_4 = st.selectbox("Select Year", ["ALL"] + measure_4)

    films_by_year_month_plt = films_by_year_month_plot(filmweb, selected_measure_4)
    st.pyplot(films_by_year_month_plt)


    st.subheader("Who is the most popular")
    measure_5 = ["Actor", "Director", "Screenwriter"]
    selected_measure_5 = st.selectbox("Select", measure_5)

    if selected_measure_5 == "Actor":
        who_the_most_popular_plt = who_the_most_popular_actor_plot(actors_data)
    else:
        who_the_most_popular_plt = who_the_most_popular_plot(filmweb, selected_measure_5)

    st.pyplot(who_the_most_popular_plt)


    # czy te same filmy sa naqjwyzej oceniane - tabelka i wykres
    st.subheader("Filmweb vs Rotten Tomatoes vs IMDB scores")

    ratings_table = prepare_ratings_table(merged_data)

    rating_comparison_plt = rating_comparison_plot(ratings_table)
    st.pyplot(rating_comparison_plt)
    st.write(ratings_table)


    # Measures For Studio
    st.subheader("Top Studios by Measure")
    if 'studio' in filmweb.columns:
        measure_1 = ["Count", "Box Office World", "Box Office USA", "Box Office Rest Of The World",
                   "Average Critics Rating", "Average Users Rating"]
        selected_measure_1 = st.selectbox("Select measure", measure_1)

        st.write(prepare_studio_dropdown(filmweb, selected_measure_1))
    else:
        st.warning("Column 'studio' not found in dataset")

    # Studios Top Movies
    st.subheader("Studios Top Movies")
    if 'studio' in filmweb.columns:
        measure_2 = ["Box Office World", "Box Office USA", "Box Office Rest Of The World",
                   "Critics Rating", "Users Rating", 'Budget', 'Duration']

        selected_studio= st.selectbox("Select studio", ["ALL"] + get_studios(filmweb))
        selected_measure_2 = st.selectbox("Select measure", measure_2, key="selection_for_studios")

        st.write(measures_for_studios(filmweb, selected_measure_2, selected_studio))

    else:
        st.warning("Column 'studio' not found in dataset")



if __name__ == "__main__":
    main()
