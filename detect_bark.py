#!/usr/bin/env python3
"""
Dog Bark Detection - Main Script

Analyze audio files to detect dog barks with timestamps.
Supports multiple formats, long files, and Google Drive links.

Usage:
    python detect_bark.py <audio_file_or_url> [options]

Examples:
    # Local file
    python detect_bark.py my_audio.mp3

    # Google Drive link
    python detect_bark.py "https://drive.google.com/file/d/YOUR_FILE_ID/view"

    # With custom confidence threshold
    python detect_bark.py my_audio.wav --confidence 0.4

    # Save results to JSON
    python detect_bark.py my_audio.mp3 --output results.json
"""

import argparse
import json
import sys
import os
from typing import List, Dict
import time

from dog_bark_detector import DogBarkDetector, AudioProcessor, GDriveDownloader


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description='Detect dog barks in audio files with high accuracy',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s recording.mp3
  %(prog)s "https://drive.google.com/file/d/FILE_ID/view"
  %(prog)s audio.wav --confidence 0.4 --merge-gap 2.0
  %(prog)s long_audio.mp3 --chunk-size 120 --output results.json
        """
    )

    parser.add_argument(
        'input',
        type=str,
        help='Audio file path or Google Drive URL'
    )

    parser.add_argument(
        '-c', '--confidence',
        type=float,
        default=0.3,
        help='Confidence threshold for detection (0.0-1.0, default: 0.3)'
    )

    parser.add_argument(
        '-m', '--merge-gap',
        type=float,
        default=1.0,
        help='Merge detections within this gap in seconds (default: 1.0)'
    )

    parser.add_argument(
        '-s', '--chunk-size',
        type=float,
        default=60.0,
        help='Chunk size for processing long files in seconds (default: 60)'
    )

    parser.add_argument(
        '-o', '--output',
        type=str,
        default=None,
        help='Output file for results (JSON format)'
    )

    parser.add_argument(
        '--no-merge',
        action='store_true',
        help='Do not merge nearby detections'
    )

    parser.add_argument(
        '--gpu',
        action='store_true',
        help='Use GPU acceleration if available'
    )

    parser.add_argument(
        '--download-dir',
        type=str,
        default='./downloads',
        help='Directory for Google Drive downloads (default: ./downloads)'
    )

    return parser.parse_args()


def process_audio_file(file_path: str, detector: DogBarkDetector,
                      audio_processor: AudioProcessor,
                      chunk_size: float = 60.0,
                      merge_gap: float = 1.0,
                      no_merge: bool = False) -> List[Dict]:
    """
    Process audio file and detect dog barks.

    Args:
        file_path: Path to audio file
        detector: Dog bark detector instance
        audio_processor: Audio processor instance
        chunk_size: Chunk size in seconds for processing
        merge_gap: Gap for merging detections
        no_merge: If True, don't merge detections

    Returns:
        List of detection events
    """
    print(f"\n{'='*80}")
    print(f"Processing: {file_path}")
    print(f"{'='*80}\n")

    # Get audio duration
    total_duration = audio_processor.get_audio_duration(file_path)
    print(f"Audio duration: {detector.format_timestamp(total_duration)}")
    print(f"Processing in chunks of {chunk_size} seconds...\n")

    all_detections = []
    chunk_count = 0

    # Process in chunks
    for audio_chunk, start_time, end_time in audio_processor.process_in_chunks(
            file_path, chunk_duration=chunk_size, overlap=2.0):

        chunk_count += 1
        print(f"Processing chunk {chunk_count}: "
              f"{detector.format_timestamp(start_time)} - "
              f"{detector.format_timestamp(end_time)}")

        # Detect in current chunk
        detections = detector.detect_in_waveform(audio_chunk)

        # Adjust timestamps based on chunk offset
        for detection in detections:
            detection['start_time'] += start_time
            detection['end_time'] += start_time

        all_detections.extend(detections)

        if detections:
            print(f"  → Found {len(detections)} detection(s) in this chunk")

    # Merge nearby detections if requested
    if not no_merge and all_detections:
        print(f"\nMerging detections with gap threshold: {merge_gap}s")
        original_count = len(all_detections)
        all_detections = detector.merge_detections(all_detections, merge_gap=merge_gap)
        print(f"Merged {original_count} detections into {len(all_detections)} events")

    return all_detections


def save_results(detections: List[Dict], output_path: str, input_file: str):
    """
    Save detection results to JSON file.

    Args:
        detections: List of detection events
        output_path: Output file path
        input_file: Input audio file path
    """
    results = {
        'input_file': input_file,
        'total_detections': len(detections),
        'detections': []
    }

    detector = DogBarkDetector(confidence_threshold=0.0)  # Just for formatting

    for idx, detection in enumerate(detections, 1):
        results['detections'].append({
            'event_number': idx,
            'start_time': detection['start_time'],
            'end_time': detection['end_time'],
            'start_timestamp': detector.format_timestamp(detection['start_time']),
            'end_timestamp': detector.format_timestamp(detection['end_time']),
            'duration': detection['end_time'] - detection['start_time'],
            'confidence': detection['confidence'],
            'class_name': detection['class_name']
        })

    # Add summary
    if detections:
        summary = detector.get_detection_summary(detections)
        results['summary'] = summary

    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to: {output_path}")


def main():
    """Main function."""
    args = parse_arguments()

    # Validate confidence threshold
    if not 0.0 <= args.confidence <= 1.0:
        print("Error: Confidence threshold must be between 0.0 and 1.0")
        sys.exit(1)

    try:
        start_time = time.time()

        # Initialize components
        print("\n" + "="*80)
        print("Dog Bark Detection System")
        print("="*80 + "\n")

        print("Initializing components...")

        # Handle Google Drive downloads
        gdrive = GDriveDownloader()
        input_file = gdrive.download_if_gdrive(args.input, args.download_dir)

        # Check if file exists
        if not os.path.exists(input_file):
            print(f"Error: File not found: {input_file}")
            sys.exit(1)

        # Initialize detector
        detector = DogBarkDetector(
            confidence_threshold=args.confidence,
            use_gpu=args.gpu
        )

        # Initialize audio processor
        audio_processor = AudioProcessor(sample_rate=16000)

        # Process audio file
        detections = process_audio_file(
            input_file,
            detector,
            audio_processor,
            chunk_size=args.chunk_size,
            merge_gap=args.merge_gap,
            no_merge=args.no_merge
        )

        # Print results
        detector.print_detections(detections)

        # Print summary
        if detections:
            summary = detector.get_detection_summary(detections)
            print("Summary Statistics:")
            print(f"  Total events: {summary['total_events']}")
            print(f"  Total duration of barking: {summary['total_duration']:.2f} seconds")
            print(f"  Average event duration: {summary['avg_duration']:.2f} seconds")
            print(f"  Average confidence: {summary['avg_confidence']:.2%}")
            print(f"  Confidence range: {summary['min_confidence']:.2%} - {summary['max_confidence']:.2%}")

        # Save results if requested
        if args.output:
            save_results(detections, args.output, input_file)

        elapsed_time = time.time() - start_time
        print(f"\nTotal processing time: {elapsed_time:.2f} seconds")

    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
