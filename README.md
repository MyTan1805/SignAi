# 🤟 VSL Learning - Học Ngôn Ngữ Ký Hiệu Việt Nam

Ứng dụng web học ngôn ngữ ký hiệu thông qua camera, sử dụng AI để đánh giá động tác của người dùng.

## 🛠️ Cài đặt

### Yêu cầu
- Python 3.11
- Webcam

### Các bước

**1. Clone repo**
```bash
git clone https://github.com/MyTan1805/TEN_REPO.git
cd TEN_REPO
```

**2. Tạo môi trường ảo**
```bash
py -3.11 -m venv venv
venv\Scripts\activate
```

**3. Cài thư viện**
```bash
pip install mediapipe==0.10.14 opencv-python flask scikit-learn pandas numpy
```

## 📦 Thu thập dữ liệu

Chạy `data_collector.py` cho từng chữ cái. Mỗi chữ cần **200 mẫu**.

```bash
python data_collector.py
```

- Nhấn `S` để bắt đầu thu thập
- Nhấn `Q` để thoát
- Thay `label = "A"` thành `"B"`, `"C"`,... cho các chữ tiếp theo

## 🧠 Train model

Sau khi thu thập đủ data:

```bash
python train_model.py
```

Sẽ tạo ra 2 file:
- `vsl_model.pkl`
- `vsl_label_encoder.pkl`

## 🚀 Chạy ứng dụng

```bash
python app.py
```

Mở trình duyệt vào **http://localhost:5000**

## 📁 Cấu trúc project
SignAi/
├── app.py                  # Flask web app
├── data_collector.py       # Thu thập dữ liệu
├── train_model.py          # Huấn luyện model
├── templates/
│   └── index.html          # Giao diện web
├── requirements.txt
└── README.md

## 🗺️ Roadmap

- [x] Thu thập data
- [x] Train AI
- [x] Real-time nhận diện
- [x] Hệ thống bài học
- [ ] Database lưu tiến độ
- [ ] Thêm nhiều chữ cái
- [ ] Deploy lên server
Tạo thêm requirements.txt để người khác cài cho tiện:
mediapipe==0.10.14
opencv-python
flask
scikit-learn
pandas
numpy
Tạo file bằng lệnh:
powershellNew-Item README.md
New-Item requirements.txt
Rồi copy nội dung vào, sau đó:
powershellgit add .
git commit -m "add README and requirements"
git push