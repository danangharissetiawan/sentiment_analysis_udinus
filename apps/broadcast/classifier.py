import numpy as np
import tensorflow as tf
from keras_preprocessing.sequence import pad_sequences

import pickle

model = tf.keras.models.load_model('D:/Dev/Learning/sentiment_analysis_udinus/models/modelupsample_ep_10.h5')

with open('D:/Dev/Learning/sentiment_analysis_udinus/models/tokenizerupsample_ep_10.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


def predict_sentiment(text):
    sequence = tokenizer.texts_to_sequences([text])
    data = pad_sequences(sequence, maxlen=200)
    pred = model.predict(data)

    if np.argmax(pred) == 0:
        return 'Neutral'
    elif np.argmax(pred) == 1:
        return 'Negative'
    else:
        return 'Positive'
