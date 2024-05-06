import streamlit as st
from prediction import get_similar_words, find_songs_with_keyword, recommend_songs_BUGRA, prompt_to_keywords, load_model
from data_preprocessing import preprocess
from time import time

st.set_page_config(layout="centered", page_title="Şarkı öneri", page_icon="🎵")

'''
Ornek promptlar

bugün okula giderken karşılaştım. çok güzel bir kız. onu gördüğümde heyecandan bayılacak gibi oluyorum

yaptıklarım için çok pişmanım, keşke bir kez olsun dinleseydi beni

Bazen durup düşünüyorum: gerek var mıydı bunca tantanaya. Neden oturup konuşamıyoruz biz seninle. Neden susup dinlemiyoruz biraz olsun. Birbirimizi çok kırdık. 

İNANILMAZ GÜZEL BİR KIZLA TANIŞTIM. kantinde geldi yanıma, durup dururken geliverdi. tanışmak istiyormuş benimle. tabii dedim tanışalım. çok başka bir hali çok başka bir havası var. o anlattıkça ben daha derinlere düştüm. kayboldum.

ben aşık oldum günlük. galiba bu kez onu buldum. doğru kızı buldum. hatunum.

'''

start = time()
# The 'limit' argument is vital, when not used, RAM goes boom
model = load_model(limit=100000)
print(f'Model yuklenme suresi: {time() - start:.2f}')

# start = time()
df = preprocess(max_df=0.005, min_df=5)
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

with open('/prompts_list.txt', mode='a') as file:
    file.write(input)

if main_tab.button("Şarkı Öner"):
    col1, col2 = main_tab.columns(2, gap="small")
    keywords = prompt_to_keywords(input, df, model)
    top_n_views = recommend_songs_BUGRA(keywords, df, sort_by='views', top_n=40)
    top_n_score = recommend_songs_BUGRA(keywords, df, sort_by='score', top_n=40)
    col1.write(top_n_views)
    col2.write(top_n_score)
    # columns = [col1, col2, col3, col4, col5]
    # for i, song in enumerate(top_five.loc[:, 'title']):
    #     columns[i % 5].write(song)

