from flask import Flask, render_template, Response, jsonify, request
import cv2
import mediapipe as mp
import pickle
import numpy as np
import time

app = Flask(__name__)

with open("vsl_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vsl_label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

# ── TRẠNG THÁI BÀI HỌC ──
LESSONS = [
    {"id": 1, "sign": "A", "title": "Chữ A", "description": "Nắm tay, ngón cái đặt bên cạnh"},
    {"id": 2, "sign": "B", "title": "Chữ B", "description": "Bốn ngón tay thẳng, ngón cái gập vào"},
    {"id": 3, "sign": "C", "title": "Chữ C", "description": "Bàn tay cong hình chữ C"},
]

state = {
    "current_lesson": 0,       # index trong LESSONS
    "prediction": "",
    "confidence": 0,
    "hold_start": None,         # thời điểm bắt đầu giữ đúng tư thế
    "hold_duration": 0,         # đã giữ bao lâu (giây)
    "passed": False,            # đã qua bài chưa
    "completed_lessons": []     # các bài đã hoàn thành
}

HOLD_REQUIRED = 2.0  # giữ đúng 2 giây mới qua

def normalize_landmarks(landmarks):
    landmarks = np.array(landmarks).reshape(21, 3)
    wrist = landmarks[0]
    landmarks -= wrist
    scale = np.max(np.abs(landmarks))
    if scale > 0:
        landmarks /= scale
    return landmarks.flatten().tolist()

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret: break

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                landmarks = []
                for lm in hand_landmarks.landmark:
                    landmarks.extend([lm.x, lm.y, lm.z])

                landmarks_normalized = normalize_landmarks(landmarks)
                prediction = model.predict([landmarks_normalized])[0]
                confidence = model.predict_proba([landmarks_normalized])[0].max()
                label = le.inverse_transform([prediction])[0]

                state["prediction"] = label
                state["confidence"] = round(float(confidence) * 100, 1)

                # ── LOGIC GIỮ TƯ THẾ ──
                current_sign = LESSONS[state["current_lesson"]]["sign"]
                if label == current_sign and confidence > 0.8 and not state["passed"]:
                    if state["hold_start"] is None:
                        state["hold_start"] = time.time()
                    state["hold_duration"] = round(time.time() - state["hold_start"], 1)
                    if state["hold_duration"] >= HOLD_REQUIRED:
                        state["passed"] = True
                        if state["current_lesson"] not in state["completed_lessons"]:
                            state["completed_lessons"].append(state["current_lesson"])
                else:
                    state["hold_start"] = None
                    state["hold_duration"] = 0
        else:
            state["prediction"] = ""
            state["hold_start"] = None
            state["hold_duration"] = 0

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/state')
def get_state():
    lesson = LESSONS[state["current_lesson"]]
    return jsonify({
        "prediction": state["prediction"],
        "confidence": state["confidence"],
        "hold_duration": state["hold_duration"],
        "hold_required": HOLD_REQUIRED,
        "passed": state["passed"],
        "current_lesson": lesson,
        "completed_lessons": state["completed_lessons"],
        "total_lessons": len(LESSONS)
    })

@app.route('/next_lesson', methods=['POST'])
def next_lesson():
    if state["current_lesson"] < len(LESSONS) - 1:
        state["current_lesson"] += 1
        state["passed"] = False
        state["hold_start"] = None
        state["hold_duration"] = 0
    return jsonify({"ok": True})

if __name__ == '__main__':
    app.run(debug=True)