import cv2
import mediapipe as mp
import pickle
import numpy as np
import time

# --- LOAD MODEL ---
with open("vsl_model.pkl", "rb") as f:
    model = pickle.load(f)
with open("vsl_label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

# --- SETUP MEDIAPIPE ---
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.7)

def normalize_landmarks(landmarks):
    landmarks = np.array(landmarks).reshape(21, 3)
    wrist = landmarks[0]
    landmarks -= wrist
    scale = np.max(np.abs(landmarks))
    if scale > 0: landmarks /= scale
    return landmarks.flatten().tolist()

# --- LOGIC BÀI HỌC ---
syllabus = ["A", "B", "C"]  # Danh sách các chữ cần học
current_lesson_idx = 0
correct_frames_counter = 0  # Đếm số khung hình làm đúng liên tiếp
REQUIRED_FRAMES = 20        # Cần khoảng 20 khung hình (~1 giây) để xác nhận

cap = cv2.VideoCapture(0)

while current_lesson_idx < len(syllabus):
    target_letter = syllabus[current_lesson_idx]
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    # Hiển thị yêu cầu bài học
    cv2.rectangle(frame, (0, 0), (w, 100), (255, 255, 255), -1)
    cv2.putText(frame, f"Hay lam chu: {target_letter}", (50, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 0), 3)

    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            landmarks = []
            for lm in hand_landmarks.landmark:
                landmarks.extend([lm.x, lm.y, lm.z])

            # Dự đoán
            ln_norm = normalize_landmarks(landmarks)
            prediction = model.predict([ln_norm])[0]
            label = le.inverse_transform([prediction])[0]
            confidence = model.predict_proba([ln_norm])[0].max()

            # Kiểm tra xem có đúng chữ đang yêu cầu không
            if label == target_letter and confidence > 0.8:
                correct_frames_counter += 1
                color = (0, 255, 0)
            else:
                correct_frames_counter = 0
                color = (0, 0, 255)

            # Vẽ thanh tiến trình (Progress Bar)
            progress_width = int((correct_frames_counter / REQUIRED_FRAMES) * w)
            cv2.rectangle(frame, (0, h-20), (progress_width, h), (0, 255, 0), -1)

            if correct_frames_counter >= REQUIRED_FRAMES:
                print(f"Chinh xac! Da vuot qua chu {target_letter}")
                current_lesson_idx += 1
                correct_frames_counter = 0
                time.sleep(1) # Nghỉ 1 giây trước khi sang chữ mới

    cv2.imshow("VSL Learning Mode", frame)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()
print("Chuc mung! Ban da hoan thanh khoa hoc co ban!")