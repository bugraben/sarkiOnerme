import streamlit as st
from prediction import get_similar_words, find_songs_with_keyword, recommend_songs_BUGRA, prompt_to_keywords, load_model
from data_preprocessing import preprocess
from time import time

st.set_page_config(layout="centered", page_title="Şarkı öneri", page_icon="🎵")

df = None

if df is None:

    # start = time()
    # The 'limit' argument is vital, when not used, RAM goes boom

    model = load_model(limit=1000000)
    # print(f'Model yuklenme suresi: {time() - start}')

    # start = time()
    df = preprocess()
    print('bitti')
    # exec(open('/home/bugra/PycharmProjects/sarkiOnerme/versiyon3/data_preprocessing.py').read())

    # print('predict import...')
    # exec(open('/home/bugra/PycharmProjects/sarkiOnerme/versiyon3/prediction.py').read())
    # print(f'Veri on isleme suresi: {time() - start}')

# sayfa duzenlemeleri

# baslik
st.title("✮🎧🎸✮:rainbow[Şarkı öneri sistemi]✮📀🎵✮")

# ikili sayfa duzeni
main_tab, recommendation_tab = st.tabs(["Ana Sayfa", "Öneri Sistemi"])

# Ana Sayfa
main_tab.header("Hoşgeldiniz!")

main_tab.write("Bize ruh halinizi anlatın size şarkı önerelim.")

main_tab.write("Lütfen aşağıda belirtilen alana yazınız.")

input = main_tab.text_input("Metin giriniz:")

if main_tab.button("Şarkı Öner"):
    keywords = prompt_to_keywords(input, df, model)
    top_five = recommend_songs_BUGRA(keywords, df)
    st.write(top_five.iloc[:, 0])
    # col1, col2, col3, col4, col5 = recommendation_tab.columns(5, gap="small")
    # columns = [col1, col2, col3, col4, col5]
    # for i, song in enumerate(top_five.loc[:, 'title']):
    #     columns[i % 5].write(song)