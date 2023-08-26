import pickle

import streamlit as st
import requests

API_KEY = '8265bd1679663a7ea12ac168da84d2e8'

hide_streamlit_style = """
            <style>
            body {overflow: hidden;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


def fetch_posters(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = f"https://tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_posters(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


st.header('Movie Recommender System')
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pickle.load(open('movie_list.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox('Type or Select a Movie from the list', movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommend_movie_posters = recommend(selected_movie)
    columns = st.columns(5)

    for i, col in enumerate(columns):
        with col:
            st.text(recommended_movie_names[i])
            st.image(recommend_movie_posters[i])
