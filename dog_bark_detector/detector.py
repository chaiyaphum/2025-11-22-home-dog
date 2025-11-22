"""
Dog bark detection using YAMNet pre-trained model from TensorFlow Hub.
"""

import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from typing import List, Dict, Tuple, Optional
import csv
import io


class DogBarkDetector:
    """
    High-performance dog bark detector using YAMNet audio classification model.
    YAMNet is trained on AudioSet and can detect 521 audio events including dog barks.
    """

    # Dog-related class IDs in YAMNet (based on AudioSet ontology)
    DOG_BARK_CLASSES = [
        'Bark',
        'Bow-wow',
        'Dog',
        'Growling',
        'Howl',
        'Yip',
        'Animal',
        'Domestic animals, pets'
    ]

    def __init__(self, model_url: str = 'https://tfhub.dev/google/yamnet/1',
                 confidence_threshold: float = 0.3,
                 use_gpu: bool = False):
        """
        Initialize dog bark detector.

        Args:
            model_url: URL to YAMNet model on TensorFlow Hub
            confidence_threshold: Minimum confidence score for detection (0-1)
            use_gpu: Whether to use GPU acceleration
        """
        self.confidence_threshold = confidence_threshold
        self.model = None
        self.class_names = None
        self.dog_class_indices = []

        # Configure TensorFlow
        if not use_gpu:
            tf.config.set_visible_devices([], 'GPU')

        # Load model
        self._load_model(model_url)

    def _load_model(self, model_url: str):
        """
        Load YAMNet model from TensorFlow Hub.

        Args:
            model_url: URL to the model
        """
        print(f"Loading YAMNet model from {model_url}...")
        self.model = hub.load(model_url)
        print("Model loaded successfully!")

        # Load class names from YAMNet
        self._load_class_names()

    def _load_class_names(self):
        """
        Load AudioSet class names used by YAMNet.
        """
        # YAMNet uses AudioSet class names
        class_map_path = self.model.class_map_path().numpy().decode('utf-8')
        self.class_names = self._load_csv_as_list(class_map_path)

        # Find indices of dog-related classes
        self.dog_class_indices = []
        for idx, class_name in enumerate(self.class_names):
            for dog_class in self.DOG_BARK_CLASSES:
                if dog_class.lower() in class_name.lower():
                    self.dog_class_indices.append(idx)
                    print(f"Found dog-related class: {class_name} (index: {idx})")
                    break

    def _load_csv_as_list(self, csv_text: str) -> List[str]:
        """
        Parse CSV text and return class names.

        Args:
            csv_text: CSV content as string

        Returns:
            List of class names
        """
        class_names = []
        with io.StringIO(csv_text) as f:
            reader = csv.DictReader(f)
            for row in reader:
                class_names.append(row['display_name'])
        return class_names

    def detect_in_waveform(self, waveform: np.ndarray, sample_rate: int = 16000) \
            -> List[Dict]:
        """
        Detect dog barks in audio waveform.

        Args:
            waveform: Audio waveform as numpy array
            sample_rate: Sample rate of the audio (YAMNet expects 16kHz)

        Returns:
            List of detection events with timestamps and confidence scores
        """
        # YAMNet expects 16kHz mono audio
        if sample_rate != 16000:
            raise ValueError(f"YAMNet requires 16kHz audio, got {sample_rate}Hz")

        # Ensure waveform is float32
        if waveform.dtype != np.float32:
            waveform = waveform.astype(np.float32)

        # Run inference
        scores, embeddings, spectrogram = self.model(waveform)

        # YAMNet produces scores for each 0.96 second frame
        # Frame rate is approximately 1 frame per 0.48 seconds (50% overlap)
        frame_duration = 0.96  # seconds
        hop_duration = 0.48    # seconds

        detections = []

        # Process each frame
        for frame_idx, frame_scores in enumerate(scores.numpy()):
            # Check dog-related classes
            max_dog_score = 0.0
            max_dog_class = None
            max_dog_class_idx = None

            for class_idx in self.dog_class_indices:
                if frame_scores[class_idx] > max_dog_score:
                    max_dog_score = frame_scores[class_idx]
                    max_dog_class = self.class_names[class_idx]
                    max_dog_class_idx = class_idx

            # If confidence exceeds threshold, record detection
            if max_dog_score >= self.confidence_threshold:
                start_time = frame_idx * hop_duration
                end_time = start_time + frame_duration

                detections.append({
                    'start_time': start_time,
                    'end_time': end_time,
                    'confidence': float(max_dog_score),
                    'class_name': max_dog_class,
                    'class_index': max_dog_class_idx
                })

        return detections

    def merge_detections(self, detections: List[Dict],
                        merge_gap: float = 1.0) -> List[Dict]:
        """
        Merge nearby detections into continuous events.

        Args:
            detections: List of detection events
            merge_gap: Maximum gap between detections to merge (seconds)

        Returns:
            List of merged detection events
        """
        if not detections:
            return []

        # Sort by start time
        sorted_detections = sorted(detections, key=lambda x: x['start_time'])

        merged = []
        current = sorted_detections[0].copy()

        for detection in sorted_detections[1:]:
            # If gap is small enough, merge
            if detection['start_time'] - current['end_time'] <= merge_gap:
                current['end_time'] = max(current['end_time'], detection['end_time'])
                current['confidence'] = max(current['confidence'], detection['confidence'])
            else:
                # Save current and start new
                merged.append(current)
                current = detection.copy()

        # Add last detection
        merged.append(current)

        return merged

    def format_timestamp(self, seconds: float) -> str:
        """
        Format seconds as HH:MM:SS.mmm

        Args:
            seconds: Time in seconds

        Returns:
            Formatted timestamp string
        """
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60

        return f"{hours:02d}:{minutes:02d}:{secs:06.3f}"

    def print_detections(self, detections: List[Dict], offset: float = 0.0):
        """
        Print detection results in a readable format.

        Args:
            detections: List of detection events
            offset: Time offset to add to timestamps (for chunked processing)
        """
        if not detections:
            print("No dog barks detected.")
            return

        print(f"\n{'='*80}")
        print(f"Found {len(detections)} dog bark event(s):")
        print(f"{'='*80}")

        for idx, detection in enumerate(detections, 1):
            start = detection['start_time'] + offset
            end = detection['end_time'] + offset
            duration = end - start

            print(f"\n[Event #{idx}]")
            print(f"  Time: {self.format_timestamp(start)} - {self.format_timestamp(end)}")
            print(f"  Duration: {duration:.2f} seconds")
            print(f"  Confidence: {detection['confidence']:.2%}")
            print(f"  Type: {detection['class_name']}")

        print(f"\n{'='*80}\n")

    def get_detection_summary(self, detections: List[Dict]) -> Dict:
        """
        Get summary statistics of detections.

        Args:
            detections: List of detection events

        Returns:
            Dictionary with summary statistics
        """
        if not detections:
            return {
                'total_events': 0,
                'total_duration': 0.0,
                'avg_confidence': 0.0,
                'max_confidence': 0.0,
                'min_confidence': 0.0
            }

        confidences = [d['confidence'] for d in detections]
        durations = [d['end_time'] - d['start_time'] for d in detections]

        return {
            'total_events': len(detections),
            'total_duration': sum(durations),
            'avg_duration': np.mean(durations),
            'avg_confidence': np.mean(confidences),
            'max_confidence': max(confidences),
            'min_confidence': min(confidences)
        }
