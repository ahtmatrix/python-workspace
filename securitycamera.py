import cv2
import time
import datetime


# 0 and above to increment and look for cameras
cap = cv2.VideoCapture(0)


# makes cascade classifer, already prebuilt into opencv
# pass base directory into the cascade classifer

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_fullbody.xml")


detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 5




frame_size = (int(cap.get(3)), int(cap.get(4)))

# pass mp4v to into separate arguments m p 4 v using the * character
fourcc = cv2.VideoWriter_fourcc(*"mp4v")


while True:
    # _, means placeholder variable
    # cap.read() returns stuff besides frame so we only care about the frames
    _, frame = cap.read()

    # gives us a gray image 
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # gray is the image to detect faces
    # pass frame and scale factor keep it 1.1 to 1.5 balance between speed and accuracy, 
    # lower the number is slower
    # last arg is minimum number of neighbors, how many neighbors to detect in order to call it a face
    # 5 boxes overlapping for it to be a face
    # higher the number = less faces
    # lower the number = more faces


    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = body_cascade.detectMultiScale(gray, 1.3, 5)

    if len(faces) + len(bodies) > 0:


        
        if detection:
            timer_started = False
        # if we weren't detection started recording
        else:
            detection = True
            
            # format time
            current_time = datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S")

            out = cv2.VideoWriter(f"{current_time} security video.mp4", fourcc, 30.0, frame_size)
            print("started recording")
    elif detection:
        if timer_started:
            if time.time() - detection_stopped_time > SECONDS_TO_RECORD_AFTER_DETECTION:
                detection = False
                timer_started = False
                out.release()
                print('stopped recording')
        else:
            timer_started = True
            detection_stopped_time = time.time()


    if detection:
        out.write(frame)


    for (x, y, width, height) in faces:
        # draws on the RGB frame
        #                   top right      bottom right      blue green red, line thickness 3
        cv2.rectangle(frame, (x,y), (x+width, y + height), (0,0,255), 3)



    # shows viewer
    cv2.imshow("Camera", frame)
    if cv2.waitKey(1) == ord('q'):
        break

out.release()
cap.release()
cv2.destroyAllWindows()

