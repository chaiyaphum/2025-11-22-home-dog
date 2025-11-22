"""
Dog Bark Detection System
A high-performance audio analysis tool for detecting dog barks in audio files.
"""

__version__ = "1.0.0"
__author__ = "Claude AI"

from .detector import DogBarkDetector
from .audio_processor import AudioProcessor
from .gdrive_downloader import GDriveDownloader

__all__ = ["DogBarkDetector", "AudioProcessor", "GDriveDownloader"]
