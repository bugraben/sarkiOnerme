from youtube_search import YoutubeSearch
import re

def get_similar_words(word, top_n=20):
    similar_words = model.most_similar(word, topn=top_n)
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


def find_songs_with_keyword(keyword):

    matching_songs = []
    song_dict = df.to_dict(orient='records')

    for song in song_dict:
        if keyword in song["lyrics"]:
            matching_songs.append(song["song_info"])

    return matching_songs


def recommend_songs(keywords, top_n=5):

    recommended_songs = []

    for keyword in keywords:
        similar_words = get_similar_words(keyword)
        similar_words.append([keyword, 1])


        for word, similarity in similar_words:
            relevant_songs = find_songs_with_keyword(word)
            recommended_songs.extend(relevant_songs)

    unique_recommended_songs = list(set(recommended_songs))
    top_recommended_songs = unique_recommended_songs[:top_n]

    songs_with_youtube_links = []
    for song_info in top_recommended_songs:
        artist, song_name = song_info.split('>>')
        youtube_link = get_youtube_link(artist, song_name)
        if youtube_link:
            songs_with_youtube_links.append(song_info + ' - ' + youtube_link)

    return songs_with_youtube_links

# get_similar_words('hata')
# find_songs_with_keyword('hatalar')
# recommend_songs(['hata', 'hayat'])

def recommend_songs_BUGRA(keywords, count_vector_matrix):
    # keywords = ['yorulduk', 'kendim']
    # count_vector_matrix = final_df

    cols = ['title', 'song_artist']
    cols.extend(keywords)
    temp_df = count_vector_matrix[cols]
    temp_df.loc[:, 'score'] = temp_df.loc[:, keywords].T.astype(int).sum()
    top_five = temp_df[['title', 'song_artist', 'score']].sort_values('score', ascending=False).iloc[:5, :]

    return top_five


def prompt_to_keywords(prompt: str, count_vector_matrix):
    keywords = []
    prompt_as_list = re.sub(r'\W', ' ', prompt).split()
    for token in prompt_as_list:
        similar_words = get_similar_words(token)
        similar_words.append([token, 1])
        keywords.extend(similar_words)

    keywords_filtered = []
    for keyword, similarity in keywords:
        if keyword in count_vector_matrix.columns:
            keywords_filtered.append(keyword)
    return keywords_filtered

# recommend_songs_BUGRA(['hata'], final_df)

# a = prompt_to_keywords('ben cok yoruldum, duvarlar ustume ustume geliyor', final_df)
# len(a)
#
# recommend_songs_BUGRA(a, final_df)