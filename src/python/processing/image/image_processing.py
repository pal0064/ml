import cv2
import numpy as np
import matplotlib.pyplot as plt

# Returns array of image (CROP FOR FORMS)

def read_image(image_path,forms=False,color=False):
      if color:
        img = cv2.imread(image_path)
        if forms:
          img = img[670:2700, :]
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # h, w, c = img.shape

        # if w > 1000:
            
        #     new_w = 1000
        #     ar = w/h
        #     new_h = int(new_w/ar)
            
        #     img = cv2.resize(img, (new_w, new_h), interpolation = cv2.INTER_AREA)
      else:
          img = cv2.imread(image_path,cv2.IMREAD_GRAYSCALE) 
          if forms:
            img = img[670:2700, :]
      return img

# Resize image array

def process_image(img, IMAGE_SIZE):
    resized_img = cv2.resize(img,IMAGE_SIZE)
    image_array = np.array(resized_img).flatten()
    return image_array


# Shows image using array as input

def show_image(image):
  plt.imshow(image, cmap='gray')


# Converts to grayscale then inverts image colors

def thresholding(image):
    img_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
    # plt.imshow(thresh, cmap='gray')
    return thresh

# Detects bounding boxes for each word

def get_bounding_box_from_image(file_name, forms=False):
  img = read_image(file_name,forms,color=True)
  # plt.imshow(img);
  thresh_img = thresholding(img);
  # #dilation
  kernel = np.ones((3,85), np.uint8)
  if forms:
     dilated = cv2.dilate(thresh_img, kernel, iterations = 3)
  else:
    dilated = cv2.dilate(thresh_img, kernel, iterations = 1)
  # plt.imshow(dilated, cmap='gray');
  (contours, heirarchy) = cv2.findContours(dilated.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
  sorted_contours_lines = sorted(contours, key = lambda ctr : cv2.boundingRect(ctr)[1]) # (x, y, w, h)
  #dilation
  if forms:
    kernel = np.ones((3,40), np.uint8)
  else:
    kernel = np.ones((3,15), np.uint8)
  dilated2 = cv2.dilate(thresh_img, kernel, iterations = 1)
  # plt.imshow(dilated2, cmap='gray');
  img3 = img.copy()
  bounding_boxes = []

  for line in sorted_contours_lines:
      
      # roi of each line
      x, y, w, h = cv2.boundingRect(line)
      roi_line = dilated2[y:y+h, x:x+w]
      
      # draw contours on each word
      (cnt, heirarchy) = cv2.findContours(roi_line.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
      sorted_contour_words = sorted(cnt, key=lambda cntr : cv2.boundingRect(cntr)[0])
      
      for word in sorted_contour_words:
          
          if cv2.contourArea(word) < 400:
              continue
          
          x2, y2, w2, h2 = cv2.boundingRect(word)
          bounding_boxes.append([x+x2, y+y2, x+x2+w2, y+y2+h2])
          cv2.rectangle(img3, (x+x2, y+y2), (x+x2+w2, y+y2+h2), (0, 255, 0),2)
  show_image(img3)
  return bounding_boxes

