import numpy as np
# import tensorflow as tf
from keras.models import load_model
from keras_preprocessing.sequence import pad_sequences
from django.conf import settings
import pickle


model = load_model(settings.MODEL)
# with open(settings.MODEL, 'rb') as handle:
#     model = pickle.load(handle)

with open(settings.TOKENIZER, 'rb') as handle:
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
