"""
Audio processing utilities for handling various audio formats and large files.
"""

import numpy as np
import librosa
import soundfile as sf
from pydub import AudioSegment
from typing import Tuple, Optional
import tempfile
import os


class AudioProcessor:
    """
    Handles audio file loading, conversion, and processing with support for
    various formats and efficient handling of long audio files.
    """

    def __init__(self, sample_rate: int = 16000):
        """
        Initialize AudioProcessor.

        Args:
            sample_rate: Target sample rate for audio processing (default: 16000 Hz)
        """
        self.sample_rate = sample_rate

    def load_audio(self, file_path: str, duration: Optional[float] = None,
                   offset: float = 0.0) -> Tuple[np.ndarray, int]:
        """
        Load audio file with support for multiple formats.

        Args:
            file_path: Path to audio file
            duration: Duration to load in seconds (None = entire file)
            offset: Start time in seconds

        Returns:
            Tuple of (audio_data, sample_rate)
        """
        file_ext = os.path.splitext(file_path)[1].lower()

        # For formats librosa handles well
        if file_ext in ['.wav', '.flac', '.ogg']:
            audio, sr = librosa.load(file_path, sr=self.sample_rate,
                                    duration=duration, offset=offset, mono=True)
            return audio, sr

        # For other formats (mp3, m4a, etc.), use pydub first
        try:
            audio, sr = librosa.load(file_path, sr=self.sample_rate,
                                    duration=duration, offset=offset, mono=True)
            return audio, sr
        except Exception as e:
            # Fallback to pydub for problematic formats
            return self._load_with_pydub(file_path, duration, offset)

    def _load_with_pydub(self, file_path: str, duration: Optional[float] = None,
                         offset: float = 0.0) -> Tuple[np.ndarray, int]:
        """
        Load audio using pydub (supports more formats via ffmpeg).

        Args:
            file_path: Path to audio file
            duration: Duration to load in seconds
            offset: Start time in seconds

        Returns:
            Tuple of (audio_data, sample_rate)
        """
        # Load with pydub
        audio_segment = AudioSegment.from_file(file_path)

        # Apply offset and duration
        start_ms = int(offset * 1000)
        end_ms = int((offset + duration) * 1000) if duration else len(audio_segment)
        audio_segment = audio_segment[start_ms:end_ms]

        # Convert to mono
        if audio_segment.channels > 1:
            audio_segment = audio_segment.set_channels(1)

        # Set sample rate
        audio_segment = audio_segment.set_frame_rate(self.sample_rate)

        # Convert to numpy array
        samples = np.array(audio_segment.get_array_of_samples())
        audio_data = samples.astype(np.float32) / (2**15)  # Normalize to [-1, 1]

        return audio_data, self.sample_rate

    def get_audio_duration(self, file_path: str) -> float:
        """
        Get the total duration of an audio file without loading it entirely.

        Args:
            file_path: Path to audio file

        Returns:
            Duration in seconds
        """
        try:
            # Try with soundfile first (fastest)
            info = sf.info(file_path)
            return info.duration
        except:
            # Fallback to librosa
            try:
                duration = librosa.get_duration(path=file_path)
                return duration
            except:
                # Last resort: pydub
                audio = AudioSegment.from_file(file_path)
                return len(audio) / 1000.0

    def process_in_chunks(self, file_path: str, chunk_duration: float = 60.0,
                         overlap: float = 2.0):
        """
        Generator that yields audio chunks for efficient processing of long files.

        Args:
            file_path: Path to audio file
            chunk_duration: Duration of each chunk in seconds
            overlap: Overlap between chunks in seconds

        Yields:
            Tuple of (audio_chunk, start_time, end_time)
        """
        total_duration = self.get_audio_duration(file_path)
        offset = 0.0

        while offset < total_duration:
            # Calculate chunk duration (handle last chunk)
            current_chunk_duration = min(chunk_duration, total_duration - offset)

            # Load chunk
            audio_chunk, _ = self.load_audio(file_path,
                                            duration=current_chunk_duration,
                                            offset=offset)

            end_time = offset + current_chunk_duration

            yield audio_chunk, offset, end_time

            # Move to next chunk with overlap
            offset += chunk_duration - overlap

            # Stop if we've reached the end
            if offset >= total_duration:
                break

    def normalize_audio(self, audio: np.ndarray) -> np.ndarray:
        """
        Normalize audio to [-1, 1] range.

        Args:
            audio: Audio data

        Returns:
            Normalized audio data
        """
        max_val = np.abs(audio).max()
        if max_val > 0:
            return audio / max_val
        return audio

    def apply_noise_reduction(self, audio: np.ndarray,
                             noise_threshold: float = 0.02) -> np.ndarray:
        """
        Simple noise reduction by removing low-amplitude samples.

        Args:
            audio: Audio data
            noise_threshold: Threshold below which to reduce signal

        Returns:
            Audio with reduced noise
        """
        # Create a copy
        cleaned = audio.copy()

        # Apply noise gate
        mask = np.abs(cleaned) < noise_threshold
        cleaned[mask] = cleaned[mask] * 0.1

        return cleaned

    @staticmethod
    def convert_to_wav(input_file: str, output_file: Optional[str] = None) -> str:
        """
        Convert any audio format to WAV.

        Args:
            input_file: Path to input audio file
            output_file: Path to output WAV file (optional)

        Returns:
            Path to the converted WAV file
        """
        if output_file is None:
            # Create temporary file
            temp_fd, output_file = tempfile.mkstemp(suffix='.wav')
            os.close(temp_fd)

        audio = AudioSegment.from_file(input_file)
        audio.export(output_file, format='wav')

        return output_file
