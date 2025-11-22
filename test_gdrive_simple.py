#!/usr/bin/env python3
"""
Simple test script for Google Drive URL parsing (no dependencies required).
"""

import re


def test_url_extraction():
    """Test URL pattern extraction for Google Drive."""

    # Pattern from gdrive_downloader.py (updated)
    DRIVE_URL_PATTERNS = [
        r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
        r'https://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
        r'[?&]id=([a-zA-Z0-9_-]+)',  # Match id= parameter (covers uc?id= and export=download&id=)
    ]

    def extract_file_id(url):
        """Extract file ID from Google Drive URL."""
        for pattern in DRIVE_URL_PATTERNS:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        # Check if it's already just a file ID
        if re.match(r'^[a-zA-Z0-9_-]+$', url):
            return url

        return None

    print("=" * 80)
    print("Testing Google Drive URL Pattern Extraction")
    print("=" * 80)

    # The URL provided by the user
    test_url = "https://drive.google.com/file/d/1Jg8n-5iB4d0gGToptRu1ddbtsqzqCgJd/view?usp=drive_link"
    expected_id = "1Jg8n-5iB4d0gGToptRu1ddbtsqzqCgJd"

    print(f"\nTest URL:")
    print(f"  {test_url}")
    print(f"\nExpected File ID:")
    print(f"  {expected_id}")
    print("\n" + "-" * 80)

    # Test extraction
    extracted_id = extract_file_id(test_url)

    print(f"\nExtracted File ID:")
    print(f"  {extracted_id}")
    print("\n" + "-" * 80)

    # Verify
    if extracted_id == expected_id:
        print("\n✓ SUCCESS: File ID extraction working correctly!")
        print(f"  Pattern matched and extracted: {extracted_id}")
        return True
    else:
        print("\n✗ FAILED: File ID mismatch!")
        print(f"  Expected: {expected_id}")
        print(f"  Got:      {extracted_id}")
        return False


def test_multiple_formats():
    """Test various Google Drive URL formats."""

    DRIVE_URL_PATTERNS = [
        r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
        r'https://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
        r'[?&]id=([a-zA-Z0-9_-]+)',  # Match id= parameter (covers uc?id= and export=download&id=)
    ]

    def extract_file_id(url):
        for pattern in DRIVE_URL_PATTERNS:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    print("\n\n" + "=" * 80)
    print("Testing Multiple Google Drive URL Formats")
    print("=" * 80)

    test_cases = [
        {
            'name': 'User provided link (with drive_link)',
            'url': 'https://drive.google.com/file/d/1Jg8n-5iB4d0gGToptRu1ddbtsqzqCgJd/view?usp=drive_link',
            'expected': '1Jg8n-5iB4d0gGToptRu1ddbtsqzqCgJd'
        },
        {
            'name': 'Standard share link (with sharing)',
            'url': 'https://drive.google.com/file/d/1ABC-def_123/view?usp=sharing',
            'expected': '1ABC-def_123'
        },
        {
            'name': 'Share link (no parameters)',
            'url': 'https://drive.google.com/file/d/1XYZ789/view',
            'expected': '1XYZ789'
        },
        {
            'name': 'Open link format',
            'url': 'https://drive.google.com/open?id=1ABC123',
            'expected': '1ABC123'
        },
        {
            'name': 'UC download link',
            'url': 'https://drive.google.com/uc?id=1DEF456',
            'expected': '1DEF456'
        },
        {
            'name': 'UC download link (with export)',
            'url': 'https://drive.google.com/uc?export=download&id=1GHI789',
            'expected': '1GHI789'
        },
    ]

    all_passed = True

    for i, test in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test['name']}")
        print(f"  URL: {test['url']}")

        extracted = extract_file_id(test['url'])

        if extracted == test['expected']:
            print(f"  ✓ PASS - Extracted: {extracted}")
        else:
            print(f"  ✗ FAIL")
            print(f"    Expected: {test['expected']}")
            print(f"    Got:      {extracted}")
            all_passed = False

    print("\n" + "=" * 80)

    if all_passed:
        print("✓ All URL format tests PASSED!")
    else:
        print("✗ Some URL format tests FAILED!")

    return all_passed


def main():
    """Run tests."""
    print("\n" + "=" * 80)
    print("Google Drive URL Pattern Test Suite")
    print("No dependencies required - Testing regex patterns only")
    print("=" * 80)

    # Test 1: Main URL
    result1 = test_url_extraction()

    # Test 2: Multiple formats
    result2 = test_multiple_formats()

    # Summary
    print("\n\n" + "=" * 80)
    print("Final Summary")
    print("=" * 80)

    if result1 and result2:
        print("\n✓ All tests PASSED!")
        print("\nConclusion:")
        print("  The Google Drive URL pattern matching is working correctly.")
        print("  The provided URL will be recognized and processed properly.")
        return 0
    else:
        print("\n✗ Some tests FAILED!")
        print("\nThe URL pattern matching needs adjustment.")
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main())
