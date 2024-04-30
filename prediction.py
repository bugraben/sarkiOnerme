import streamlit as st
from gensim.models.keyedvectors import KeyedVectors
from youtube_search import YoutubeSearch
import re

@st.cache_resource
def load_model(limit):
    '''
    :param limit:

    The 'limit' argument is vital, when not used, RAM goes boom
    cc.tr.300.vec model has 2.000.000 entires.
    '''

    print("Model yukleniyor...")
    model = KeyedVectors.load_word2vec_format('cc.tr.300.vec', binary=False, limit=limit)
    print('Model yuklendi.')
    return model

def get_similar_words(word, model, top_n=10):
    print('get_similar_words()')
    try:
        similar_words = model.most_similar(word, topn=top_n)
    except KeyError:
        return []
    return similar_words


def get_youtube_link(artist, song_name):
    # YouTube'da arama yapın
    results = YoutubeSearch(artist + " " + song_name, max_results=1).to_dict()

    # İlk sonucun bağlantısını alın
    if results:
        youtube_link = "https://www.youtube.com/watch?v=" + results[0]['id']
    else:
        youtube_link = None

    return youtube_link


def find_songs_with_keyword(keyword, df):
    print('find_songs_with_keyword()')
    matching_songs = []
    song_dict = df.to_dict(orient='records')

    for song in song_dict:
        if keyword in song["lyrics"]:
            matching_songs.append(song["song_info"])

    return matching_songs


def songs_with_yt_links(songs):
    songs_with_youtube_links = []
    for song_info in songs:
        artist, song_name = song_info.split('>>')
        youtube_link = get_youtube_link(artist, song_name)
        if youtube_link:
            songs_with_youtube_links.append(song_info + ' - ' + youtube_link)

    return songs_with_youtube_links


def recommend_songs_BUGRA(keywords, count_vector_matrix, top_n=5):
    # keywords = ['yorulduk', 'kendim']
    # count_vector_matrix = final_df
    print('recommend_songs_BUGRA()')
    cols = ['title', 'song_artist', 'views']
    cols.extend(keywords)
    temp_df = count_vector_matrix.loc[:, cols]
    temp_df.loc[:, 'score'] = temp_df.loc[:, keywords].T.astype(int).sum()
    top_n = temp_df[['title', 'song_artist', 'score', 'views']]\
                .sort_values('score', ascending=False)\
                .iloc[:top_n, :]\
                .sort_values('views', ascending=False)
    return top_n


def prompt_to_keywords(prompt: str, count_vector_matrix, model):
    print('prompt_to_keywords()')
    keywords = []
    prompt_as_list = re.sub(r'\W', ' ', prompt).split()
    for token in prompt_as_list:
        similar_words = get_similar_words(token, model)
        similar_words.append([token, 1])
        keywords.extend(similar_words)

    keywords_filtered = []
    for keyword, similarity in keywords:
        if keyword in count_vector_matrix.columns:
            keywords_filtered.append(keyword)
    st.write(keywords_filtered)
    return keywords_filtered




# def recommend_songs(keywords, model, df, top_n=5):
#     print('recommend_songs()')
#
#     recommended_songs = []
#
#     for keyword in keywords:
#         similar_words = get_similar_words(keyword, model)
#         similar_words.append([keyword, 1])
#
#
#         for word, similarity in similar_words:
#             relevant_songs = find_songs_with_keyword(word, df)
#             recommended_songs.extend(relevant_songs)
#
#     unique_recommended_songs = list(set(recommended_songs))
#     top_recommended_songs = unique_recommended_songs[:top_n]
#
#     songs_with_youtube_links = []
#     for song_info in top_recommended_songs:
#         artist, song_name = song_info.split('>>')
#         youtube_link = get_youtube_link(artist, song_name)
#         if youtube_link:
#             songs_with_youtube_links.append(song_info + ' - ' + youtube_link)
#
#     return songs_with_youtube_links

