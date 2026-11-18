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

EMOJI_SIZE = 100
def load_emoji(path):
    img = cv2.imread(path)
    if img is None:
        raise FileNotFoundError(f"Couldnt fine {path}")
    return cv2.resize(img, (EMOJI_SIZE, EMOJI_SIZE))
emojis = {
    "up": load_emoji("happy.jpg"),
    "middle": load_emoji("ok.jpg"),
    "down": load_emoji("sad.webp"),
    "unsure": load_emoji("error.webp"),
}


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
    else:
        print("No hand detected")
    cv2.imshow("Hand Tracking", frame) #creates window and displays current frame
    if cv2.waitKey(1) == ord("q"):
        break
camera.release()
detector.close()
cv2.destroyAllWindows()