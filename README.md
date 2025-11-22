# 🐕 Dog Bark Detection System

ระบบวิเคราะห์เสียงหมาเห่าด้วย AI ที่มีประสิทธิภาพสูง รองรับไฟล์เสียงหลากหลายรูปแบบและความยาว พร้อมการดาวน์โหลดจาก Google Drive

A high-performance AI-powered dog bark detection system that analyzes audio files to identify when and where dog barks occur. Supports multiple audio formats, long files, and Google Drive integration.

## ✨ คุณสมบัติหลัก (Features)

- 🎯 **ความแม่นยำสูง**: ใช้ YAMNet model จาก Google (pre-trained on AudioSet) ที่สามารถตรวจจับเสียงหมาเห่าได้แม่นยำ
- 📁 **รองรับหลายรูปแบบ**: MP3, WAV, FLAC, OGG, M4A และอื่นๆ
- ⏱️ **ประมวลผลไฟล์ยาว**: แบ่งการประมวลผลเป็นส่วนย่อย (chunking) สำหรับไฟล์เสียงที่มีความยาวมาก
- 📍 **ระบุช่วงเวลาแม่นยำ**: บอกเวลาเริ่มต้นและสิ้นสุดของเสียงหมาเห่าแต่ละครั้ง
- ☁️ **Google Drive Support**: ดาวน์โหลดและวิเคราะห์ไฟล์จาก Google Drive ได้โดยตรง
- 📊 **รายงานผลละเอียด**: แสดงสถิติและสรุปผลการตรวจจับ
- 💾 **Export เป็น JSON**: บันทึกผลลัพธ์เป็นไฟล์ JSON สำหรับการวิเคราะห์ต่อ

## 🚀 การติดตั้ง (Installation)

### ข้อกำหนดของระบบ (Requirements)

- Python 3.8 หรือสูงกว่า
- ffmpeg (สำหรับการแปลงไฟล์เสียง)

### ติดตั้ง ffmpeg

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
ดาวน์โหลดจาก [https://ffmpeg.org/](https://ffmpeg.org/)

### ติดตั้ง Python Dependencies

```bash
# Clone repository
git clone <repository-url>
cd 2025-11-22-home-dog

# สร้าง virtual environment (แนะนำ)
python -m venv venv
source venv/bin/activate  # Linux/macOS
# หรือ
venv\Scripts\activate  # Windows

# ติดตั้ง dependencies
pip install -r requirements.txt
```

## 📖 วิธีการใช้งาน (Usage)

### การใช้งานพื้นฐาน

```bash
# วิเคราะห์ไฟล์เสียงในเครื่อง
python detect_bark.py my_audio.mp3

# วิเคราะห์ไฟล์จาก Google Drive
python detect_bark.py "https://drive.google.com/file/d/YOUR_FILE_ID/view"
```

### ตัวเลือกขั้นสูง

```bash
# ปรับค่า confidence threshold (0.0-1.0)
python detect_bark.py audio.wav --confidence 0.4

# กำหนดระยะเวลาสำหรับรวมการตรวจจับที่อยู่ใกล้กัน
python detect_bark.py audio.mp3 --merge-gap 2.0

# ปรับขนาด chunk สำหรับไฟล์ยาว (วินาที)
python detect_bark.py long_audio.mp3 --chunk-size 120

# บันทึกผลลัพธ์เป็น JSON
python detect_bark.py audio.mp3 --output results.json

# ไม่รวมการตรวจจับที่อยู่ใกล้กัน
python detect_bark.py audio.mp3 --no-merge

# ใช้ GPU (ถ้ามี)
python detect_bark.py audio.mp3 --gpu
```

### ดูตัวเลือกทั้งหมด

```bash
python detect_bark.py --help
```

## 📊 ตัวอย่างผลลัพธ์ (Output Example)

```
================================================================================
Found 3 dog bark event(s):
================================================================================

[Event #1]
  Time: 00:00:12.480 - 00:00:14.400
  Duration: 1.92 seconds
  Confidence: 87.45%
  Type: Bark

[Event #2]
  Time: 00:01:05.760 - 00:01:08.160
  Duration: 2.40 seconds
  Confidence: 92.31%
  Type: Bow-wow

[Event #3]
  Time: 00:02:33.120 - 00:02:34.560
  Duration: 1.44 seconds
  Confidence: 78.92%
  Type: Bark

================================================================================

Summary Statistics:
  Total events: 3
  Total duration of barking: 5.76 seconds
  Average event duration: 1.92 seconds
  Average confidence: 86.23%
  Confidence range: 78.92% - 92.31%
```

## 🏗️ โครงสร้างโปรเจค (Project Structure)

```
2025-11-22-home-dog/
├── dog_bark_detector/           # Main package
│   ├── __init__.py              # Package initialization
│   ├── detector.py              # YAMNet-based dog bark detector
│   ├── audio_processor.py       # Audio file processing utilities
│   └── gdrive_downloader.py     # Google Drive file downloader
├── tests/                       # Test suite
│   ├── __init__.py              # Test package initialization
│   ├── test_installation.py     # Installation verification tests
│   ├── test_gdrive.py           # Google Drive functionality tests
│   ├── test_gdrive_simple.py    # Simple URL parsing tests
│   ├── test_real_gdrive.py      # Real download tests
│   ├── test_download_large.py   # Large file download tests
│   └── README.md                # Test documentation
├── detect_bark.py               # Main script
├── pytest.ini                   # Pytest configuration
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🔧 การใช้งานเป็น Library

คุณสามารถใช้โปรเจคนี้เป็น library ในโค้ดของคุณได้:

```python
from dog_bark_detector import DogBarkDetector, AudioProcessor

# Initialize
detector = DogBarkDetector(confidence_threshold=0.3)
audio_processor = AudioProcessor(sample_rate=16000)

# Load and process audio
audio, sr = audio_processor.load_audio('my_audio.mp3')
detections = detector.detect_in_waveform(audio, sample_rate=sr)

# Print results
detector.print_detections(detections)

# Get summary
summary = detector.get_detection_summary(detections)
print(f"Total events: {summary['total_events']}")
```

### ประมวลผลไฟล์ยาวแบบ chunks

```python
from dog_bark_detector import DogBarkDetector, AudioProcessor

detector = DogBarkDetector(confidence_threshold=0.3)
audio_processor = AudioProcessor()

all_detections = []

# Process in 60-second chunks
for audio_chunk, start_time, end_time in audio_processor.process_in_chunks(
        'long_audio.mp3', chunk_duration=60.0):

    detections = detector.detect_in_waveform(audio_chunk)

    # Adjust timestamps
    for d in detections:
        d['start_time'] += start_time
        d['end_time'] += start_time

    all_detections.extend(detections)

# Merge nearby detections
merged = detector.merge_detections(all_detections, merge_gap=1.0)
detector.print_detections(merged)
```

### ดาวน์โหลดจาก Google Drive

```python
from dog_bark_detector import GDriveDownloader

gdrive = GDriveDownloader()

# Download from Google Drive
file_path = gdrive.download_file(
    'https://drive.google.com/file/d/YOUR_FILE_ID/view',
    'downloaded_audio.mp3'
)

# Or use convenience method
file_path = gdrive.download_if_gdrive(
    'https://drive.google.com/file/d/YOUR_FILE_ID/view',
    output_dir='./downloads'
)
```

## ⚙️ การปรับแต่ง (Configuration)

### Confidence Threshold

- **ค่าต่ำ (0.1-0.2)**: ตรวจจับได้มากขึ้นแต่อาจมี false positives
- **ค่ากลาง (0.3-0.4)**: สมดุลระหว่างความแม่นยำและการตรวจจับ (แนะนำ)
- **ค่าสูง (0.5-0.8)**: แม่นยำมากแต่อาจพลาดบางเสียง

### Merge Gap

- กำหนดว่าการตรวจจับที่อยู่ห่างกันเท่าไรจะถูกรวมเป็นเหตุการณ์เดียวกัน
- ค่าที่แนะนำ: 1.0-2.0 วินาที

### Chunk Size

- สำหรับไฟล์ยาว ควรใช้ chunk size ที่เหมาะสม
- ค่าที่แนะนำ: 60-120 วินาที
- Chunk ใหญ่ = ใช้ RAM มากขึ้น แต่ประมวลผลเร็วกว่า

## 🧠 เทคโนโลยีที่ใช้ (Technology Stack)

- **YAMNet**: Google's audio event classification model (trained on AudioSet)
- **TensorFlow & TensorFlow Hub**: Deep learning framework
- **Librosa**: Audio analysis library
- **Pydub**: Audio file manipulation
- **NumPy**: Numerical computing

## 📝 หมายเหตุ (Notes)

1. **Model Download**: ครั้งแรกที่รันโปรแกรม จะมีการดาวน์โหลด YAMNet model (~13MB) อัตโนมัติ
2. **Audio Formats**: รองรับทุกรูปแบบที่ ffmpeg รองรับ
3. **Processing Time**: ขึ้นอยู่กับความยาวของไฟล์และสเปกของเครื่อง โดยทั่วไปใช้เวลาประมาณ 1-2 วินาทีต่อนาทีของเสียง
4. **Google Drive**: สามารถใช้ทั้ง sharing link และ direct link

## 🧪 การทดสอบ (Testing)

### ทดสอบการติดตั้ง

ตรวจสอบว่าระบบติดตั้งถูกต้องและพร้อมใช้งาน:
```bash
python tests/test_installation.py
```

### รัน Test Suite ทั้งหมด

```bash
# ติดตั้ง pytest (ถ้ายังไม่มี)
pip install pytest

# รัน tests ทั้งหมด
pytest

# รันแบบ verbose
pytest -v

# รัน test file เฉพาะ
pytest tests/test_gdrive.py
```

### Test Categories

- **test_installation.py**: ตรวจสอบการติดตั้งและ dependencies
- **test_gdrive.py**: ทดสอบการทำงานของ Google Drive downloader
- **test_gdrive_simple.py**: ทดสอบ URL parsing (ไม่ต้องใช้ dependencies)
- **test_real_gdrive.py**: ทดสอบการดาวน์โหลดจริงจาก Google Drive
- **test_download_large.py**: ทดสอบการดาวน์โหลดไฟล์ขนาดใหญ่

สำหรับข้อมูลเพิ่มเติม ดูที่ [tests/README.md](tests/README.md)

## 🐛 การแก้ปัญหา (Troubleshooting)

### ปัญหา: ImportError with librosa

```bash
pip install numba==0.56.4
pip install librosa --no-cache-dir
```

### ปัญหา: ffmpeg not found

ตรวจสอบว่าติดตั้ง ffmpeg แล้วและอยู่ใน PATH:
```bash
ffmpeg -version
```

### ปัญหา: TensorFlow GPU issues

ถ้าไม่มี GPU หรือมีปัญหากับ GPU ให้ใช้ CPU:
```bash
python detect_bark.py audio.mp3  # ไม่ต้องใส่ --gpu
```

### ปัญหา: Google Drive download fails

ลองใช้ gdown library แทน:
```bash
pip install gdown
```

## 📄 License

MIT License

## 👨‍💻 Author

Created with ❤️ by Claude AI

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.