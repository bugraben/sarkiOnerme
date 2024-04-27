import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

pd.set_option('display.max_columns', 30)

df_ = pd.read_excel('./genius_turkce.xlsx')
df = df_.copy()

df = df[['title', 'artist', 'lyrics']]
df['song_artist'] = df['artist']
df = df.drop(columns='artist')

bad_entries = df[(df['title'].str.contains('remix', case=False) == 1) |
   (df['title'].str.contains('türkçe', case=False) == 1) |
   (df['title'].str.contains('bass', case=False) == 1)].index

df = df.drop(index=bad_entries)
df = df.reset_index()

# df.info()
# df.head()

# df['title'].isnull().sum()
df = df.dropna()

stopwords = ['fakat', 'lakin', 'ancak', 'acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey',
             'biz', 'bu', 'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem', 'hep',
             'hepsi', 'her', 'hiç', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'mı', 'mu', 'mü', 'nasıl', 'ne', 'neden',
             'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz', 'şu', 'tüm', 've', 'veya', 'ya',
             'yani']

cvector = CountVectorizer(stop_words=stopwords, max_df=0.05, min_df=10)

cvector_matrix = cvector.fit_transform(df['lyrics'].astype(str))
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
final_df['title'] = df['title']
final_df['song_artist'] = df['song_artist']
final_df = pd.concat([df[['title', 'song_artist']], final_df], axis=1)
final_df.info()
final_df = final_df.reset_index()
df = final_df.iloc[:40631, :]

# final_df.to_hdf('./CountVectorMatrix.h5', 'key', 'a')
# final_df.columns
# final_df = final_df.drop(columns=['00', '000'])
# final_df.to_parquet('./CountVectorMatrix.parquet')


#https://arrow.apache.org/docs/python/parquet.html
# import pyarrow as pa

# table = pa.Table.from_pandas(final_df)
