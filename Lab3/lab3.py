from gopigo import *
import cv2, picamera
import numpy as np
import time

#robot settings
set_speed(100)

refPt = []
list_of_clicks = []
camera = picamera.PiCamera()
init_flag = False
init_area = 0
IMAGE_CENTER = 360
CENTER_THRESHOLD = 60
AREA_THRESHOLD = 0.2 # 20% of area 

def main():
  global camera
  time.sleep(0.5) # Sleep fixes bug where first image is too dark
  camera.capture('image.jpg')
  img = cv2.imread('image.jpg',1)
  getXY(img)

def getXY(img):
  #define the event
  def getxy_callback(event, x, y, flags, param):
    global list_of_clicks, refPt, camera
    clone = img.copy()
    image = clone
    if event == cv2.EVENT_LBUTTONDOWN:
      refPt = [(x,y)]
      list_of_clicks.append([x,y])
      print "click point is...", (x,y)

    elif event == cv2.EVENT_LBUTTONUP:
      refPt.append((x,y))
      cropping = False
      print "release point is...", (x,y)
      cv2.rectangle(image, refPt[0], refPt[1], (0,255,0), 2)
      
      cv2.imshow('image', image)
      cv2.waitKey(1000)

      #crop region our color of interest is in
      region = image[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0] ]
      
      # Convert BGR to HSV 
      # Only need to calculate hsvR once
      hsvR = cv2.cvtColor(region, cv2.COLOR_BGR2HSV)
      
      #find histogram of region
      hist = cv2.calcHist([hsvR], [0,1], None, [180, 256], [0, 180, 0, 256])
      cv2.normalize( hist, hist, 0, 255, cv2.NORM_MINMAX)
      
      while (True):
        findCentroid(image, hist)
        camera.capture('image.jpg')
        image = cv2.imread('image.jpg', 1)

  #Read the image
  print "Reading the image..."
  
  #Set mouse CallBack event
  cv2.namedWindow('image')
  cv2.setMouseCallback('image', getxy_callback)
  
  #show the image
  print "Please select the color by clicking on the screen..."
  cv2.imshow('image', img)
  cv2.waitKey(0)
  cv2.destroyAllWindows()

  return list_of_clicks

def findCentroid(img, histogram):
  '''This function will calculate the centroid of the largest object'''
  global init_area, init_flag
  
  #calculate mask
  #hsvI must be calculated for each new image  
  hsvI = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  dst = cv2.calcBackProject([hsvI], [0,1], histogram, [0, 180, 0, 256], 1)

  # Now convolute with circular disc
  disc = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
  cv2.filter2D(dst,-1,disc,dst)

  # threshold and binary AND
  ret,mask = cv2.threshold(dst,50,255,cv2.THRESH_BINARY)
  mask_multi = cv2.merge((mask,mask,mask))
  res = cv2.bitwise_and(img,mask_multi) 

  # get rid of unwanted stuff in image
  blur = cv2.medianBlur(mask,7)
  kernel = np.ones((5,5),np.uint8)
  erosion = cv2.erode(blur,kernel,iterations=1)
  dilate = cv2.dilate(erosion,kernel,iterations=1)
  
  dst = np.uint8(dilate)
  connectivity = 4
  output = cv2.connectedComponentsWithStats(dst)
  
  num_labels = output[0]
  labels = output[1]
  stats = output[2]
  centroids = output[3]
  
  # initialize list of zeros so that we can keep track of label counts
  numList = [0] * num_labels
  for x in np.nditer(labels):
    numList[x] += 1
  # find the blob label with the greatest count -> biggest area
  greatest = 0
  mode_label = -1
  for i in range(1,len(numList)):
    if numList[i] > greatest:
      greatest = numList[i]
      mode_label = i
  # take area of blob with label that appeared the most    
  area = stats[mode_label][4]
  x_centroid = centroids[mode_label][0]

  # take initial object area only on first iteration to compare later
  if init_flag == False:
    init_area = area
    init_flag = True

  reposition(area, x_centroid)

def reposition(area, x_centroid):
  '''This function calculates the reposition required to follow an object'''
  global init_area, IMAGE_CENTER, CENTER_THRESHOLD, AREA_THRESHOLD

  # Set ranges to account for error in calculations
  CENTER_MIN_RANGE = IMAGE_CENTER - CENTER_THRESHOLD
  CENTER_MAX_RANGE = IMAGE_CENTER + CENTER_THRESHOLD
  AREA_MIN_RANGE = init_area * (1 - AREA_THRESHOLD)
  AREA_MAX_RANGE = init_area * (1 + AREA_THRESHOLD)

  # This block is for centering on the object
  if x_centroid > CENTER_MAX_RANGE:
    enc_tgt(1,1,1)
    right_rot()
    while(read_enc_status()):
      continue  
  elif x_centroid < CENTER_MIN_RANGE:
    enc_tgt(1,1,1)
    left_rot()
    while(read_enc_status()):
      continue  

  # This block is for adjusting to keep same distance from object
  if area > AREA_MAX_RANGE:
    enc_tgt(1,1,8)
    bwd()
    while(read_enc_status()):
      continue
  elif area < AREA_MIN_RANGE:
    enc_tgt(1,1,8)
    fwd()
    while(read_enc_status()):
      continue

main()
