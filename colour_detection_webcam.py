import argparse
import cv2
import numpy as np
import pandas as pd

## Creating argument parser to take image path from command line
# ap = argparse.ArgumentParser()
# ap.add_argument('-i', '--image',required = True, help = "Image Path")
# args = vars(ap.parse_args())
# img_path = args['image']

## Read the image
# img = cv2.imread(img_path)

r = g = b = xpos = ypos = 0
clicked = False

## Get (x,y) coordinates of mouse click and find r,g,b values
def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        global b,g,r,xpos,ypos, clicked
        print("clicked")
        clicked = True
        xpos = x
        ypos = y
        b,g,r = frame[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

## Find closest colour with the given R,G,B values by calculating distance
## distance = abs(Red – ithRedColor) + (Green – ithGreenColor) + (Blue – ithBlueColor)
def getColourName(R, G, B):
    min = 10000
    for i in range(len(csv)):
        d = abs(R - int(csv.loc[i,"R"])) + abs(G - int(csv.loc[i,"G"])) + abs(B - int(csv.loc[i,"B"]))
        if(d<=min):
            min = d
            cname = csv.loc[i,"colour_name"]
    return cname

# Read the csv file
index = ["colour", "colour_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names = index, header = None)

# Display webcam and set the callback function for mouse click
cv2.namedWindow('Webcam')
cv2.setMouseCallback('Webcam',draw_function)

# Initialize video capture instance
cap = cv2.VideoCapture(0)
scaling_factor = 0.8
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while(1):
    ret, frame = cap.read()
    frame = cv2.resize(frame, None, fx=scaling_factor, fy=scaling_factor, interpolation=cv2.INTER_AREA)
    cv2.imshow('Webcam', frame)

    if(clicked):
        cv2.rectangle(frame,(20,20), (750,60), (b,g,r), -1)

        text = getColourName(r,g,b) + ' R = ' + str(r) + ' ,G = ' + str(g) + ' ,B = ' + str(b)
        cv2.putText(frame, text, (50,50),2,0.8,(255,255,255),2,cv2.LINE_AA)
        if(r+g+b>=600):
            cv2.putText(frame, text,(50,50),2,0.8,(0,0,0),2,cv2.LINE_AA)
        ## print(text)
        cv2.imshow('Webcam', frame)
        ## clicked = False

    if(cv2.waitKey(20) & 0xFF==27):
        break

cap.release()
cv2.destroyAllWindows()
