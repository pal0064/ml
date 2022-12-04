import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
import cv2
from processing.image.image_processing import show_image
from datasets.iam.labels_pre_processing import get_words_from_image
from processing.audio.tts import convert_to_audio
from ml.model.model_exec import get_predict_from_model
# Converts encoded numeric labels back words

def get_predictions(label_encoder,results):
  labels_inversed = label_encoder.inverse_transform(results)
  return labels_inversed

# Prints each word image and predicted label

def show_predictions(labels,x_test,IMAGE_SIZE,sample=5):
  total = len(labels[0:sample])
  breaker = 4
  _, ax = plt.subplots((total//4)+1,4,figsize=(15, 8))
  results = []
  for idx,img_ar in enumerate(x_test[0:sample]):
      results.append(labels[idx])
      img = np.round(img_ar * 255).astype(int).reshape(IMAGE_SIZE)
      title = f"Prediction: {labels[idx]}"
      ax[idx // breaker, idx % breaker].imshow(img, cmap="gray")
      ax[idx // breaker, idx % breaker].set_title(title)
      ax[idx // breaker, idx % breaker].axis("off")
  for idx in range((total//4+1) *4):
     ax[idx // breaker, idx % breaker].axis("off")
  plt.show()
  return results

  # Get word count in both train and test

def get_word_count(label_encoder,y_train,y_test):
  words = []
  for i in get_predictions(label_encoder,y_train):
    words.append(i)
  for i in get_predictions(label_encoder,y_test):
    words.append(i)
  return Counter(words)


  # Runs selected model on image path and returns predicted words and sound file
def recognize(model,label_encoder, image_path,image_size,normalize_scale,show_sample=10, forms=False, engine_type='gtts'):
  img = cv2.imread(image_path)
  if forms:
    img = img[670:2700, :]
  show_image(img)
  words = np.array(get_words_from_image(image_path, image_size, forms))/normalize_scale
  preds = get_predict_from_model(model,words)
  predicted_labels = get_predictions(label_encoder,preds)
  sound_file = convert_to_audio(predicted_labels,engine_type)
  show_predictions(predicted_labels,words,image_size,sample=show_sample)
  return sound_file, predicted_labels


  # Get word count in both train and test

def get_word_count(label_encoder,y_train,y_test):
  words = []
  for i in get_predictions(label_encoder,y_train):
    words.append(i)
  for i in get_predictions(label_encoder,y_test):
    words.append(i)
  return Counter(words)