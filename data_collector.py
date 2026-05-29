import cv2
import csv
import mediapipe as mp

# ĐỊNH NGHĨA TRỰC TIẾP (Bỏ qua mp.solutions)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Khởi tạo mô hình
hand_model = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5
)

cap = cv2.VideoCapture(0)
label = "C" 
count = 0
collecting = False

print("--- PHIEN BAN SUA LOI CHO PYTHON 3.12 ---")
print(f"Chuan bi thu thap chu: {label}")
print("Nhan 'S' de bat dau, 'Q' de thoat.")

while count < 200:
    ret, frame = cap.read()
    if not ret: break
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Xử lý ảnh
    results = hand_model.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Vẽ thủ công
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            
            if collecting:
                # Lưu tọa độ
                data = [label]
                for lm in hand_landmarks.landmark:
                    data.extend([lm.x, lm.y, lm.z])
                
                with open("vsl_data.csv", "a", newline="") as f:
                    csv.writer(f).writerow(data)
                
                count += 1
                cv2.putText(frame, f"Saved: {count}/200", (50, 80), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("VSL Collector 3.12 Fix", frame)
    key = cv2.waitKey(1)
    if key == ord('s'): 
        collecting = True
    if key == ord('q'): break

cap.release()
cv2.destroyAllWindows()