# Load Libraries
import tensorflow as tf
from tensorflow.keras import regularizers
from tensorflow.keras.layers import Input, Embedding, LSTM, Dense, Dropout, Flatten
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam

from model_evaluator import Evaluator
from model_preprocessor import Preprocessor

# LSTM Model
def lstm(max_len=80, emb_dim=32, max_vocab_len=128, W_reg=regularizers.l2(1e-4)):
    """LSTM with Attention model with the Keras Sequential model"""

    input = Input(shape=(max_len,), dtype='int32', name='lstm_input')

    emb = Embedding(input_dim=max_vocab_len, output_dim=emb_dim, input_length=max_len, embeddings_regularizer=W_reg)(input)
    emb = Dropout(0.2)(emb)

    lstm = LSTM(units=128, return_sequences=True)(emb)
    lstm = Dropout(0.5)(lstm)
    lstm = Flatten()(lstm)

    h1 = Dense(8576, activation='relu')(lstm)
    h1 = Dropout(0.5)(h1)

    output = Dense(1, activation='sigmoid', name='lstm_output')(h1)

    model = Model(input, output)

    return model

x_train, x_test, y_train, y_test = Preprocessor.load_data_binary(10000)

epochs = 5
batch_size = 64

model = lstm()
adam = Adam(lr=1e-4, beta_1=0.9, beta_2=0.999, epsilon=1e-08, decay=0.0)
model.compile(optimizer=adam, loss='binary_crossentropy',
              metrics=['accuracy'])

model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, validation_split=0.11)

model_json = model.to_json()
with open("./saved_model/gru.json", "w") as json_file:
    json_file.write(model_json)
model.save_weights("./saved_model/gru.h5")

