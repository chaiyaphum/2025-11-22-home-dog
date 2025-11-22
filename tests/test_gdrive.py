#!/usr/bin/env python3
"""
Test script for Google Drive downloader with the provided URL.
"""

import sys
import os

# Add parent directory to path (go up one level from tests/)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dog_bark_detector import GDriveDownloader


def test_url_parsing():
    """Test if the URL pattern matching works."""
    print("=" * 80)
    print("Testing Google Drive URL Pattern Matching")
    print("=" * 80)

    # The URL provided by the user
    test_url = "https://drive.google.com/file/d/1Jg8n-5iB4d0gGToptRu1ddbtsqzqCgJd/view?usp=drive_link"

    gdrive = GDriveDownloader()

    print(f"\nTest URL: {test_url}")
    print("-" * 80)

    # Test if it's recognized as a Google Drive URL
    is_gdrive = gdrive.is_gdrive_url(test_url)
    print(f"Is Google Drive URL: {is_gdrive}")

    if is_gdrive:
        print("✓ URL recognized as Google Drive link")
    else:
        print("✗ URL NOT recognized as Google Drive link")
        return False

    # Test file ID extraction
    file_id = gdrive.extract_file_id(test_url)
    print(f"\nExtracted File ID: {file_id}")

    if file_id:
        print(f"✓ Successfully extracted file ID: {file_id}")
        expected_id = "1Jg8n-5iB4d0gGToptRu1ddbtsqzqCgJd"
        if file_id == expected_id:
            print(f"✓ File ID matches expected: {expected_id}")
            return True
        else:
            print(f"✗ File ID mismatch!")
            print(f"  Expected: {expected_id}")
            print(f"  Got:      {file_id}")
            return False
    else:
        print("✗ Failed to extract file ID")
        return False


def test_other_url_formats():
    """Test various Google Drive URL formats."""
    print("\n" + "=" * 80)
    print("Testing Various Google Drive URL Formats")
    print("=" * 80)

    test_cases = [
        {
            'url': 'https://drive.google.com/file/d/1Jg8n-5iB4d0gGToptRu1ddbtsqzqCgJd/view?usp=drive_link',
            'expected_id': '1Jg8n-5iB4d0gGToptRu1ddbtsqzqCgJd',
            'description': 'Standard share link with drive_link parameter'
        },
        {
            'url': 'https://drive.google.com/file/d/1ABC123xyz/view?usp=sharing',
            'expected_id': '1ABC123xyz',
            'description': 'Standard share link with sharing parameter'
        },
        {
            'url': 'https://drive.google.com/file/d/1ABC123xyz/view',
            'expected_id': '1ABC123xyz',
            'description': 'Share link without parameters'
        },
        {
            'url': 'https://drive.google.com/open?id=1ABC123xyz',
            'expected_id': '1ABC123xyz',
            'description': 'Open link format'
        },
        {
            'url': 'https://drive.google.com/uc?id=1ABC123xyz',
            'expected_id': '1ABC123xyz',
            'description': 'Direct download link format'
        },
    ]

    gdrive = GDriveDownloader()
    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['description']}")
        print(f"URL: {test_case['url']}")

        file_id = gdrive.extract_file_id(test_case['url'])

        if file_id == test_case['expected_id']:
            print(f"✓ PASSED - Extracted ID: {file_id}")
        else:
            print(f"✗ FAILED")
            print(f"  Expected: {test_case['expected_id']}")
            print(f"  Got:      {file_id}")
            all_passed = False

    return all_passed


def test_download_attempt():
    """Attempt to download the file from Google Drive."""
    print("\n" + "=" * 80)
    print("Testing File Download from Google Drive")
    print("=" * 80)

    test_url = "https://drive.google.com/file/d/1Jg8n-5iB4d0gGToptRu1ddbtsqzqCgJd/view?usp=drive_link"
    output_dir = "./test_downloads"

    # Create output directory
    os.makedirs(output_dir, exist_ok=True)

    gdrive = GDriveDownloader()

    print(f"\nAttempting to download from Google Drive...")
    print(f"URL: {test_url}")
    print(f"Output directory: {output_dir}")
    print("-" * 80)

    try:
        # Try to download
        file_path = gdrive.download_if_gdrive(test_url, output_dir)

        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"\n✓ Download successful!")
            print(f"  File path: {file_path}")
            print(f"  File size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")

            # Check if it's an audio file
            file_ext = os.path.splitext(file_path)[1].lower()
            if file_ext in ['.mp3', '.wav', '.m4a', '.ogg', '.flac']:
                print(f"  File type: Audio file ({file_ext})")
            else:
                print(f"  File type: {file_ext if file_ext else 'Unknown'}")

            return True
        else:
            print(f"\n✗ Download failed - file not found at: {file_path}")
            return False

    except Exception as e:
        print(f"\n✗ Download failed with error:")
        print(f"  {type(e).__name__}: {str(e)}")

        # Check if it's a permission issue
        if "403" in str(e) or "Forbidden" in str(e):
            print("\n  This may be a private file. Possible solutions:")
            print("  1. Make the file publicly accessible")
            print("  2. Set sharing to 'Anyone with the link can view'")
            print("  3. Use a different authentication method")
        elif "404" in str(e) or "Not Found" in str(e):
            print("\n  The file may not exist or has been deleted")

        return False


def main():
    """Run all tests."""
    print("\n" + "=" * 80)
    print("Google Drive Downloader Test Suite")
    print("=" * 80)

    results = {}

    # Test 1: URL parsing
    print("\n")
    results['url_parsing'] = test_url_parsing()

    # Test 2: Various URL formats
    print("\n")
    results['url_formats'] = test_other_url_formats()

    # Test 3: Actual download (optional)
    print("\n")
    response = input("\nDo you want to attempt downloading the file? (y/n): ").lower()

    if response == 'y':
        results['download'] = test_download_attempt()
    else:
        print("\nSkipping download test.")
        results['download'] = None

    # Summary
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)

    for test_name, result in results.items():
        if result is None:
            status = "SKIPPED"
            symbol = "-"
        elif result:
            status = "PASSED"
            symbol = "✓"
        else:
            status = "FAILED"
            symbol = "✗"

        print(f"{symbol} {test_name.replace('_', ' ').title():20s} - {status}")

    print("=" * 80)

    # Clean up test downloads directory if empty
    if os.path.exists('./test_downloads') and not os.listdir('./test_downloads'):
        os.rmdir('./test_downloads')

    return 0 if all(r for r in results.values() if r is not None) else 1


if __name__ == '__main__':
    sys.exit(main())
