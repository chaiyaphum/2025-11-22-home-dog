#!/usr/bin/env python3
"""
Test script to verify the dog bark detection system installation.

This script checks if all dependencies are correctly installed and
the system components can be imported.
"""

import sys


def test_imports():
    """Test if all required packages can be imported."""
    print("Testing imports...")
    print("=" * 60)

    packages = {
        'numpy': 'NumPy',
        'librosa': 'Librosa',
        'soundfile': 'SoundFile',
        'pydub': 'Pydub',
        'tensorflow': 'TensorFlow',
        'tensorflow_hub': 'TensorFlow Hub',
        'tqdm': 'tqdm',
        'requests': 'Requests'
    }

    all_ok = True

    for package, name in packages.items():
        try:
            __import__(package)
            print(f"✓ {name:20s} - OK")
        except ImportError as e:
            print(f"✗ {name:20s} - FAILED ({str(e)})")
            all_ok = False

    print("=" * 60)
    return all_ok


def test_dog_bark_detector():
    """Test if dog_bark_detector package can be imported."""
    print("\nTesting dog_bark_detector package...")
    print("=" * 60)

    try:
        from dog_bark_detector import DogBarkDetector, AudioProcessor, GDriveDownloader
        print("✓ DogBarkDetector imported successfully")
        print("✓ AudioProcessor imported successfully")
        print("✓ GDriveDownloader imported successfully")
        print("=" * 60)
        return True
    except ImportError as e:
        print(f"✗ Failed to import dog_bark_detector: {str(e)}")
        print("=" * 60)
        return False


def test_initialization():
    """Test if components can be initialized."""
    print("\nTesting component initialization...")
    print("=" * 60)

    try:
        from dog_bark_detector import DogBarkDetector, AudioProcessor, GDriveDownloader

        # Test AudioProcessor
        print("Initializing AudioProcessor...")
        audio_processor = AudioProcessor(sample_rate=16000)
        print("✓ AudioProcessor initialized")

        # Test GDriveDownloader
        print("Initializing GDriveDownloader...")
        gdrive = GDriveDownloader()
        print("✓ GDriveDownloader initialized")

        # Test DogBarkDetector (this will download the model on first run)
        print("Initializing DogBarkDetector (may download model on first run)...")
        print("This may take a moment...")
        detector = DogBarkDetector(confidence_threshold=0.3, use_gpu=False)
        print("✓ DogBarkDetector initialized")

        print("=" * 60)
        return True

    except Exception as e:
        print(f"✗ Initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()
        print("=" * 60)
        return False


def test_ffmpeg():
    """Test if ffmpeg is available."""
    print("\nTesting ffmpeg availability...")
    print("=" * 60)

    import subprocess

    try:
        result = subprocess.run(['ffmpeg', '-version'],
                              capture_output=True,
                              text=True,
                              timeout=5)

        if result.returncode == 0:
            # Get first line (version info)
            version_line = result.stdout.split('\n')[0]
            print(f"✓ ffmpeg is installed: {version_line}")
            print("=" * 60)
            return True
        else:
            print("✗ ffmpeg command failed")
            print("=" * 60)
            return False

    except FileNotFoundError:
        print("✗ ffmpeg not found in PATH")
        print("\nPlease install ffmpeg:")
        print("  Ubuntu/Debian: sudo apt-get install ffmpeg")
        print("  macOS: brew install ffmpeg")
        print("  Windows: Download from https://ffmpeg.org/")
        print("=" * 60)
        return False
    except subprocess.TimeoutExpired:
        print("✗ ffmpeg command timed out")
        print("=" * 60)
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Dog Bark Detection - Installation Test")
    print("="*60 + "\n")

    results = {}

    # Test 1: Imports
    results['imports'] = test_imports()

    # Test 2: Package import
    results['package'] = test_dog_bark_detector()

    # Test 3: ffmpeg
    results['ffmpeg'] = test_ffmpeg()

    # Test 4: Initialization (only if package import succeeded)
    if results['package']:
        results['initialization'] = test_initialization()
    else:
        results['initialization'] = False
        print("\nSkipping initialization test (package import failed)")

    # Summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    for test_name, passed in results.items():
        status = "PASSED" if passed else "FAILED"
        symbol = "✓" if passed else "✗"
        print(f"{symbol} {test_name.capitalize():20s} - {status}")

    print("="*60)

    all_passed = all(results.values())

    if all_passed:
        print("\n✓ All tests passed! The system is ready to use.")
        print("\nTo get started, run:")
        print("  python detect_bark.py <your_audio_file.mp3>")
        print("\nOr check the examples:")
        print("  python dog_bark_detector/examples/example_usage.py")
        return 0
    else:
        print("\n✗ Some tests failed. Please install missing dependencies.")
        print("\nTo install dependencies:")
        print("  pip install -r requirements.txt")

        if not results['ffmpeg']:
            print("\nDon't forget to install ffmpeg (see above)")

        return 1


if __name__ == '__main__':
    sys.exit(main())
