import string
from collections import defaultdict,Counter
import os
import numpy as np
from processing.image.image_processing import read_image,process_image
from processing.image.handwriting.htr_image_processing import get_bounding_box_from_image
# Extract word from line
# INPUT: 'a01-000u-00-03 ok 154 919 757 166 78 VB stop\n'
# OUTPUT: 'stop'
def get_word(line):
  return " ".join(line.split("\n")[0].split(" ")[8:]).strip()


# Returns a list of all words, each word has list of occurences
# INPUT:   # each line contains image and word info
# 'a01-000u-00-03 ok 154 919 757 166 78 VB stop\n',
# 'a01-000u-00-04 ok 154 1185 754 126 61 NPT Mr.\n',
# 'a01-000u-00-05 ok 154 1438 746 382 73 NP Gaitskell\n',
# OUTPUT:  # each word has list of corresponding image info
# unique_words
# 'Sea': ['a02-027-08-00 ok 184 351 2328 121 74 NPL Sea',
#         'c02-017-06-07 ok 191 1913 2006 122 67 NPL Sea'],
# 'professes': ['a02-027-08-05 ok 184 1153 2333 280 90 VBZ professes'],
# 'return': ['a02-027-09-01 ok 183 568 2528 213 64 VB return',
# counter_input_data
#  'A',
#  'MOVE',
#  'to',

def get_unique_words_and_counter(file_path):
  unique_words = defaultdict(list)
  counter_input_data = []
  word_file = open(file_path, "r").readlines()
  for line in word_file:
      if line[0] == "#": # lines that start with # are comments and don't contain information about words
          continue
      if line.split(" ")[1] != "err": # err means word may not be segmented correctly
          word = get_word(line)
          unique_words[word].append(line.strip())
          counter_input_data.append(word)
  return unique_words,counter_input_data


# # most_common_words
# [('the', 4986),
#  (',', 4376),
#  ('.', 4094),
#  ('of', 2741),    
# list containing n images of m most common words
# n: max_images_per_word
# m: max_words
# OUTPUT:
# ['a01-000u-04-05 ok 157 1665 1476 167 61 ATI the',
#  'a01-000x-03-07 ok 179 1650 1285 69 78 ATI the',
def filter_labels(most_common_words,unique_words,max_words,max_images_per_word): 
  filtered_labels = []
  num_word = 0
  for word,size in most_common_words:
    flag = False
    for char in word: # only continue if word contains any alphabet characters
      if char in string.ascii_letters:
        flag=True
        break
    if flag:
      if num_word < max_words:
        if size >= max_images_per_word: # only consider words with num images > max_images
            filtered_labels.extend(unique_words[word][0:max_images_per_word])
            num_word+=1
      else:
        break        
  return filtered_labels

# Filtered list of words by given list and max images per word
def get_labels_for_the_words(unique_words,words,max_images_per_word):
  labels = []
  for word in unique_words:
    if word in words:
      labels.extend(unique_words[word][0:max_images_per_word])
  return labels


# Filtered list of words by given list and max images per word

# INPUT:
# train_words
# {'backed','be','by','down','for','from','has','he','is'}

def get_input_for_labels_based_on_training_words(file_path,train_words,max_images_per_word):
  unique_words,counter_input_data = get_unique_words_and_counter(file_path)
  input_for_labels = get_labels_for_the_words(unique_words,train_words,max_images_per_word)
  return input_for_labels


# Filtered list of words by max number of words and max images per word

# counter_data
# 'A': 143,
# 'MOVE': 2,
# 'to': 2255,

# most_common_words
# [('the', 4986),
#  (',', 4376),
#  ('.', 4094),
#  ('of', 2741),

# OUTPUT: 
# input_for_labels (filtered list of words and images we will use)
# ['a01-000u-04-05 ok 157 1665 1476 167 61 ATI the',
#  'a01-000x-03-07 ok 179 1650 1285 69 78 ATI the',

def get_input_for_labels_based_max_size(file_path,max_words=50,max_images_per_word=100):
  unique_words,counter_input_data = get_unique_words_and_counter(file_path)
  counter_data=Counter(counter_input_data)    
  most_common_words = counter_data.most_common()
  input_for_labels = filter_labels(most_common_words,unique_words,max_words,max_images_per_word)
  return input_for_labels


# Get image arrays and word labels
def get_images_and_labels(base_path, samples,IMAGE_SIZE, forms=False):
    base_image_path = os.path.join(base_path, "/words")
    data = []
    for (i, file_line) in enumerate(samples):
        line_split = file_line.strip()
        line_split = line_split.split(" ")
        image_name = line_split[0]
        partI = image_name.split("-")[0]
        partII = image_name.split("-")[1]
        img_path = os.path.join(
            base_image_path, partI, partI + "-" + partII, image_name + ".png"
        )
        if os.path.getsize(img_path):
            img = read_image(img_path, forms)
            image_array = process_image(img, IMAGE_SIZE)
            label = get_word(file_line)
            data.append((image_array,label))
    return data


# encode word labels to numeric values

def get_features_and_labels(input_data, label_encoder):
  tmp_features = []
  tmp_labels =[]
  for feature,label in input_data:
      tmp_features.append(feature)
      tmp_labels.append(label)
  features = np.array(tmp_features)
  labels =label_encoder.fit_transform(np.array(tmp_labels))
  return features,labels


# Returns array for each word
def get_words_from_image(image_path, IMAGE_SIZE, forms=False):
  bounding_boxes = get_bounding_box_from_image(image_path, forms)
  word_images = []
  img = read_image(image_path, forms)
  for bounding_box in bounding_boxes:
    x, y, w, h = bounding_box
    cropped_img = img[y:h,x:w].copy()
    word_image = process_image(cropped_img, IMAGE_SIZE)
    word_images.append(word_image)
  return word_images
