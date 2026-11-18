# In this document I will note all my learnings that I learned during this programme

## Computer screen layout

While it might seem that the pixel coordinate system is like the mathematical one, it is not the case. The coordinate system starts in the top left corner and goes till the right down corner. Therefore, the lower down you go, the greater the Y pixel coordinate gets and the more right you go, the greater the X pixel coordinate gets. If we have a centre at (320, 240) and our object lies at (340, 260), it lies 20 pixels more to the right and 20 pixels more down. For a visual concept view Coordination_Example.png

## Understanding how a computer sees.

A computer sends numerical data representing pixels instead of viewing a picture like a human. For exmaple one pixel would be (255, 0, 0) this means this pixel is red. With those codes the computer can bild pictures. Therefore we could track red pixels on the screen and get the position of a red object. Important you may seperate between RGB (255,0,0) and OpenCV's BGR (0,0,255).

## Connecting a Camera to python

A video is just a sequence of many pictures called Frames. 30 Fps vides are videos with 30 Frames per second. The goal is to catch each frame and analyze it for objects to detect them. In camera_test.py i created a test connection and released the camera on the press of the key "q" a problem the image is mirrored. One important thing OpenCV uses y,x not x,y when talking about pixels. 

## Pixel behavior
While movment sun or shadow can influence the pixels color code you may need a brighter acceptence of colors when you search for red objects. Even after placing them directly next to each other they still vary in frame shape. 
Example:
    pixel_1 = frame[150,400]
    pixel_2 = frame [150, 401]
    print("Pixel 1:", pixel_1)
    print("Pixel 2", pixel_2)
Output:
    Pixel 1: [116 117 126]
    Pixel 2 [116 117 126]

## Detecting Objects
While a blue Pixel might look like [200,30,20] a not blue might look like [20,30,200] real world pixels arent exact blue so we will use a color range.  

## Binary Mask
In order to check an entired frame we create masks for example if we have the values lower_blue = (100, 0, 0)
upper_blue = (255, 100, 100) everything between lower_blue and upper_blue will be accepted. Displayed as white in our mask everything else is black and not accepted. Therefore we can check a frame where it has blue pixels.

## Object localisation
1. Create a Mask for a color range 
2. Find the outlines of connected regions
3. We draw rectangle around each detected region

A Rectangle is build from 
- x = horizontal position
- y = vertical position 
- w = width
- h = height

## Hand Tracker
While the color approce worked for colored objects this wouldnt work for a hand tracker. We need a programm like MediaPipe that detects elements like wrist and fingers to identify a hand. Mediapip uses coordinates between 0 and 1 as in 0 left edge and 1 right edge throught the mathematic formulas:
pixel_x = int(x * frame_width)
pixel_y = int(y * frame_height)
we can convert them into actual frame coordinaten.
Through the Mediapipe liberay we can use the 21 detected hand marks as a tracking system for refernce view 21-coordinates.png
Therefore wrist = hand_landmarks.landmark[0] would detected the wrist which we can extracte the position frome:
print(wrist.x)
print(wrist.y)
print(wrist.z)