import streamlit as st
import pickle
import pandas
import requests

def recommend(movie):
    movie_recommended = []
    movie_recommended_poster = []
    movie_index = movies[movies["title"] == movie].index[0]
    distances = sorted(list(enumerate(similarity[movie_index])), reverse=True, key=lambda x: x[1])
    for i in range(1, 6):
        recommend_index = distances[i][0]
        recommend_movie = movies.loc[recommend_index, "title"]
        movie_recommended.append(recommend_movie)
        movie_recommended_poster.append(poster(movies.loc[recommend_index, "movie_id"]))
    return movie_recommended, movie_recommended_poster

def poster(movie_id):
    file = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=339f2ee038fd29f938a051eb4e1a04a0&language=en-US".format(movie_id))
    data = file.json()
    image = "https://image.tmdb.org/t/p/original/" + data["poster_path"]
    return image

movies = pickle.load(open("movies.pkl","rb"))
movies_list = movies["title"].values

similarity = pickle.load(open("similarity.pkl","rb"))
st.title("Movie Recommendation System")

selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies_list)
if st.button("Recommend"):
    names, posters = recommend(selected_movie_name)
    index = 0
    for i in st.columns(5):
        with i:
            st.text(names[index])
            st.image(posters[index])
            index += 1
