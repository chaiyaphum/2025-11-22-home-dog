# 🚀 Quick Start Guide

เริ่มต้นใช้งานระบบตรวจจับเสียงหมาเห่าใน 5 นาที!

## ขั้นตอนที่ 1: ติดตั้ง

```bash
# 1. Clone repository
git clone <repository-url>
cd 2025-11-22-home-dog

# 2. สร้าง virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# หรือ venv\Scripts\activate สำหรับ Windows

# 3. ติดตั้ง dependencies
pip install -r requirements.txt

# 4. ติดตั้ง ffmpeg (ถ้ายังไม่มี)
# Ubuntu/Debian: sudo apt-get install ffmpeg
# macOS: brew install ffmpeg
# Windows: ดาวน์โหลดจาก https://ffmpeg.org/
```

## ขั้นตอนที่ 2: ทดสอบการติดตั้ง

```bash
python test_installation.py
```

คุณควรเห็นข้อความ "✓ All tests passed!"

## ขั้นตอนที่ 3: ใช้งาน

### วิธีที่ 1: ไฟล์เสียงในเครื่อง

```bash
python detect_bark.py your_audio.mp3
```

### วิธีที่ 2: ไฟล์จาก Google Drive

```bash
python detect_bark.py "https://drive.google.com/file/d/YOUR_FILE_ID/view"
```

### วิธีที่ 3: กำหนดค่าต่างๆ

```bash
# ปรับความไว (0.0-1.0, default: 0.3)
python detect_bark.py audio.mp3 --confidence 0.4

# บันทึกผลลัพธ์
python detect_bark.py audio.mp3 --output results.json

# ไฟล์ยาว (ปรับขนาด chunk)
python detect_bark.py long_audio.mp3 --chunk-size 120
```

## ตัวอย่างผลลัพธ์

```
================================================================================
Found 2 dog bark event(s):
================================================================================

[Event #1]
  Time: 00:00:15.360 - 00:00:17.280
  Duration: 1.92 seconds
  Confidence: 85.23%
  Type: Bark

[Event #2]
  Time: 00:01:23.040 - 00:01:25.440
  Duration: 2.40 seconds
  Confidence: 91.47%
  Type: Bow-wow
```

## การใช้งานในโค้ด Python

```python
from dog_bark_detector import DogBarkDetector, AudioProcessor

# Initialize
detector = DogBarkDetector(confidence_threshold=0.3)
audio_processor = AudioProcessor(sample_rate=16000)

# Load and detect
audio, sr = audio_processor.load_audio('audio.mp3')
detections = detector.detect_in_waveform(audio, sample_rate=sr)

# Show results
detector.print_detections(detections)
```

## ตัวเลือกที่มีประโยชน์

| Option | Description | Example |
|--------|-------------|---------|
| `--confidence` | ระดับความมั่นใจ (0.0-1.0) | `--confidence 0.4` |
| `--merge-gap` | รวมเสียงที่ใกล้กัน (วินาที) | `--merge-gap 2.0` |
| `--chunk-size` | ขนาด chunk สำหรับไฟล์ยาว | `--chunk-size 120` |
| `--output` | บันทึกผลลัพธ์เป็น JSON | `--output results.json` |
| `--no-merge` | ไม่รวมการตรวจจับ | `--no-merge` |
| `--gpu` | ใช้ GPU | `--gpu` |

## เคล็ดลับ

1. **ไฟล์ยาวมาก**: ใช้ `--chunk-size` ที่ใหญ่ขึ้น (เช่น 180-300)
2. **ความแม่นยำสูง**: ใช้ `--confidence 0.5` ขึ้นไป
3. **หาเสียงหมาทุกเสียง**: ลด confidence เป็น `0.2`
4. **บันทึกผล**: ใช้ `--output` เพื่อบันทึกเป็น JSON

## ปัญหาที่พบบ่อย

**Q: ติดตั้ง librosa ไม่ได้**
```bash
pip install numba==0.56.4
pip install librosa --no-cache-dir
```

**Q: ffmpeg not found**
```bash
# ตรวจสอบว่าติดตั้งแล้ว
ffmpeg -version
```

**Q: Model download ช้า**
- ครั้งแรกต้องดาวน์โหลด YAMNet (~13MB)
- ครั้งต่อไปจะเร็วขึ้น

## ต้องการความช่วยเหลือ?

```bash
# ดูตัวเลือกทั้งหมด
python detect_bark.py --help

# ดูตัวอย่างการใช้งาน
python dog_bark_detector/examples/example_usage.py
```

## เริ่มต้นได้เลย!

```bash
# ลองทดสอบกับไฟล์เสียงของคุณ
python detect_bark.py your_audio_file.mp3

# หรือจาก Google Drive
python detect_bark.py "YOUR_GOOGLE_DRIVE_LINK"
```

สนุกกับการตรวจจับเสียงหมาเห่า! 🐕
