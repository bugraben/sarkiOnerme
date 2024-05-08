import streamlit as st
from prediction import get_similar_words, recommend_songs, prompt_to_keywords, load_model, get_youtube_link
from data_preprocessing import preprocess
from time import time

st.set_page_config(layout="centered", page_title="Şarkı öneri", page_icon="🎵")

start = time()
model = load_model(limit=90000)
try:
    print(f'Model yuklenme suresi: {time() - start:.2f}')
except OSError:
    print('OSError')

df = preprocess(max_df=0.005, min_df=5)
print('bitti')
# exec(open('/home/bugra/PycharmProjects/sarkiOnerme/versiyon3/data_preprocessing.py').read())


# baslik
st.title("✮🎧🎸✮:rainbow[Şarkı öneri sistemi]✮📀🎵✮")

# ikili sayfa duzeni
main_tab, credits_tab, pathway_tab = st.tabs(["Ana Sayfa", "Künye", 'Yol Haritası'])

with main_tab:
    # Ana Sayfa
    main_tab.header("Hoşgeldin!")

    main_tab.write("Bana başından geçeni anlat. Sana şarkı önereyim.")

    input = main_tab.text_input("Uzun uzun anlat ama")

    with open('./prompts_list.txt', mode='a') as file:
        file.write(input + '\n\n')

    if main_tab.button("Şarkı Öner"):

        tab_topfive, tab_hybrid, tab_pop, tab_match, tab_keywords = main_tab.tabs(['Ilk 5 Oneri',
                                                                                   'Hibrit Sıralama',
                                                                                   'Popularite',
                                                                                   'Eslesme',
                                                                                   'Anahtar Kelimeler'])


        keywords = prompt_to_keywords(input, df, model)
        tab_keywords.write(keywords)
        top_n_views = recommend_songs(keywords, df, sort_by='views', top_n=40)
        top_n_score = recommend_songs(keywords, df, sort_by='score', top_n=40)
        top_n_hybrid = recommend_songs(keywords, df, sort_by='hybrid', top_n=40)



        next_song = 0
        for n in range((next_song), (next_song+5)):
            cont_song = tab_topfive.container(border=True)
            song_info = top_n_hybrid.reset_index().loc[n, ['title', 'song_artist', 'year']].values
            list_song_info = [f'{song_info[0]} - {song_info[1]}({song_info[2]})', get_youtube_link(song_info[0], song_info[1])]
            for i, col in enumerate(cont_song.columns(2)):
                col.write(list_song_info[i])




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

with pathway_tab:
    '''
    "Daha fazla öner" butonu.
    
    Künye eklenecek.
    '''