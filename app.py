from gensim.models.keyedvectors import KeyedVectors
import streamlit as st
# from prediction import get_similar_words, find_songs_with_keyword, recommend_songs, prompt_to_keywords
from time import time

# start = time()
print("Model yukleniyor...")
# The 'limit' argument is vital, when not used, RAM goes boom
model = KeyedVectors.load_word2vec_format('cc.tr.300.vec', binary=False, limit=100000)
# print(f'Model yuklenme suresi: {time() - start}')

# start = time()
print("Veri on isleme...")
exec(open('/home/bugra/PycharmProjects/sarkiOnerme/versiyon3/data_preprocessing.py').read())

print('predict import...')
exec(open('/home/bugra/PycharmProjects/sarkiOnerme/versiyon3/prediction.py').read())
# print(f'Veri on isleme suresi: {time() - start}')

# sayfa duzenlemeleri
st.set_page_config(layout="centered", page_title="Şarkı öneri", page_icon="🎵")

# baslik
st.title("✮🎧🎸✮:rainbow[Şarkı öneri sistemi]✮📀🎵✮")

# ikili sayfa duzeni
main_tab, recommendation_tab = st.tabs(["Ana Sayfa", "Öneri Sistemi"])

# Ana Sayfa
main_tab.header("Hoşgeldiniz!")

main_tab.write("Bize ruh halinizi anlatın size şarkı önerelim.")

main_tab.write("Lütfen aşağıda belirtilen alana yazınız.")

input = main_tab.text_input("Metin giriniz:")
keywords = prompt_to_keywords(input, df)

if main_tab.button("Şarkı Öner"):
    tahminler = recommend_songs(keywords)
    col1, col2, col3, col4, col5 = recommendation_tab.columns(5, gap="small")
    columns = [col1, col2, col3, col4, col5]

    for i, song in enumerate(tahminler):
        columns[i % 5].write(song)