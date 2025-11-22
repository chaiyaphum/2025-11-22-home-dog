#!/usr/bin/env python3
"""
Examples of using the Dog Bark Detection library.

This file demonstrates various ways to use the dog_bark_detector package.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from dog_bark_detector import DogBarkDetector, AudioProcessor, GDriveDownloader


def example_1_basic_detection():
    """
    Example 1: Basic detection on a single audio file.
    """
    print("\n" + "="*80)
    print("Example 1: Basic Detection")
    print("="*80 + "\n")

    # Initialize detector and audio processor
    detector = DogBarkDetector(confidence_threshold=0.3)
    audio_processor = AudioProcessor(sample_rate=16000)

    # Load audio file
    audio_file = 'path/to/your/audio.mp3'

    # Check if file exists (for demo purposes)
    if not os.path.exists(audio_file):
        print(f"Note: Please replace '{audio_file}' with an actual audio file path")
        return

    # Load audio
    audio, sr = audio_processor.load_audio(audio_file)

    # Detect dog barks
    detections = detector.detect_in_waveform(audio, sample_rate=sr)

    # Print results
    detector.print_detections(detections)

    # Get summary
    summary = detector.get_detection_summary(detections)
    print(f"\nTotal events detected: {summary['total_events']}")
    print(f"Average confidence: {summary['avg_confidence']:.2%}")


def example_2_process_long_file():
    """
    Example 2: Process a long audio file in chunks.
    """
    print("\n" + "="*80)
    print("Example 2: Processing Long Files")
    print("="*80 + "\n")

    detector = DogBarkDetector(confidence_threshold=0.3)
    audio_processor = AudioProcessor()

    audio_file = 'path/to/long/audio.mp3'

    if not os.path.exists(audio_file):
        print(f"Note: Please replace '{audio_file}' with an actual audio file path")
        return

    all_detections = []

    # Process in 60-second chunks with 2-second overlap
    for audio_chunk, start_time, end_time in audio_processor.process_in_chunks(
            audio_file, chunk_duration=60.0, overlap=2.0):

        print(f"Processing: {detector.format_timestamp(start_time)} - "
              f"{detector.format_timestamp(end_time)}")

        # Detect in chunk
        detections = detector.detect_in_waveform(audio_chunk)

        # Adjust timestamps to global time
        for d in detections:
            d['start_time'] += start_time
            d['end_time'] += start_time

        all_detections.extend(detections)

    # Merge nearby detections
    merged = detector.merge_detections(all_detections, merge_gap=1.0)

    # Print results
    detector.print_detections(merged)


def example_3_custom_confidence():
    """
    Example 3: Using different confidence thresholds.
    """
    print("\n" + "="*80)
    print("Example 3: Custom Confidence Threshold")
    print("="*80 + "\n")

    audio_file = 'path/to/audio.mp3'

    if not os.path.exists(audio_file):
        print(f"Note: Please replace '{audio_file}' with an actual audio file path")
        return

    audio_processor = AudioProcessor()
    audio, sr = audio_processor.load_audio(audio_file)

    # Try different thresholds
    thresholds = [0.2, 0.3, 0.4, 0.5]

    for threshold in thresholds:
        print(f"\nTesting with confidence threshold: {threshold}")
        print("-" * 60)

        detector = DogBarkDetector(confidence_threshold=threshold)
        detections = detector.detect_in_waveform(audio)

        print(f"Detected {len(detections)} events")

        if detections:
            avg_conf = sum(d['confidence'] for d in detections) / len(detections)
            print(f"Average confidence: {avg_conf:.2%}")


def example_4_google_drive():
    """
    Example 4: Download and process from Google Drive.
    """
    print("\n" + "="*80)
    print("Example 4: Google Drive Integration")
    print("="*80 + "\n")

    # Initialize components
    gdrive = GDriveDownloader()
    detector = DogBarkDetector(confidence_threshold=0.3)
    audio_processor = AudioProcessor()

    # Google Drive URL (replace with your actual URL)
    gdrive_url = 'https://drive.google.com/file/d/YOUR_FILE_ID/view'

    print(f"Note: Please replace the URL with an actual Google Drive link")
    print(f"Example URL format: {gdrive_url}\n")

    # This would download the file
    # file_path = gdrive.download_file(gdrive_url, 'downloaded_audio.mp3')

    # Or use convenience method
    # file_path = gdrive.download_if_gdrive(gdrive_url, output_dir='./downloads')

    # Then process as usual
    # audio, sr = audio_processor.load_audio(file_path)
    # detections = detector.detect_in_waveform(audio)
    # detector.print_detections(detections)


def example_5_export_to_json():
    """
    Example 5: Export detection results to JSON.
    """
    print("\n" + "="*80)
    print("Example 5: Export to JSON")
    print("="*80 + "\n")

    import json

    audio_file = 'path/to/audio.mp3'

    if not os.path.exists(audio_file):
        print(f"Note: Please replace '{audio_file}' with an actual audio file path")
        return

    detector = DogBarkDetector(confidence_threshold=0.3)
    audio_processor = AudioProcessor()

    # Process audio
    audio, sr = audio_processor.load_audio(audio_file)
    detections = detector.detect_in_waveform(audio)

    # Prepare results for JSON
    results = {
        'file': audio_file,
        'total_events': len(detections),
        'detections': []
    }

    for idx, d in enumerate(detections, 1):
        results['detections'].append({
            'event_number': idx,
            'start_time': d['start_time'],
            'end_time': d['end_time'],
            'start_timestamp': detector.format_timestamp(d['start_time']),
            'end_timestamp': detector.format_timestamp(d['end_time']),
            'duration': d['end_time'] - d['start_time'],
            'confidence': d['confidence'],
            'class_name': d['class_name']
        })

    # Save to JSON
    output_file = 'detection_results.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"Results saved to {output_file}")
    print(json.dumps(results, indent=2))


def example_6_batch_processing():
    """
    Example 6: Process multiple files in batch.
    """
    print("\n" + "="*80)
    print("Example 6: Batch Processing")
    print("="*80 + "\n")

    import glob

    # Get all audio files in a directory
    audio_files = glob.glob('path/to/audio/folder/*.mp3')

    if not audio_files:
        print("Note: No audio files found. Please update the path.")
        return

    detector = DogBarkDetector(confidence_threshold=0.3)
    audio_processor = AudioProcessor()

    all_results = {}

    for audio_file in audio_files:
        print(f"\nProcessing: {os.path.basename(audio_file)}")
        print("-" * 60)

        try:
            # Load and process
            audio, sr = audio_processor.load_audio(audio_file)
            detections = detector.detect_in_waveform(audio)

            # Store results
            all_results[audio_file] = {
                'total_events': len(detections),
                'detections': detections
            }

            print(f"Found {len(detections)} bark events")

        except Exception as e:
            print(f"Error processing {audio_file}: {str(e)}")
            continue

    # Summary
    print("\n" + "="*80)
    print("Batch Processing Summary")
    print("="*80)

    total_files = len(all_results)
    total_events = sum(r['total_events'] for r in all_results.values())

    print(f"Total files processed: {total_files}")
    print(f"Total bark events found: {total_events}")
    print(f"Average events per file: {total_events/total_files if total_files > 0 else 0:.1f}")


def main():
    """Run all examples."""
    examples = [
        ("Basic Detection", example_1_basic_detection),
        ("Processing Long Files", example_2_process_long_file),
        ("Custom Confidence", example_3_custom_confidence),
        ("Google Drive", example_4_google_drive),
        ("Export to JSON", example_5_export_to_json),
        ("Batch Processing", example_6_batch_processing)
    ]

    print("\n" + "="*80)
    print("Dog Bark Detection - Usage Examples")
    print("="*80)
    print("\nAvailable examples:")
    for idx, (name, _) in enumerate(examples, 1):
        print(f"  {idx}. {name}")

    print("\nNote: These are example templates. Update file paths before running.")
    print("\nTo run an example, uncomment the desired function call below:")

    # Uncomment to run specific examples:
    # example_1_basic_detection()
    # example_2_process_long_file()
    # example_3_custom_confidence()
    # example_4_google_drive()
    # example_5_export_to_json()
    # example_6_batch_processing()


if __name__ == '__main__':
    main()
