import cv2 # importing dependency

camera = cv2.VideoCapture(0) # Opens the first camera

lower_blue =(100, 0,0)         # lowest blue 
upper_blue =(270,150,100)   # highest blue

while True:
    sucess, frame = camera.read()   #Retrives a frame

    if not sucess:                 # If something went wrong 
        print("Something went wrong!")
        break

    mask = cv2.inRange(frame, lower_blue, upper_blue)

    cv2.imshow("Original Camera", frame)
    cv2.imshow("Blue detected", mask)
    print("Screen pixel:", frame[350, 120])

    

    if cv2.waitKey(1) == ord("q"): # Waits for keyboard press q then stops
        break

camera.release          #Releases the camera
cv2.destroyAllWindows   # Destroys all windows