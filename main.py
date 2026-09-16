import cv2
import mediapipe as mp
import joblib
import time
import warnings

# --- 1. IMPORT YOUR SEPARATE CUSTOM MODULES ---
from TTS.model import speak
from SLI.model import extract_and_predict

warnings.filterwarnings("ignore", category=UserWarning)

# Load machine learning assets
model = joblib.load("asl_model.pkl")
scaler = joblib.load("asl_scaler.pkl")

# Setup MediaPipe framework
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Open webcam capture
cap = cv2.VideoCapture(0)

# Settings and UI state trackers
confidence_threshold = 0.75
spelled_text = ""
last_char = ""
last_added_time = 0
cooldown_seconds = 2

while True:
    ret, frame = cap.read()
    if not ret:
        break

    img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for handLms in result.multi_hand_landmarks:
            
            # --- 2. CALL YOUR SEPARATED PREDICTION MODULE ---
            pred_char, confidence, box = extract_and_predict(
                handLms, frame, scaler, model, confidence_threshold
            )

            # If a valid hand layout was fully calculated
            if pred_char and confidence >= confidence_threshold:
                current_time = time.time()
                
                # Typing manager gatekeeper checks
                if (pred_char != last_char) or (current_time - last_added_time >= cooldown_seconds):
                    if pred_char.lower() == "del":
                        spelled_text = spelled_text[:-1]
                        speak("delete")  # <-- Triggering your imported speak function
                    elif pred_char.lower() == "space":
                        spelled_text += " "
                        speak("space")   # <-- Triggering your imported speak function
                    else:
                        spelled_text += pred_char
                        speak(pred_char) # <-- Triggering your imported speak function
                        
                    last_char = pred_char
                    last_added_time = current_time

                # Draw prediction text at the calculated boundary box coordinates
                x_min, x_max, y_min, y_max = box
                cv2.putText(frame, f'{pred_char} ({confidence:.2f})',
                            (x_min, y_max + 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (0, 255, 0), 2)

            # Overlay hand skeleton visuals onto camera frame
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

    # Render sentence text bar across top header
    cv2.putText(frame, f'Spelled: {spelled_text}', (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 0, 0), 3)

    cv2.imshow("ASL Detection Panel", frame)
    
    # Check keystrokes
    key = cv2.waitKey(1) & 0xFF
    if key == 27: # Exit on Escape key
        break
    elif key == ord('s'): # Read the whole built sentence out loud when typing 'S'
        speak(spelled_text)

# Release physical stream assets safely
cap.release()
cv2.destroyAllWindows()
