import face_recognition
import cv2
import numpy as np
from picamera2 import Picamera2
import time
import pickle
import pyttsx3
import speech_recognition as sr
from datetime import datetime
import pandas as pd
import os
import tkinter as tk
from tkinter import simpledialog

# Text-to-Speech
engine = pyttsx3.init()
def speak(message):
    engine.say(message)
    engine.runAndWait()
# Voice input
def listen_lecture_name(timeout=5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            speak("Please say your lecture name.")
            print("Listening...")
            audio = r.listen(source, timeout=timeout)
            lecture = r.recognize_google(audio)
            print(f"Recognized: {lecture}")
            return lecture
        except Exception as e:
            print(f"Voice input failed: {e}")
            return None

# Fallback GUI input
def get_lecture_name_gui(student_name):
    root = tk.Tk()
    root.withdraw()
    lecture = simpledialog.askstring("Lecture Name", f"Enter lecture name for {student_name}:")
    root.destroy()
    return lecture
# Combined method
def get_lecture_name_combined(student_name):
    lecture = listen_lecture_name()
    if lecture and lecture.strip() != "":
        return lecture
    else:
        speak("Voice not detected. Please enter your lecture name in the window.")
        return get_lecture_name_gui(student_name)

# Excel attendance
EXCEL_FILE = "attendance.xlsx"
def mark_attendance(name, lecture):
    now = datetime.now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%H:%M:%S')
    new_data = pd.DataFrame([[name, lecture, date_str, time_str]],
                            columns=['Name', 'Lecture', 'Date', 'Time'])
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
        df = pd.concat([df, new_data], ignore_index=True)
    else:
        df = new_data
    df.to_excel(EXCEL_FILE, index=False)
# Load face encodings
print("[INFO] loading encodings...")
with open("encodings.pickle", "rb") as f:
    data = pickle.loads(f.read())
known_face_encodings = data["encodings"]
known_face_names = data["names"]

# Camera setup
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1920, 1080)}))
picam2.start()

cv_scaler = 4
face_locations = []
face_encodings = []
face_names = []
frame_count = 0
start_time = time.time()
fps = 0
already_marked = set()
def process_frame(frame):
    global face_locations, face_encodings, face_names

    resized_frame = cv2.resize(frame, (0, 0), fx=(1 / cv_scaler), fy=(1 / cv_scaler))
    rgb_resized_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_resized_frame)
    face_encodings = face_recognition.face_encodings(rgb_resized_frame, face_locations, model='large')

    face_names = []

    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            if name not in already_marked:
                speak(f"Hello {name}")
                lecture = get_lecture_name_combined(name)
                if lecture:
                    mark_attendance(name, lecture)
                    speak("Attendance marked successfully. Have a nice day.")
                    already_marked.add(name)
        else:
            speak("Unknown person. I don't want to mark attendance. Thank you. Have a nice day.")

        face_names.append(name)

    return frame

def draw_results(frame):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= cv_scaler
        right *= cv_scaler
        bottom *= cv_scaler
        left *= cv_scaler

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 255), 2)
        cv2.rectangle(frame, (left, top - 30), (right, top), (0, 255, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name, (left + 6, top - 6), font, 0.7, (0, 0, 0), 1)
    return frame

def calculate_fps():
    global frame_count, start_time, fps
    frame_count += 1
    elapsed_time = time.time() - start_time
    if elapsed_time > 1:
        fps = frame_count / elapsed_time
        frame_count = 0
        start_time = time.time()
    return fps
while True:
    frame = picam2.capture_array()
    processed_frame = process_frame(frame)
    display_frame = draw_results(processed_frame)

    current_fps = calculate_fps()
    cv2.putText(display_frame, f"FPS: {current_fps:.1f}", (display_frame.shape[1] - 150, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('Smart Attendance System', display_frame)

    if cv2.waitKey(1) == ord("q"):
        break

cv2.destroyAllWindows()
picam2.stop()