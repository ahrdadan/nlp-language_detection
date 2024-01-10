# -*- coding: utf-8 -*-
"""Belajar Pengembangan Machine Learning NLP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1TgCNkUsCuemsOrvNWKj7SC-p9yZxrS_i

# Proyek Pertama : Membuat Model NLP dengan TensorFlow
- Nama: Ahmad Ramadhan
- Email: ahmad.ramadhan@live.jp
- Id Dicoding: dhadhan

## Category & Dataset
- NLP
- Dataset: https://www.kaggle.com/datasets/basilb2s/language-detection

## Install Kaggle
"""

# !pip install kaggle

"""## Import Kaggle Token
Upload Kaggle JSON refer to:
https://www.kaggle.com/discussions/general/156610
"""

# from google.colab import files
# files.upload()

# !mkdir ~/.kaggle
# !cp kaggle.json ~/.kaggle/
# !chmod 600 ~/.kaggle/kaggle.json

# !kaggle datasets download -d basilb2s/language-detection

# !unzip language-detection.zip

"""---

## NLP Start
"""

# dataframe
import pandas as pd
import numpy as np

# split data
from sklearn.model_selection import train_test_split

# modeling
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping

# visualisasi loss & acc
import matplotlib.pyplot as plt

# Read Dataset
df = pd.read_csv('https://raw.githubusercontent.com/ahrdadan/nlp-language_detection/main/Language%20Detection.csv')

# Preprocessing
df = df.dropna(axis=0)
df.drop_duplicates()

df = df.rename(columns={'Text': 'text', 'Language':'label'})

name_label = df['label'].unique()

# # Seleksi column label tertentu
selected_labels = ['English', 'French','Spanish','Arabic']
df = df[df['label'].isin(selected_labels)]

# Convert to one-hot encoding
label_pd = pd.get_dummies(df.label)
new_df = pd.concat([df, label_pd], axis=1)
new_df = new_df.drop(columns='label')

# transform column to array
desc = new_df['text'].values

# Get labels
label = new_df[selected_labels].values

# Split Dataset to train (80%) and validation set (20%)
desc_train, desc_test, label_train, label_test = train_test_split(desc, label, test_size=0.2)

#data tokenizing
tokenizer = Tokenizer(num_words=5_000, oov_token='<oov>')
tokenizer.fit_on_texts(desc_train)
tokenizer.fit_on_texts(desc_test)

#data sequencing
train_sequence = tokenizer.texts_to_sequences(desc_train)
test_sequence = tokenizer.texts_to_sequences(desc_test)

#data padding
train_padded = pad_sequences(train_sequence)
test_padded = pad_sequences(test_sequence)

# Modelling
model = tf.keras.Sequential([
    tf.keras.layers.Embedding(input_dim=7_500, output_dim=64),
    tf.keras.layers.LSTM(128),
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dropout(0.6),
    tf.keras.layers.Dense(64, activation='relu'),
    tf.keras.layers.Dropout(0.4),
    tf.keras.layers.Dense(label_test.shape[1], activation='softmax'),
])

# compile model
# optimizer = Adam(learning_rate=0.001)
model.compile(loss='categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# add callbacks for desired acc
class stop_callback(tf.keras.callbacks.Callback):
  def on_epoch_end(self, epoch, logs={}):
    if(logs.get('accuracy')>0.94 and logs.get('val_accuracy')>0.94):
      print("\nacc telah dicapai > 94%!")
      self.model.stop_training = True
callbacks = stop_callback()

# train model
num_epochs = 500
history = model.fit(train_padded, label_train,
                    epochs=num_epochs,
                    validation_data=(test_padded, label_test),
                    verbose=1,
                    callbacks=[callbacks])


#plot accuracy
plt.plot(history.history['accuracy'], label='Training')
plt.plot(history.history['val_accuracy'], label='Validation')
plt.title('Plot Accuracy')
plt.ylabel('Accuracy')
plt.xlabel('Epoch')
plt.legend(loc="lower right")
plt.show()

#plot loss
plt.plot(history.history['loss'], label='Training')
plt.plot(history.history['val_loss'], label='Validation')
plt.title('Plot Loss')
plt.ylabel('Loss')
plt.xlabel('Epoch')
plt.legend(loc="upper right")
plt.show()

"""# Result
Dengan NLP pada deteksi bahasa dari bahasa berikut ini:
- English
- French
- Spanish
- Arabic

Akurasi dan Validasi akurasi yang didapatkan adalah **94%** dengan jumlah datasets 3754
"""