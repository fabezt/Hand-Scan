import cv2
import mediapipe as mp
import time
import math

from mediapipe.tasks import python
from mediapipe.tasks.python import vision

model_path = "hand_landmarker.task"

base_options = python.BaseOptions(
    model_asset_path=model_path
)

options = vision.HandLandmarkerOptions(
    base_options=base_options, # using the base modell
    running_mode = vision.RunningMode.VIDEO, # processing a video
    num_hands= 2, #detect two hands
    min_hand_detection_confidence=0.5,   # detection confidence
    min_hand_presence_confidence=0.5,
    min_tracking_confidence=0.5
)

detector = vision.HandLandmarker.create_from_options(options) #detector

camera= cv2.VideoCapture(0)

if not camera.isOpened():
    print("Error: Could not open webcam")
    exit()

#zoom variables
zoom_factor = 1.0
min_zoom = 1.0
max_zoom = 3.0
zoom_speed = 0.8
previous_time = time.time()


def detect_gesture(hand_landmarks):
    # important hand compounts 
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]
    extended_fingers = 0
    for tip, pip in zip(finger_tips,finger_pips): # looks at all finger tips / pips 

        tip_y = hand_landmarks[tip].y
        pip_y = hand_landmarks[pip].y

        if tip_y < pip_y:
            extended_fingers += 1

    print("Extended fingers:", extended_fingers)

    if extended_fingers >= 3: # determints how many fingers are up either fist or closed
        return "OPEN"

    elif extended_fingers <= 1:
        return "FIST"

    else:
        return "NEUTRAL"

    

def zoom_image(frame, zoom_factor):
    #zooming in and out of the image 
    height, width = frame.shape[:2]

    new_width = int(width / zoom_factor)
    new_height = int(height / zoom_factor)

    center_x = width // 2
    center_y = height // 2

    x1 = center_x - new_width // 2
    y1 = center_y - new_height // 2

    x2 = x1 + new_width
    y2 = y1 + new_height

    cropped = frame[y1:y2, x1:x2]

    zoomed = cv2.resize(cropped, (width, height))

    return zoomed


while True:
    success, frame = camera.read()

    if not success:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) # comverts BGR into rgb

    mp_image = mp.Image(  # the format mediapipe expectes
        image_format=mp.ImageFormat.SRGB,
        data=rgb_frame
    )

    timestamp_ms = int(time.time() * 1000)
    results = detector.detect_for_video( # process frame and returns the marked handlines
        mp_image,
        timestamp_ms
    )
    if results.hand_landmarks:
        print("success")
        for hand_landmarks in results.hand_landmarks:
            for landmark in hand_landmarks:

                height,width,channels = frame.shape
                pixel_x = int(landmark.x * width)
                pixel_y = int(landmark.y * height)

                cv2.circle(
                    frame,
                    (pixel_x, pixel_y),
                    5,
                    (0, 255, 0),
                    -1
                ) # draw the resutls
        gesture = detect_gesture(hand_landmarks)

        current_time = time.time()
        delta_time = current_time - previous_time
        previous_time = current_time

        if gesture == "FIST":
            zoom_factor += zoom_speed * delta_time

        elif gesture == "OPEN":
            zoom_factor -= zoom_speed * delta_time

        zoom_factor = max(min_zoom, min(max_zoom, zoom_factor))
        print("Gesture:", gesture)
        print("Zoom:", round(zoom_factor, 2))
    else:
        print("No hand detected")
    zoomed_frame = zoom_image(frame, zoom_factor)

    cv2.imshow("Hand Tracking", zoomed_frame) # shows the new frame
    if cv2.waitKey(1) == ord("q"):
        break
camera.release()
detector.close()
cv2.destroyAllWindows()