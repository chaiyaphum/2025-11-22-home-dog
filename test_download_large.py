#!/usr/bin/env python3
"""
Test downloading large file from Google Drive with improved downloader.
"""

import os
import sys
import re

sys.path.insert(0, os.path.dirname(__file__))

try:
    import requests
    from tqdm import tqdm
except ImportError:
    print("Installing required packages...")
    os.system("pip install -q requests tqdm")
    import requests
    from tqdm import tqdm


def download_large_file(file_id, output_path):
    """Download large file from Google Drive with virus scan handling."""

    print(f"File ID: {file_id}")
    print(f"Output: {output_path}\n")

    session = requests.Session()

    # Step 1: Get initial response
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"
    print(f"Step 1: Fetching download page...")
    response = session.get(download_url, stream=True)

    # Check if we got HTML (virus scan warning)
    content_type = response.headers.get('content-type', '')
    print(f"Content-Type: {content_type}")

    if 'text/html' in content_type:
        print("Step 2: Virus scan warning detected, parsing form...")

        # Parse confirm and uuid from HTML
        confirm_match = re.search(r'name="confirm"\s+value="([^"]+)"', response.text)
        uuid_match = re.search(r'name="uuid"\s+value="([^"]+)"', response.text)
        action_match = re.search(r'action="([^"]+)"', response.text)

        if action_match:
            print(f"  Action URL found: {action_match.group(1)[:50]}...")

        if confirm_match:
            print(f"  Confirm token: {confirm_match.group(1)}")

        if uuid_match:
            print(f"  UUID: {uuid_match.group(1)}")

        # Try new download URL
        if action_match and confirm_match and uuid_match:
            action_url = action_match.group(1)
            confirm = confirm_match.group(1)
            uuid = uuid_match.group(1)

            download_url = f"{action_url}?id={file_id}&export=download&confirm={confirm}&uuid={uuid}"
            print(f"\nStep 3: Downloading with confirmation...")
            print(f"URL: {download_url[:80]}...")

            response = session.get(download_url, stream=True)
        else:
            print("\nStep 3: Trying alternative method...")
            download_url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"
            response = session.get(download_url, stream=True)

    # Get file size
    total_size = int(response.headers.get('content-length', 0))
    content_type = response.headers.get('content-type', '')

    print(f"\nDownload info:")
    print(f"  Content-Type: {content_type}")
    print(f"  Size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")

    # Create directory
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

    # Download
    print(f"\nDownloading...")
    with open(output_path, 'wb') as f:
        if total_size > 0:
            with tqdm(total=total_size, unit='B', unit_scale=True, unit_divisor=1024) as pbar:
                for chunk in response.iter_content(chunk_size=32768):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        else:
            # No size info, download without progress
            downloaded = 0
            for chunk in response.iter_content(chunk_size=32768):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
                    if downloaded % (1024*1024) == 0:  # Print every MB
                        print(f"  Downloaded: {downloaded/1024/1024:.1f} MB")

    file_size = os.path.getsize(output_path)
    print(f"\n✓ Download complete!")
    print(f"  File: {output_path}")
    print(f"  Size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")

    # Detect file type
    with open(output_path, 'rb') as f:
        header = f.read(12)

    if header[:4] == b'ID3\x03' or header[:4] == b'ID3\x04':
        print(f"  Type: MP3 (ID3 tag)")
    elif header[:2] == b'\xff\xfb' or header[:2] == b'\xff\xf3' or header[:2] == b'\xff\xf2':
        print(f"  Type: MP3")
    elif header[:4] == b'RIFF' and header[8:12] == b'WAVE':
        print(f"  Type: WAV")
    elif header[:4] == b'fLaC':
        print(f"  Type: FLAC")
    elif header[:4] == b'OggS':
        print(f"  Type: OGG")
    elif header[4:8] == b'ftyp':
        print(f"  Type: M4A/MP4")
    else:
        print(f"  Type: Unknown")
        print(f"  Header: {header.hex()}")

    return output_path


def main():
    """Test download."""

    print("=" * 80)
    print("Testing Large File Download from Google Drive")
    print("=" * 80 + "\n")

    url = "https://drive.google.com/file/d/1Jg8n-5iB4d0gGToptRu1ddbtsqzqCgJd/view?usp=drive_link"

    # Extract file ID
    match = re.search(r'file/d/([a-zA-Z0-9_-]+)', url)
    if not match:
        print("Could not extract file ID")
        return 1

    file_id = match.group(1)
    output_path = "./test_downloads/2025-11-21_Home.mp3"

    try:
        download_large_file(file_id, output_path)
        return 0
    except Exception as e:
        print(f"\n✗ Error: {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
