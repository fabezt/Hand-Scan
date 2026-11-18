import cv2 # importing dependency

camera = cv2.VideoCapture(0) # Opens the first camera

lower_blue =(100, 0,0)         # lowest blue 
upper_blue =(290,190,100)   # highest blue

while True:
    sucess, frame = camera.read()   #Retrives a frame

    if not sucess:                 # If something went wrong 
        print("Something went wrong!")
        break

    mask = cv2.inRange(frame, lower_blue, upper_blue)
    contours, hierarchy = cv2.findContours(
        mask,           #The mask we created
        cv2.RETR_EXTERNAL,  #Get the outside contours
        cv2.CHAIN_APPROX_SIMPLE  # Only choose important outside Contours so it builds straight line
    )
    for contour in contours:   # processes each contour
        area = cv2.contourArea(contour) #calculates the area enclosed the contour
        if area > 500: # sorts out small contour areas
            x, y, w, h = cv2.boundingRect(contour)  # calculats the smallest rectangle that closes the area

            cv2.rectangle( 
                frame, #drawing the rectangle the image one 
                (x,y),
                (x + w, y + h),
                (0, 255, 0),
                2
            )

    cv2.imshow("Original Camera", frame)
    cv2.imshow("Blue detected", mask)
    

    

    if cv2.waitKey(1) == ord("q"): # Waits for keyboard press q then stops
        break

camera.release          #Releases the camera
cv2.destroyAllWindows   # Destroys all windows