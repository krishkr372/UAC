import cv2
import mediapipe as mp
import os
import csv 

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=True, max_num_hands=1)
data = []

dataset_path = "dataset/asl_alphabet_train/"

for label in os.listdir(dataset_path):
    label_path = os.path.join(dataset_path, label)
    if not os.path.isdir(label_path):
        continue
    print(f"Processing label: {label}")
    for img_file in os.listdir(label_path):
        img_path = os.path.join(label_path, img_file)
        image = cv2.imread(img_path)
        if image is None: 
            continue
        image_rgb = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            landmarks = []
            for landmark in hand_landmarks.landmark:
                landmarks.extend([landmark.x, landmark.y, landmark.z])
            landmarks.append(label)
            data.append(landmarks)  

with open("asl_hand_landmarks.csv" , "w" , newline='') as f:
    writer = csv.writer(f)
    header = [f"{axis}{i}" for i in range (21) for axis in ['x', 'y', 'z']] + ['label']
    writer.writerow(header)
    writer.writerows(data)

print("Saved")





