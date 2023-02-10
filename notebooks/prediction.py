import numpy as np
import tensorflow as tf
from keras_preprocessing.sequence import pad_sequences

model = tf.keras.models.load_model('D:/Dev/Learning/sentiment_analysis_udinus/models/modelupsample_ep_10.h5')

# load model and tokenizerm
import pickle

# with open('D:/Dev/Learning/sentiment_analysis_udinus/models/modelupsample_ep_10.pickle', 'rb') as f:
#     model = pickle.load(f)


with open('D:/Dev/Learning/sentiment_analysis_udinus/models/tokenizerupsample_ep_10.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

#%%
# predict sentiment using real data
# inputs = ['saya gagal menjadi mahasiswa udinus']
# sequence = tokenizer.texts_to_sequences(inputs)
# data = pad_sequences(sequence, maxlen=200)
# pred = model.predict(data)
#
# if np.argmax(pred) == 0:
#     print('Negative')
# elif np.argmax(pred) == 1:
#     print('Neutral')
# else:
#     print('Positive')


#%%

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

#%%

# predict sentiment using real data
inputs = ['saya benci udinus']

pred = predict_sentiment(inputs[0])
print(pred)



#%%