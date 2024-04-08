import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sys import getsizeof

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)
# pd.set_option('display.max_rows', 20)

df_ = pd.read_excel('./genius_turkce.xlsx')
df = df_.copy()

df.describe(percentiles=[.01, .05, .10, .20, .30, .40, .50, .60, .70, .80, .90, .95, .99]).T
df.info()

df[df['views'] < 3]['views'].value_counts()

df = df[~df['views'] < 3]

stopwords = ['fakat','lakin','ancak','acaba', 'ama', 'aslında', 'az', 'bazı', 'belki', 'biri', 'birkaç', 'birşey',
             'biz', 'bu', 'çok', 'çünkü', 'da', 'daha', 'de', 'defa', 'diye', 'eğer', 'en', 'gibi', 'hem', 'hep',
             'hepsi', 'her', 'hiç', 'için', 'ile', 'ise', 'kez', 'ki', 'kim', 'mı', 'mu', 'mü', 'nasıl', 'ne', 'neden',
             'nerde', 'nerede', 'nereye', 'niçin', 'niye', 'o', 'sanki', 'şey', 'siz', 'şu', 'tüm', 've', 'veya', 'ya',
             'yani']


tfidf = TfidfVectorizer(lowercase=True, stop_words=stopwords, max_df=0.05, min_df=10)

tfidf_matrix = tfidf.fit_transform(df['lyrics'].astype(str))


# Tum tokenleri (kelimeleri) ekrana yazdirir. Biraz uzun suren bir islem
for i in tfidf.get_feature_names_out():
    print(i)

# CSR Matrixi numpy arrayine ceviriyor. CSR matrix sckipy kutuphanesinden gelen bir veri tipiymis
tfidf_matrix.toarray()

# Onemli olmayan bir seyler
tfidf_matrix.shape
tfidf.get_feature_names_out().shape
tfidf_matrix.max()
tfidf_features = [i for i in tfidf.get_feature_names_out() if len(i) <= 2]
len(tfidf_features)
dir(tfidf_matrix)
tfidf_matrix.shape

getsizeof(tfidf_fp16)
tfidf_matrix.astype(np.float32).toarray(out=tfidf_fp16)
matrix_np = np.array(tfidf_matrix, dtype=np.float16)
tfidf_matrix.T.value_counts()
print(('hello', 'bye')[1 < 2])

# Farkli esik degerleri icin deneme yaptim
tfidf_2 = TfidfVectorizer(lowercase=True, stop_words=stopwords, max_df=1.0, min_df=0.1)
tfidf_matrix_2 = tfidf_2.fit_transform(df['lyrics'].astype(str))

for i in tfidf_2.get_feature_names_out():
    print(i)

#     öl
#     ölüm
#     ölümsüz
#     ölü
#     ölemem
#     ölmem
#
#
#     vazgeçmek
#
#
#
# (deniz, sarap)