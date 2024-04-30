import pandas as pd
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer

# pd.set_option('display.max_columns', 30)
@st.cache_data
def preprocess(max_df, min_df):
    print("Veri on isleme...")

    df = pd.read_excel('./genius_turkce.xlsx')

    # pd.options.display.max_rows = None
    # pd.options.display.max_columns = 30
    # pd.options.display.width = None
    # pd.options.display.max_rows = None
    # df[(df['tag'] == 'misc') & (df['views'] > 0)].loc[:, ['title', 'artist', 'tag', 'views', 'year']] \
    #     .sort_values('views', ascending=True) \
    #     .head(200)


    bad_entries = (df[(df['title'].str.contains('remix', case=False)) |
                      (df['title'].str.contains('mix', case=False)) |
                      (df['title'].str.contains('türkçe', case=False)) |
                      (df['title'].str.contains('turkish', case=False)) |
                      (df['title'].str.contains('translation', case=False)) |
                      (df['title'].str.contains('bass', case=False)) |
                      (df['title'].str.contains("Kur'an", case=False)) |
                      (df['artist'].str.contains('Said Nursi', case=False)) |
                      (df['artist'].str.contains('Genius Trke eviri', case=False)) |
                      (df['tag'] == 'rap') & (df['views'] < 3000000000)].index)

    df = df.drop(index=bad_entries)
    df = df.reset_index()
    df = df.loc[:, ['title', 'artist', 'lyrics', 'views']]
    df['song_artist'] = df['artist']
    df = df.drop(columns='artist')

    # df.info()
    # df.head()

    # df['title'].isnull().sum()
    df = df.dropna()

    stopwords = ['fakat', 'lakin', 'ancak', 'acaba', 'ama', 'aslında', 'az', 'bazı', 'biri', 'birkaç', 'birşey',
                 'bu', 'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem', 'hep',
                 'hepsi', 'her', 'için', 'ile', 'ise', 'kez', 'ki', 'mı', 'mu', 'mü', 'nasıl', 'ne',
                 'nerde', 'niçin', 'niye', 'sanki', 'şey', 'siz', 'şu', 'tüm', 've', 'veya', 'ya',
                 'yani']

    cvector = TfidfVectorizer(stop_words=stopwords, max_df=max_df, min_df=min_df)

    print('TfidfVectorizer egitiliyor...')
    cvector_matrix = cvector.fit_transform(df['lyrics'].astype(str))
    print('TfidfVectorizer egitildi.')
    # a = 0
    # for i in cvector.get_feature_names_out():
    #     a += 1
    #     print(i)


    # cvector_matrix.shape
    # cvector_matrix.toarray()
    # type(cvector_matrix)

    final_df = pd.DataFrame.sparse.from_spmatrix(cvector_matrix)
    final_df.columns = cvector.get_feature_names_out()
    # final_df.head()
    # final_df.shape
    # final_df.info()
    final_df.loc[:, 'title'] = df.loc[:, 'title']
    final_df.loc[:, 'song_artist'] = df.loc[:, 'song_artist']
    final_df.loc[:, 'views'] = df.loc[:, 'views']
    # final_df = pd.concat([df[['title', 'song_artist']], final_df], axis=1)
    final_df = final_df.reset_index()
    df = final_df.iloc[:-4, :]
    print('--df.info()--')
    final_df.info()
    print('----------')
    return df
    # final_df.to_hdf('./CountVectorMatrix.h5', 'key', 'a')
    # final_df.columns
    # final_df = final_df.drop(columns=['00', '000'])
    # final_df.to_parquet('./CountVectorMatrix.parquet')


    #https://arrow.apache.org/docs/python/parquet.html
    # import pyarrow as pa

    # table = pa.Table.from_pandas(final_df)
