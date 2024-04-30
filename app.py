import streamlit as st
from prediction import get_similar_words, find_songs_with_keyword, recommend_songs_BUGRA, prompt_to_keywords, load_model
from data_preprocessing import preprocess
from time import time

st.set_page_config(layout="centered", page_title="Şarkı öneri", page_icon="🎵")



start = time()
# The 'limit' argument is vital, when not used, RAM goes boom
model = load_model(limit=20000000)
print(f'Model yuklenme suresi: {time() - start:.2f}')

# start = time()
df = preprocess(max_df=0.01, min_df=10)
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
    top_n = recommend_songs_BUGRA(keywords, df, top_n=20)
    st.write(top_n)
    # col1, col2, col3, col4, col5 = recommendation_tab.columns(5, gap="small")
    # columns = [col1, col2, col3, col4, col5]
    # for i, song in enumerate(top_five.loc[:, 'title']):
    #     columns[i % 5].write(song)


    '''
    Ornek promptlar
    
    bugün okula giderken karşılaştım. çok güzel bir kız. onu gördüğümde heyecandan bayılacak gibi oluyorum
    
    yaptıklarım için çok pişmanım, keşke bir kez olsun dinleseydi beni
    
    '''