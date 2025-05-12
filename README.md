# Smart Attendance System with Face Recognition and Audio Feedback 🎓🔊

This project implements an AI-powered **Smart Attendance System** using **Raspberry Pi 4**, capable of recognizing faces in real-time, marking attendance in an Excel sheet, and giving **instant audio feedback**.

## 🚀 Features

- Real-time face detection and recognition using PiCamera
- Attendance logging in Excel (.xlsx) using `openpyxl`
- Audio confirmation for attendance status (present/absent) using `pyttsx3` or `gTTS`
- Offline or online text-to-speech support
- Compact and hardware-efficient design

## 🧩 Hardware Components

- **Raspberry Pi 4** – Core processor
- **PiCamera** – Captures facial images
- **Speaker** – Delivers audio feedback
- **SSD / MicroSD Card** – Stores OS, code, and face encodings
- **Power Supply & Cables** – Required for proper operation

## 🖥️ Software & Libraries

- **Raspberry Pi OS**
- **Python 3**
- **OpenCV** – For live video and image processing
- **face_recognition** – For facial encoding and matching
- **openpyxl** – For Excel (.xlsx) file handling
- **pyttsx3 / gTTS** – For text-to-speech feedback

## 📂 Directory Structure

smart-attendance-system/
├── attendance.xlsx # Excel sheet to store attendance logs
├── dataset/ # Folder containing sample student images
├── main.py # Main Python script
├── requirements.txt # Required Python libraries
├── README.md # Project readme
└── utils/ # Additional helper scripts (e.g., audio, recognition)


## ⚙️ Setup Instructions

1. **Clone this repository**
   ```bash
   git clone https://github.com/your-username/smart-attendance-system.git
   cd smart-attendance-system
Install Dependencies

pip install -r requirements.txt
Collect Facial Data

Add clear front-facing images to the dataset/ folder. Use file names as student names.

Run the System


python3 main.py
🔊 Audio Feedback Options
Offline (Recommended): pyttsx3 for local text-to-speech

Online: gTTS for Google TTS (requires internet)

📈 Sample Output

[INFO] Recognizing...
[RECOGNIZED] John Mrigank Jaiswal as present
[VOICE] "Mrigank Jaiswal, your attendance has been marked"

📌 Use Cases
Smart classroom attendance
Office check-ins
Lab access logging
Secure event registration

🙌 Acknowledgements
OpenCV

face_recognition by Adam Geitgey

gTTS

pyttsx3

✅ Built as a part of my academic and personal learning journey in IoT, Computer Vision, and Python-based embedded systems.

