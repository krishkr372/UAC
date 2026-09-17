from tkinter import ttk

import cv2
import mediapipe as mp
import joblib
import numpy as np
import time
import warnings
import serial  
import pyttsx3
import threading

warnings.filterwarnings("ignore", category=UserWarning)

# --- Text to speech function ---
def bg_speak(tts):
    """Run the speech engine in the background to prevent OpenCV window lag."""

    def worker():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 140)
            engine.say(tts)
            engine.runAndWait()
        except Exception as tts_err:
            print(f"[TTS] Error in background speecch: {tts_err}")
    threading.Thread(target=worker, daemon=True).start()
        
           
# --- ARDUINO CONFIGURATION ---
try:
    print("[OLED] Connecting to Arduino...")
    arduino = serial.Serial('COM4', 9600, timeout=0.1)
    time.sleep(3)  
    print("[OLED] Arduino connected successfully! Ready to send text.")
except Exception as e:
    print(f"[OLED] Connection failed: {e}. (Running without OLED hardware)")
    arduino = None

# Load model, scaler, and label encoder
model = joblib.load("sli_asl_model.pkl")
scaler = joblib.load("sli_asl_scaler.pkl")
label_encoder = joblib.load("sli_asl_label_encoder.pkl") 

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

confidence_threshold = 0.75
spelled_text = ""
last_char = ""
last_added_time = 0

# Cooldown delay in seconds
cooldown_seconds = 2

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    
    # --- VISUAL COOLDOWN CALCULATIONS ---
    time_elapsed = current_time - last_added_time
    
    if time_elapsed < cooldown_seconds:
        # System is locked: Calculate remaining time and progress bar width
        time_left = cooldown_seconds - time_elapsed
        progress = time_elapsed / cooldown_seconds
        bar_width = int(progress * 200) # Max width of 200 pixels
        
        status_text = f"LOCKED ({time_left:.1f}s)"
        status_color = (0, 0, 255) # Red for locked status
    else:
        # System is unlocked and ready
        bar_width = 200
        status_text = "READY FOR SIGN"
        status_color = (0, 255, 0) # Green for ready status

    # --- DRAW VISUAL TIMER INTERFACE ---
    # Draw Background Container Border
    cv2.rectangle(frame, (10, 70), (210, 95), (200, 200, 200), 2)
    # Draw Solid Progress Filling Bar
    if bar_width > 0:
        cv2.rectangle(frame, (10, 70), (10 + bar_width, 95), status_color, -1)
    # Put Status Text Label above the Progress Bar
    cv2.putText(frame, status_text, (10, 115),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, status_color, 2)

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            lm_list = []
            h, w, _ = frame.shape
            x_list, y_list = [], []

            for lm in handLms.landmark:
                x, y, z = lm.x, lm.y, lm.z
                lm_list.extend([x, y, z])
                x_list.append(int(x * w))
                y_list.append(int(y * h))

            if len(lm_list) == 63:
                lm_scaled = scaler.transform([lm_list])
                
                proba = model.predict_proba(lm_scaled)[0]
                pred_index = np.argmax(proba)
                
                # Decode the index back to the original label string
                pred_char = str(label_encoder.inverse_transform([pred_index])[0])
                confidence = proba[pred_index]

                if confidence >= confidence_threshold:
                    # Enforce the global cooldown between inputs
                    if time_elapsed >= cooldown_seconds:
                        if pred_char.lower() == "del":
                            spelled_text = spelled_text[:-1]
                            tts_phase = "Deleted last character."
                        elif pred_char.lower() == "space":
                            tts_phase = "Clear"
                            spelled_text = "" 
                        else:
                            spelled_text += pred_char
                            tts_phase = pred_char
                        last_char = pred_char
                        last_added_time = current_time


                        # --- STEP-BY-STEP TERMINAL MESSAGES ---
                        print(f"[ACTION] Detected Sign: '{pred_char}' | Current Word: '{spelled_text}'")


                        # --- STEP-BY-STEP TEXT-TO-SPEECH ---
                        if tts_phase:
                            bg_speak(tts_phase)

                            
                        # --- STEP-BY-STEP OLED TRANSMISSION ---
                        if arduino and arduino.is_open:
                            try:
                                arduino.write(f"{spelled_text}\n".encode('utf-8'))
                                print(f"[OLED] Successfully sent to screen: '{spelled_text}'")
                            except Exception as serial_err:
                                print(f"[OLED] Transmission error: {serial_err}")

                # Draw character prediction bounding box label
                x_min, x_max = min(x_list), max(x_list)
                y_min, y_max = min(y_list), max(y_list)
                cv2.putText(frame, f'{pred_char} ({confidence:.2f})',
                            (x_min, y_max + 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)

            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    # Display spelled text at top
    cv2.putText(frame, f'Spelled: {spelled_text}', (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)

    cv2.imshow("ASL Detection", frame)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
if arduino:
    arduino.close()
    print("[OLED] Connection safely closed.")
cv2.destroyAllWindows()
