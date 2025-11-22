#!/usr/bin/env python3
"""
Test downloading from the actual Google Drive URL provided by user.
"""

import os
import sys

# Try to download using only standard library + requests
try:
    import requests
    from tqdm import tqdm
except ImportError:
    print("Installing required packages...")
    os.system("pip install -q requests tqdm")
    import requests
    from tqdm import tqdm

import re


def download_gdrive_file(url, output_path):
    """Download file from Google Drive."""

    # Extract file ID
    pattern = r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)'
    match = re.search(pattern, url)

    if not match:
        raise ValueError("Could not extract file ID from URL")

    file_id = match.group(1)
    print(f"File ID: {file_id}")

    # Download URL
    download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

    session = requests.Session()
    response = session.get(download_url, stream=True)

    # Check for virus scan warning
    if 'download_warning' in response.text or 'virus scan' in response.text.lower():
        # Look for confirmation token
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                download_url = f"https://drive.google.com/uc?export=download&confirm={value}&id={file_id}"
                response = session.get(download_url, stream=True)
                break

    # Get file size
    total_size = int(response.headers.get('content-length', 0))

    # Create directory
    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)

    # Download
    print(f"Downloading to: {output_path}")
    print(f"File size: {total_size:,} bytes ({total_size/1024/1024:.2f} MB)")

    with open(output_path, 'wb') as f:
        if total_size > 0:
            with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
                for chunk in response.iter_content(chunk_size=32768):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        else:
            for chunk in response.iter_content(chunk_size=32768):
                if chunk:
                    f.write(chunk)

    return output_path


def main():
    """Test download."""

    print("=" * 80)
    print("Testing Google Drive Download")
    print("=" * 80)

    url = "https://drive.google.com/file/d/1Jg8n-5iB4d0gGToptRu1ddbtsqzqCgJd/view?usp=drive_link"
    output_path = "./test_downloads/gdrive_audio_test.audio"

    print(f"\nURL: {url}")
    print(f"Output: {output_path}\n")

    try:
        file_path = download_gdrive_file(url, output_path)

        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print(f"\n✓ Download successful!")
            print(f"  File: {file_path}")
            print(f"  Size: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")

            # Try to detect file type
            with open(file_path, 'rb') as f:
                header = f.read(12)

            if header[:4] == b'ID3\x03' or header[:4] == b'ID3\x04':
                print(f"  Type: MP3 (ID3 tag detected)")
            elif header[:4] == b'RIFF' and header[8:12] == b'WAVE':
                print(f"  Type: WAV")
            elif header[:4] == b'fLaC':
                print(f"  Type: FLAC")
            elif header[:4] == b'OggS':
                print(f"  Type: OGG")
            elif header[4:8] == b'ftyp':
                print(f"  Type: M4A/MP4")
            elif header[:2] == b'\xff\xfb' or header[:2] == b'\xff\xf3' or header[:2] == b'\xff\xf2':
                print(f"  Type: MP3")
            else:
                print(f"  Type: Unknown (header: {header[:12].hex()})")

            return file_path
        else:
            print(f"\n✗ Download failed - file not found")
            return None

    except Exception as e:
        print(f"\n✗ Error: {type(e).__name__}: {str(e)}")

        if "403" in str(e) or "Forbidden" in str(e):
            print("\n  Possible reasons:")
            print("  - File is private")
            print("  - Need to set sharing to 'Anyone with the link'")

        return None


if __name__ == '__main__':
    sys.exit(0 if main() else 1)
