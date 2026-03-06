import cv2

#face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades +
#                                    "haarcascade_frontalface_default.xml")
#smile_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 
#                                    "haarcascade_smile.xml")
#eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 
#                                    "haarcascade_eye.xml")

def detect_features(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            #You can also specify minSize and maxSize
    for (x, y, w, h) in faces:
        frame = cv2.rectangle(frame, (x, y), (x+w, y+h),
                              color=(0, 255, 0), thickness=5)
        face = frame[y : y+h, x : x+w]
        gray_face = gray[y : y+h, x : x+w]
        smiles = smile_cascade.detectMultiScale(gray_face,
                                                 2.5, minNeighbors=9)
        for (xp, yp, wp, hp) in smiles:
            face = cv2.rectangle(face, (xp, yp), (xp+wp, yp+hp),
                              color=(0, 0, 255), thickness=5)
            
        eyes = eye_cascade.detectMultiScale(gray_face,
                    2.5, minNeighbors=7)
        for (xp, yp, wp, hp) in eyes:
            face = cv2.rectangle(face, (xp, yp), (xp+wp, yp+hp),
                              color=(255, 0, 0), thickness=5)

    return frame


stream = cv2.VideoCapture(0) #This can be changed to the filepath to camera (ros2_astra_camera)

if not stream.isOpened():
    print("No stream :(")
    exit() #If the stream isn't open, exit


### Video Writer (Permenately save the stream)
fps = stream.get(cv2.CAP_PROP_FPS)
width = int(stream.get(3))
height = int(stream.get(4))

# https://softron.zendesk.com/hc/en-us/articles/207695697-List-of-FourCC-codes-for-video-codecs
output = cv2.VideoWriter("Assests/facial_rec.mp4",
                         cv2.VideoWriter_fourcc('m', 'p', '4', 'v'), fps = fps, frameSize=(width, height))
##########

while (True): #If stream is opened, read/display each frame, frame by frame
    ret, frame = stream.read()
    if not ret:
        print("No more stream :(")
        break

    frame = detect_features(frame)
    frame = cv2.resize(frame, (width, height))
    output.write(frame)
    cv2.imshow("Webcam!", frame) #Display the frame
    if cv2.waitKey(1) == ord('q'): #We use 1 here as "False" and casts and integer(1) it to 'q' key, which exits the infinite loop for the stream
        break
