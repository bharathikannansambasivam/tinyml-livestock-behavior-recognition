# live_behavior_detection.py

import cv2
import numpy as np
import tensorflow as tf
from collections import deque
import requests

# -----------------------
# SETTINGS
# -----------------------
MODEL_PATH = "behavior_model.tflite"

IMG_SIZE = 96
THRESHOLD = 0.55
SMOOTH_FRAMES = 5

labels = ["fence", "grazing", "background"]  # no_animal renamed

# -----------------------
# Load TFLite model
# -----------------------
interpreter = tf.lite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()

input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

print("✅ TinyML model loaded")

# -----------------------
# Camera
# -----------------------
cap = cv2.VideoCapture(0)

history = deque(maxlen=SMOOTH_FRAMES)

# -----------------------
# MAIN LOOP
# -----------------------
while True:

    ret, frame = cap.read()
    if not ret:
        continue

    img = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    img = img.astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)

    interpreter.set_tensor(input_details[0]['index'], img)
    interpreter.invoke()

    pred = interpreter.get_tensor(output_details[0]['index'])[0]

    idx = np.argmax(pred)
    conf = float(pred[idx])

    history.append(idx)
    stable_idx = max(set(history), key=history.count)

    behavior = labels[stable_idx]
    confidence = round(conf * 100, 2)

    # -----------------------
    # Logic
    # -----------------------
    if behavior == "background" or conf < THRESHOLD:
        behavior = "No Animal"
        status = "None"
        color = (180, 180, 180)

    elif behavior == "fence":
        status = "ALERT"
        color = (0, 0, 255)

    else:
        status = "Safe"
        color = (0, 255, 0)

    # -----------------------
    # Send to backend (optional)
    # -----------------------
    try:
        requests.post(
            "http://localhost:5000/update",
            json={
                "animal": "Livestock" if behavior != "No Animal" else "None",
                "behavior": behavior,
                "confidence": confidence,
                "status": status
            },
            timeout=0.2
        )
    except:
        pass

    # -----------------------
    # Draw UI
    # -----------------------
    cv2.putText(frame, f"Behavior: {behavior}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    cv2.putText(frame, f"Confidence: {confidence}%", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.putText(frame, f"Status: {status}", (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

    cv2.imshow("TinyML Behavior Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
