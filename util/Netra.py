import cv2
import os
import random
import cv2
from ultralytics import YOLO
import threading
from playsound import playsound
import math
from gtts import gTTS
import time
from datetime import datetime
import requests

# State
tabungan = {}
tanggal = datetime.now().strftime("%d/%m/%y")
tabungan[f"{tanggal}"] = 0
uangSekarang = 0

classNames = [
    {
        "nominal": 100000,
        "class": "100rb"
    },
    {
        "nominal": 10000,
        "class": "10rb"
    },
    {
        "nominal": 1000,
        "class": "1rb"
    },
    {
        "nominal": 20000,
        "class": "20rb"
    },
    {
        "nominal": 2000,    
        "class": "2rb"
    },
    {
        "nominal": 50000,
        "class": "50rb"
    },
    {
        "nominal": 5000,
        "class": "5rb"
    }
]

model = YOLO('model/best_2.pt')

def play_audio(file):
    threading.Thread(target=lambda: playsound(file), daemon=True).start()
    
def scan(frame):
    play_audio("audio/wait.mp3")
    time.sleep(1)
    if not os.path.exists("captured_images"):
        os.makedirs("captured_images")
    
    # Save a random image for YOLO detection
    rnd = random.randint(1, 5)
    image_path = f"captured_images/img_{rnd}.jpg"
    cv2.imwrite(image_path, frame)
    print(f"Image saved as {image_path}")

    # Run YOLO detection on the image
    results = model([f"captured_images/img_{rnd}.jpg"]) 

    detection_found = False  # Flag to track if any detection is found

    for r in results:
        print("=========DETECTION==========")
        print(r.boxes)
        
        # Check if there are no boxes (i.e., no detections)
        if r.boxes is None or len(r.boxes) == 0:
            print("No detection")
            play_audio("audio/ulang.mp3")  # Play ulang.mp3 if nothing is detected
            continue
        
        # If we found any boxes, process them
        for box in r.boxes:
            detection_found = True  # Set flag to True as detection is found
            confidence = math.ceil((box.conf[0] * 100)) / 100
            print("Confidence --->", confidence)
            cls = int(box.cls[0])
            print(cls)
            play_audio(f"audio/{classNames[cls]['class']}.mp3")  # Play audio for detected class
            global uangSekarang
            uangSekarang=classNames[cls]["nominal"]

    # If no detection was found at all, play ulang.mp3
    if not detection_found:
        play_audio("audio/ulang.mp3")

    return f"captured_images/img_{rnd}.jpg"


def generateSuara(text):
    sound_filename=random.randint(1,20)
    gTTS(text,lang="id").save(f"audio/temp/audio_{sound_filename}.mp3")
    play_audio(f"audio/temp/audio_{sound_filename}.mp3")
    return f"audio/temp/audio_{sound_filename}.mp3"

def tabung():
    tanggal = datetime.now().strftime("%d/%m/%y")
    global tabungan
    tabungan[f"{tanggal}"] += uangSekarang
    generateSuara(f'Uang kamu {uangSekarang} dimasukkan ke tabungan, Total tabungan kamu hari ini adalah {tabungan[f"{tanggal}"]} Rupiah')
    return 0


def laporan():
    generateSuara(f"Laporan Tabungan Kamu")
    msg = "Laporan TABITA (Tabungan Bicara Tunanetra)\n"
    for date in tabungan:
        print(date,tabungan[date])
        msg += f"Tanggal {date} : Rp{tabungan[date]}\n"

    TelegramSendMessage(msg)
    return 0


def TelegramSendMessage(message):
    bot_token = '7349734127:AAHe2XD-2dblK9BtAlZllgEWDa2zUFwyt8U'
    chat_id = '534911718'
    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    params = {
        'chat_id': chat_id,
        'text': message,
        'parse_mode': 'Markdown' 
    }
    response = requests.get(send_message_url, params=params)
    if response.status_code == 200:
        print('Message sent successfully!')
    else:
        print('Failed to send message.')
