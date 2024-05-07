import streamlit as st
from prediction import get_similar_words, find_songs_with_keyword, recommend_songs, prompt_to_keywords, load_model
from data_preprocessing import preprocess
from time import time

st.set_page_config(layout="centered", page_title="Şarkı öneri", page_icon="🎵")

start = time()
# The 'limit' argument is vital, when not used, RAM goes boom
model = load_model(limit=90000)
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
main_tab, credits_tab = st.tabs(["Ana Sayfa", "Künye"])

# Ana Sayfa
main_tab.header("Hoşgeldin!")

main_tab.write("Bana başından geçeni anlat. Sana şarkı önereyim.")

input = main_tab.text_input("Uzun uzun anlat ama")

with open('./prompts_list.txt', mode='a') as file:
    file.write(input + '\n\n')

if main_tab.button("Şarkı Öner"):

    tab_hybrid, tab_pop, tab_match, tab_keywords = main_tab.tabs(['Hibrit Sıralama',
                                                                  'Popularite',
                                                                  'Eslesme',
                                                                  'Anahtar Kelimeler'])
    keywords = prompt_to_keywords(input, df, model)
    tab_keywords.write(keywords)
    top_n_views = recommend_songs(keywords, df, sort_by='views', top_n=40)
    top_n_score = recommend_songs(keywords, df, sort_by='score', top_n=40)
    top_n_hybrid = recommend_songs(keywords, df, sort_by='hybrid', top_n=40)
    tab_pop.write(top_n_views)
    tab_match.write(top_n_score)
    tab_hybrid.write(top_n_hybrid)
    # columns = [col1, col2, col3, col4, col5]
    # for i, song in enumerate(top_five.loc[:, 'title']):
    #     columns[i % 5].write(song)

'''
Örnek Metinler:

eski sinemada bir filme girsek seninle. geçmişimizden, çocukluktan konuşsak. özlediğimiz her şey, gözlerimize dolan her anı...

5 sene önce güzel bir kızı ay ışığı altında deniz kenarında öptüm. O günü özlüyorum 

Yıllardır yorgunum, ne dost kaldı ne yâr kaldı. Tek başıma savaştım çok şey başardım

içimde bir şeyler ölüyor sanki. yalnızlık dört yandan kuşatıyor içimi. sanırım sonuna geliyoruz.

İNANILMAZ GÜZEL BİR KIZLA TANIŞTIM. kantinde geldi yanıma, durup dururken geliverdi. tanışmak istiyormuş benimle. tabii dedim tanışalım. çok başka bir hali çok başka bir havası var. o anlattıkça ben daha derinlere düştüm. kayboldum.

'''
