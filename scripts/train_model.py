# train_model.py - thêm normalize
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle

def normalize_landmarks(landmarks):
    """Chuẩn hóa tọa độ theo wrist (điểm 0) để không phụ thuộc vị trí tay"""
    landmarks = np.array(landmarks).reshape(21, 3)
    
    # Lấy wrist làm gốc tọa độ
    wrist = landmarks[0]
    landmarks -= wrist
    
    # Scale theo khoảng cách lớn nhất để không phụ thuộc kích thước tay
    scale = np.max(np.abs(landmarks))
    if scale > 0:
        landmarks /= scale
    
    return landmarks.flatten().tolist()

print("Đang đọc dữ liệu...")
df = pd.read_csv("data/vsl_data.csv", header=None)

X_raw = df.iloc[:, 1:].values
y = df.iloc[:, 0].values

# ── NORMALIZE ──
print("Đang normalize...")
X = np.array([normalize_landmarks(row) for row in X_raw])

print(f"Tổng mẫu: {len(X)} | Nhãn: {sorted(set(y))}")

le = LabelEncoder()
y_encoded = le.fit_transform(y)

X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print("Đang huấn luyện...")
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=15,
    min_samples_leaf=3,   # tránh overfit
    random_state=42,
    n_jobs=-1
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\n✅ Độ chính xác: {acc*100:.1f}%")
print(classification_report(y_test, y_pred, target_names=le.classes_))

with open("models/vsl_model.pkl", "wb") as f:
    pickle.dump(model, f)
with open("models/vsl_label_encoder.pkl", "wb") as f:
    pickle.dump(le, f)

print("🎉 Đã lưu model!")