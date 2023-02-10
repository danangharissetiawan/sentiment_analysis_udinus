# Import library yang dibutuhkan
import re, string, unicodedata  # modul regular expression

import nltk
from nltk import word_tokenize, sent_tokenize  # Paket ini membagi teks input menjadi kata-kata.,
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

# %%
# reading dataset
df = pd.read_csv("data/datasets.csv")

# add id column in first column for each row
df.insert(0, "id", range(0, len(df)))

# set id column as index
df = df.set_index("id")

# %%

df.describe()


# %%
# text preprocessing

# case folding
def case_folding(text):
    text = str(text).lower()
    # remove url
    text = re.sub(r"http\S+", "", text)
    # remove username
    text = re.sub(r"@\S+", "", text)
    # remove hashtag
    text = re.sub(r"#\S+", "", text)
    # remove number
    text = re.sub(r"\d+", "", text)
    # remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))
    # remove whitespace leading & trailing
    text = text.strip()
    # remove character
    text = re.sub(r"[^a-zA-Z0-9]+", " ", text)
    # remove double word (ex: yaaaay -> yay)
    text = re.sub(r"(\w)\1{2,}", r"\1", text)
    # remove whitespace double
    text = re.sub(r"\s+", " ", text)
    # remove
    return text


raw_sample = " ".join(df["text"][0:10].tolist())
case_folding(raw_sample)


# %%

# slang word normalization

def slang_word_normalization(text):
    normal_words = pd.read_csv("data/key_norm.csv")
    normal_words = normal_words.set_index("singkat").to_dict()["hasil"]
    text = text.split()
    for i, word in enumerate(text):
        if word in normal_words:
            text[i] = normal_words[word]
            # print(word, " -> ", normal_words[word])
    return " ".join(text)


slang_word_normalization(case_folding(raw_sample))


# %%

# tokenizing

def tokenizing(text):
    return word_tokenize(text)


tokenizing(case_folding(raw_sample))


# %%

# filtering stopwords

def filtering_stopwords(text):
    stop_words = set(stopwords.words("indonesian"))
    stop_words_eng = set(stopwords.words("english"))
    stop_words.update(stop_words_eng)
    # more stopwords with another txt file
    with open("data/stopwords.txt", "r") as f:
        more_stopwords = f.read().splitlines()
    stop_words.update(more_stopwords)
    word_tokens = word_tokenize(text)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    return " ".join(filtered_sentence)


filtering_stopwords(case_folding(raw_sample))

# %%

# stemming
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()


def stemming(text):
    return stemmer.stem(text)


stemming(case_folding(raw_sample))


# %%

# text preprocessing
def text_preprocessing(text):
    text = case_folding(text)
    text = slang_word_normalization(text)
    text = filtering_stopwords(text)
    text = stemming(text)
    return text


# %%

import swifter

# apply text preprocessing
df["text_clean"] = df["text"].swifter.apply(text_preprocessing)
df.head()

# %%
# save to csv
df.to_csv("data/datasets_clean.csv", index=False)

# %%

# fetch sentiment
# from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#
#
# # with sia
# def fetch_sentiment_using_SIA(text):
#     analyzer = SentimentIntensityAnalyzer()
#     vs = analyzer.polarity_scores(text)
#     return 'pos' if vs['compound'] >= 0.05 else 'neg' if vs['compound'] <= -0.05 else 'neu'
#
#
# # with textblob
# from textblob import TextBlob
#
#
# def fetch_sentiment_using_textblob(text):
#     analysis = TextBlob(text)
#     return 'pos' if analysis.sentiment.polarity >= 0.05 else 'neg' if analysis.sentiment.polarity <= -0.05 else 'neu'
#
#
# def fetch_sentiment_using_textblob2(text):
#     analysis = TextBlob(text)
#     return 'pos' if analysis.sentiment.polarity >= 0 else 'neg'
# %%

# apply sentiment
# sentiment_using_sia = df["text"].swifter.apply(fetch_sentiment_using_SIA)
# pd.DataFrame(sentiment_using_sia.value_counts())

# %%
# apply sentiment
# sentiment_using_textblob = df["text"].swifter.apply(fetch_sentiment_using_textblob)
# pd.DataFrame(sentiment_using_textblob.value_counts())

# %%
# apply sentiment
# sentiment_using_textblob2 = df["text"].swifter.apply(fetch_sentiment_using_textblob2)
# pd.DataFrame(sentiment_using_textblob2.value_counts())

# %%

# save sentiment
# df["sentiment"] = sentiment_using_textblob
# df.to_csv("data/comments_sentiment.csv", index=False)

# %%

# df.value_counts("sentiment")

# %%
# remove row with null value
df = df.dropna()
df = df.reset_index(drop=True)
df.head()


# %%

# df['token'] = [nltk.word_tokenize(i) for i in df['text_clean']]

# %%

# opinion lexicon based sentiment analysis (only positive and negative words)
def opinion_lexicon_based_sentiment_analysis(text):
    positive_words = pd.read_csv("data/positive_words.txt", header=None)
    positive_words = positive_words[0].tolist()
    negative_words = pd.read_csv("data/negative_words.txt", header=None)
    negative_words = negative_words[0].tolist()
    text = text.split()
    positive_count = 0
    negative_count = 0
    for word in text:
        if word in positive_words:
            positive_count += 1
        elif word in negative_words:
            negative_count += 1
    if positive_count > negative_count:
        print(text, " -> ", "pos")
        return "pos"
    elif positive_count < negative_count:
        print(text, " -> ", "neg")
        return "neg"
    else:
        print(text, " -> ", "neu")
        return "neu"


# %%
# apply sentiment
sentiment_using_opinion_lexicon = df["text_clean"].swifter.apply(opinion_lexicon_based_sentiment_analysis)
pd.DataFrame(sentiment_using_opinion_lexicon.value_counts())

# %%
# save sentiment
df["sentiment"] = sentiment_using_opinion_lexicon
df.to_csv("data/dataset_sentiment.csv", index=False)

# %%
