# 🤟 VSL Learning

Ứng dụng web học **Ngôn Ngữ Ký Hiệu Việt Nam** qua camera, sử dụng AI nhận diện động tác tay theo thời gian thực.

---

## ✨ Tính năng

- 📷 Nhận diện ký hiệu tay qua webcam
- 🧠 AI đánh giá độ chính xác động tác
- 📚 Hệ thống bài học từng bước
- ✅ Tự động qua bài khi giữ đúng tư thế 2 giây

---

## 🖥️ Demo

> Coming soon

---

## 📁 Cấu trúc project

```
SignAi/
├── app.py                  # Flask entry point
├── requirements.txt
├── README.md
│
├── core/                   # Logic AI
│   ├── model.py
│   └── collector.py
│
├── data/                   # Dữ liệu training
│   └── vsl_data.csv
│
├── models/                 # Model đã train
│   ├── vsl_model.pkl
│   └── vsl_label_encoder.pkl
│
├── scripts/                # Script tiện ích
│   ├── train_model.py
│   └── check_data.py
│
└── templates/
    └── index.html
```

---

## ⚙️ Cài đặt

### Yêu cầu
- Python 3.11
- Webcam

### Các bước

```bash
# 1. Clone repo
git clone https://github.com/MyTan1805/SignAi.git
cd SignAi

# 2. Tạo môi trường ảo
py -3.11 -m venv venv
venv\Scripts\activate

# 3. Cài thư viện
pip install -r requirements.txt
```

---

## 🗂️ Thu thập dữ liệu

```bash
python core/collector.py
```

- Nhấn `S` để bắt đầu thu thập
- Nhấn `Q` để dừng
- Thay `label = "A"` thành `"B"`, `"C"`... cho từng chữ
- Mỗi chữ cần tối thiểu **200 mẫu**

---

## 🧠 Train model

```bash
python scripts/train_model.py
```

Tạo ra 2 file trong `models/`:
- `vsl_model.pkl`
- `vsl_label_encoder.pkl`

---

## 🚀 Chạy ứng dụng

```bash
python app.py
```

Mở trình duyệt: **http://localhost:5000**

---

## 🗺️ Roadmap

- [x] Thu thập data
- [x] Train AI
- [x] Nhận diện real-time
- [x] Hệ thống bài học
- [ ] Database lưu tiến độ người dùng
- [ ] Thêm toàn bộ bảng chữ cái
- [ ] Deploy lên server

---

## 🛠️ Tech Stack

| | Công nghệ |
|---|---|
| Backend | Python, Flask |
| AI / ML | MediaPipe, Scikit-learn |
| Frontend | HTML, CSS, JavaScript |
| Computer Vision | OpenCV |

---

## 👤 Tác giả

**Quach My Tan** — [@MyTan1805](https://github.com/MyTan1805)