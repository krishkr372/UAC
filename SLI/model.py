import numpy as np

def extract_and_predict(hand_landmarks, frame, scaler, model, confidence_threshold=0.75):
    """
    Extracts 63 coordinates from a hand, normalizes them, and predicts the sign.
    Returns (predicted_char, confidence, boundary_box_coordinates) or (None, None, None)
    """
    lm_list = []
    h, w, _ = frame.shape
    x_list, y_list = [], []

    for lm in hand_landmarks.landmark:
        x, y, z = lm.x, lm.y, lm.z
        lm_list.extend([x, y, z])
        x_list.append(int(x * w))
        y_list.append(int(y * h))

    if len(lm_list) == 63:
        # Scale the extracted landmarks
        lm_scaled = scaler.transform([lm_list])
        
        # Run prediction
        proba = model.predict_proba(lm_scaled)[0]
        pred_index = np.argmax(proba)
        pred_char = str(model.classes_[pred_index])
        confidence = proba[pred_index]

        # Calculate bounding box coordinates for text drawing later
        box = (min(x_list), max(x_list), min(y_list), max(y_list))
        
        return pred_char, confidence, box
        
    return None, None, None
