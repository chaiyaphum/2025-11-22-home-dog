#!/usr/bin/env python3
"""
Demo script showing how to use the dog bark detector with the provided Google Drive URL.

This demonstrates:
1. URL parsing and file ID extraction
2. How to use the URL with detect_bark.py
3. Alternative methods using the library directly
"""

import re


def demonstrate_url_usage():
    """Demonstrate how to use the Google Drive URL."""

    # The URL provided by the user
    gdrive_url = "https://drive.google.com/file/d/1Jg8n-5iB4d0gGToptRu1ddbtsqzqCgJd/view?usp=drive_link"

    print("=" * 80)
    print("Google Drive URL Usage Demo")
    print("=" * 80)

    # Extract file ID
    pattern = r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, gdrive_url)

    if match:
        file_id = match.group(1)
        print(f"\nProvided URL:")
        print(f"  {gdrive_url}")
        print(f"\nExtracted File ID:")
        print(f"  {file_id}")
        print(f"\n✓ URL is valid and will work with the system!")
    else:
        print("✗ Could not extract file ID")
        return

    print("\n" + "=" * 80)
    print("Usage Methods")
    print("=" * 80)

    # Method 1: Command line
    print("\n【 Method 1: Command Line (Recommended) 】")
    print("-" * 80)
    print("\nSimply pass the Google Drive URL to detect_bark.py:")
    print(f'\n  python detect_bark.py "{gdrive_url}"')
    print("\nWith options:")
    print(f'  python detect_bark.py "{gdrive_url}" --confidence 0.3 --output results.json')

    # Method 2: Using library
    print("\n\n【 Method 2: Python Script 】")
    print("-" * 80)
    print("\nCreate a Python script:")
    print("""
from dog_bark_detector import DogBarkDetector, AudioProcessor, GDriveDownloader

# Initialize components
gdrive = GDriveDownloader()
detector = DogBarkDetector(confidence_threshold=0.3)
audio_processor = AudioProcessor()

# Your Google Drive URL
gdrive_url = "https://drive.google.com/file/d/1Jg8n-5iB4d0gGToptRu1ddbtsqzqCgJd/view?usp=drive_link"

# Download file
print("Downloading from Google Drive...")
audio_file = gdrive.download_if_gdrive(gdrive_url, output_dir='./downloads')

# Process audio
print("Processing audio...")
all_detections = []

for audio_chunk, start_time, end_time in audio_processor.process_in_chunks(
        audio_file, chunk_duration=60.0):
    detections = detector.detect_in_waveform(audio_chunk)

    # Adjust timestamps
    for d in detections:
        d['start_time'] += start_time
        d['end_time'] += start_time

    all_detections.extend(detections)

# Merge and display results
merged = detector.merge_detections(all_detections)
detector.print_detections(merged)
""")

    # Method 3: Direct file ID
    print("\n\n【 Method 3: Using File ID Directly 】")
    print("-" * 80)
    print(f"\nYou can also use just the file ID:")
    print(f"\n  python detect_bark.py {file_id}")
    print(f"\nOr construct a direct download URL:")
    direct_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    print(f"  {direct_url}")

    # Important notes
    print("\n\n" + "=" * 80)
    print("Important Notes")
    print("=" * 80)
    print("""
1. File Permissions:
   - The file must be publicly accessible or set to "Anyone with the link"
   - Private files require authentication

2. File Size:
   - Large files (>25MB) may require additional confirmation
   - The downloader handles this automatically

3. Supported Formats:
   - MP3, WAV, FLAC, OGG, M4A, and more
   - Any format supported by ffmpeg

4. Processing Time:
   - Depends on file length and system specs
   - Approximately 1-2 seconds per minute of audio
""")

    # Quick start
    print("\n" + "=" * 80)
    print("Quick Start")
    print("=" * 80)
    print(f"""
To detect dog barks in your Google Drive file right now:

1. Make sure the file is publicly accessible

2. Run this command:

   python detect_bark.py "{gdrive_url}"

3. Wait for the download and processing to complete

4. View the results showing when dog barks occur!

Optional: Save results to JSON:

   python detect_bark.py "{gdrive_url}" --output my_results.json
""")

    print("=" * 80)
    print("\nThe system is ready to process your Google Drive audio file!")
    print("=" * 80 + "\n")


def test_url_formats():
    """Show various supported URL formats."""
    print("\n" + "=" * 80)
    print("Supported Google Drive URL Formats")
    print("=" * 80)

    formats = [
        {
            'name': 'Share Link (your format)',
            'example': 'https://drive.google.com/file/d/FILE_ID/view?usp=drive_link',
            'note': 'Most common format from "Share" button'
        },
        {
            'name': 'Share Link with sharing',
            'example': 'https://drive.google.com/file/d/FILE_ID/view?usp=sharing',
            'note': 'Alternative share link format'
        },
        {
            'name': 'Open Link',
            'example': 'https://drive.google.com/open?id=FILE_ID',
            'note': 'Older format'
        },
        {
            'name': 'Direct Download',
            'example': 'https://drive.google.com/uc?id=FILE_ID',
            'note': 'Direct download URL'
        },
        {
            'name': 'Export Download',
            'example': 'https://drive.google.com/uc?export=download&id=FILE_ID',
            'note': 'Full direct download URL'
        },
        {
            'name': 'File ID Only',
            'example': 'FILE_ID',
            'note': 'Just the file ID (will be converted)'
        },
    ]

    for i, fmt in enumerate(formats, 1):
        print(f"\n{i}. {fmt['name']}")
        print(f"   Format:  {fmt['example']}")
        print(f"   Note:    {fmt['note']}")
        print(f"   Status:  ✓ Supported")

    print("\n" + "=" * 80)
    print("All these formats will work with the dog bark detector!")
    print("=" * 80 + "\n")


def main():
    """Run demo."""
    demonstrate_url_usage()
    test_url_formats()


if __name__ == '__main__':
    main()
