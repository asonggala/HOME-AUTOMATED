import face_recognition, cv2, time, datetime, pygame, pyttsx3, os 
import numpy as np
import RPi.GPIO as GPIO
from pocketsphinx import LiveSpeech, get_model_path

pygame.init()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice',voices[10].id)
model_path = get_model_path()

i = [18,24]
GPIO.setmode(GPIO.BCM)
GPIO.setup(4,GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.OUT)
GPIO.setup(i,GPIO.OUT)
GPIO.setup(20,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(20,GPIO.LOW)
GPIO.setup(21,GPIO.LOW)
GPIO.output(i,GPIO.LOW)
p = GPIO.PWM(7, 50)
p.start(0)

speech = LiveSpeech(
    verbose=False,
    sampling_rate=16000,
    buffer_size=2048,
    no_search=False,
    full_utt=False,
    hmm = os.path.join(model_path, 'en-us'),
    lm='en-us.lm.bin',
    dic='cmudict-en-us.dict',
     kws='key.list',
    ln=False)

imgChristian = face_recognition.load_image_file('/home/pi/Desktop/SuperFinal/FaceData/christian.jpg')
imgChristian_encoding = face_recognition.face_encodings(imgChristian)[0]

imgMark = face_recognition.load_image_file('/home/pi/Desktop/SuperFinal/FaceData/mark.jpg')
imgMark_encoding = face_recognition.face_encodings(imgMark)[0]

imgj = face_recognition.load_image_file('/home/pi/Desktop/SuperFinal/FaceData/Joshua.jpg')
imgJo_encoding = face_recognition.face_encodings(imgj)[0]
# Create arrays of known face encodings and their names
known_face_encodings = [imgChristian_encoding, imgMark_encoding, imgJo_encoding]
known_face_names = ["Christian", "Mark","Joshua"]
date = datetime.datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
print('ready')

    
def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(7, True)
    p.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(7, False)
    p.ChangeDutyCycle(0)
    
def parseVoice(word):
    if word == 'LIGHT ONE OPEN':
        print('Light one on')
        engine.setProperty('rate',150)
        engine.say("Light one is on")
        engine.runAndWait()
        GPIO.output(20, GPIO.HIGH)
        
        
    if word == 'LIGHT ONE CLOSE':
        print('Light one off')
        engine.setProperty('rate',150)
        engine.say("Light one is off")
        engine.runAndWait()
        GPIO.output(20, GPIO.LOW)
        
    if word == 'LIGHT TWO OPEN':
        print('Light two on')
        engine.setProperty('rate',150)
        engine.say("Light two is on")
        engine.runAndWait()
        GPIO.output(21, GPIO.HIGH)
        
    if word == 'LIGHT TWO CLOSE':
        print('Light two off')
        engine.setProperty('rate',150)
        engine.say("Light two is off")
        engine.runAndWait()
        GPIO.output(21, GPIO.LOW)
        
    if word == 'FAN OPEN':
        print('Fan is on')
        engine.setProperty('rate',150)
        engine.say("Fan is on")
        engine.runAndWait()
        
    if word == 'FAN CLOSE':
        print('Fan is off')
        engine.setProperty('rate',150)
        engine.say("Fan is off")
        engine.runAndWait()
        
    if word == 'DOOR OPEN':
        print('Door is open')
        engine.setProperty('rate',150)
        engine.say("Opening Door")
        engine.runAndWait()
        
    if word == 'WHAT ARE YOU':
        print('Hello, my name is CLEDD and I am your assistant')
        engine.setProperty('rate',150)
        engine.say("Hello, my name is cled and I am your assistant")
        engine.runAndWait()
        
    return word

def camera():
    
    video_capture = cv2.VideoCapture(0)
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    count = 0
    
    while True():
        ret, frame = video_capture.read()

        print("button is pressed")
        pygame.mixer.music.load("Doorbell.mp3")
        pygame.mixer.music.play()
        time.sleep(1.5)
        print('looking for faces')
        time.sleep(1)
        cv2.imwrite("trail/User." + str(date) + '.' + str(count) + ".jpg", frame)
        print("saved",count)
        count += 1
        
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
        rgb_small_frame = small_frame[:, :, ::-1]

        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

            face_names = []
            for face_encoding in face_encodings:
            # See if the face is a match for the known face(s)
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                name = "Unknown"
            
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                    print(name)
                    SetAngle(90)
                    time.sleep(2)
                    SetAngle(0)
                    engine.setProperty('rate',150)
                    engine.say("Welcome "+name+"")
                    engine.runAndWait()
                face_names.append(name)

        process_this_frame = not process_this_frame
        
def speak():       
    for phrase in speech:
        word = str(phrase)
        Output_string = parseVoice(word)
        print('you said :', Output_string)
        
while True:
    speak()
    button = GPIO.input(4)
    if button == False:
        camera()
        print('button is press')
        time.sleep(.2)
        
        
        
        

