import cv2
import numpy as np
from processing.image.image_processing import read_image,thresholding,show_image

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

