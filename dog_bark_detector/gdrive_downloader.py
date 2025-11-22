"""
Google Drive file downloader with support for large files and direct/shared links.
"""

import os
import re
from typing import Optional
import requests
from tqdm import tqdm


class GDriveDownloader:
    """
    Download files from Google Drive with support for both direct and shared links.
    Handles large files efficiently with progress tracking.
    """

    CHUNK_SIZE = 32768  # 32KB chunks
    DRIVE_URL_PATTERNS = [
        r'https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)',
        r'https://drive\.google\.com/open\?id=([a-zA-Z0-9_-]+)',
        r'[?&]id=([a-zA-Z0-9_-]+)',  # Match id= parameter (covers uc?id= and export=download&id=)
    ]

    def __init__(self):
        """Initialize GDrive downloader."""
        self.session = requests.Session()

    def extract_file_id(self, url: str) -> Optional[str]:
        """
        Extract Google Drive file ID from various URL formats.

        Args:
            url: Google Drive URL

        Returns:
            File ID or None if not found
        """
        for pattern in self.DRIVE_URL_PATTERNS:
            match = re.search(pattern, url)
            if match:
                return match.group(1)

        # Check if it's already just a file ID
        if re.match(r'^[a-zA-Z0-9_-]+$', url):
            return url

        return None

    def download_file(self, url_or_id: str, output_path: str,
                     show_progress: bool = True) -> str:
        """
        Download file from Google Drive.

        Args:
            url_or_id: Google Drive URL or file ID
            output_path: Path to save the downloaded file
            show_progress: Whether to show download progress bar

        Returns:
            Path to downloaded file

        Raises:
            ValueError: If URL is invalid
            Exception: If download fails
        """
        # Extract file ID
        file_id = self.extract_file_id(url_or_id)
        if not file_id:
            raise ValueError(f"Could not extract file ID from: {url_or_id}")

        print(f"Downloading from Google Drive (ID: {file_id})...")

        # Try direct download first
        download_url = f"https://drive.google.com/uc?export=download&id={file_id}"

        try:
            response = self.session.get(download_url, stream=True)

            # Check for virus scan warning (large files)
            if 'download_warning' in response.text or 'virus scan' in response.text.lower():
                download_url = self._get_confirm_token_url(response, file_id)
                response = self.session.get(download_url, stream=True)

            # Check response
            if response.status_code != 200:
                raise Exception(f"Download failed with status code: {response.status_code}")

            # Get file size if available
            total_size = int(response.headers.get('content-length', 0))

            # Create output directory if needed
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Download with progress bar
            with open(output_path, 'wb') as f:
                if show_progress and total_size > 0:
                    with tqdm(total=total_size, unit='B', unit_scale=True,
                             desc=os.path.basename(output_path)) as pbar:
                        for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                            if chunk:
                                f.write(chunk)
                                pbar.update(len(chunk))
                else:
                    # No progress bar
                    for chunk in response.iter_content(chunk_size=self.CHUNK_SIZE):
                        if chunk:
                            f.write(chunk)

            print(f"Download complete: {output_path}")
            return output_path

        except Exception as e:
            # Clean up partial download
            if os.path.exists(output_path):
                os.remove(output_path)
            raise Exception(f"Download failed: {str(e)}")

    def _get_confirm_token_url(self, response: requests.Response, file_id: str) -> str:
        """
        Get download URL with confirmation token for large files.

        Args:
            response: Initial response from Google Drive
            file_id: Google Drive file ID

        Returns:
            URL with confirmation token
        """
        # Look for confirmation token
        for key, value in response.cookies.items():
            if key.startswith('download_warning'):
                return f"https://drive.google.com/uc?export=download&confirm={value}&id={file_id}"

        # Alternative: parse token from HTML
        token_match = re.search(r'confirm=([0-9A-Za-z_]+)', response.text)
        if token_match:
            confirm = token_match.group(1)
            return f"https://drive.google.com/uc?export=download&confirm={confirm}&id={file_id}"

        # If no token found, try the original URL
        return f"https://drive.google.com/uc?export=download&id={file_id}"

    @staticmethod
    def is_gdrive_url(url: str) -> bool:
        """
        Check if a URL is a Google Drive link.

        Args:
            url: URL to check

        Returns:
            True if it's a Google Drive URL
        """
        return 'drive.google.com' in url.lower()

    def download_if_gdrive(self, url_or_path: str, output_dir: str = './downloads') -> str:
        """
        Download file if it's a Google Drive URL, otherwise return the original path.

        Args:
            url_or_path: Google Drive URL or local file path
            output_dir: Directory to save downloaded files

        Returns:
            Path to the file (downloaded or original)
        """
        if self.is_gdrive_url(url_or_path):
            # Generate output filename
            file_id = self.extract_file_id(url_or_path)
            output_path = os.path.join(output_dir, f"gdrive_{file_id}.audio")

            # Check if already downloaded
            if os.path.exists(output_path):
                print(f"File already downloaded: {output_path}")
                return output_path

            # Download
            return self.download_file(url_or_path, output_path)
        else:
            # It's a local path
            return url_or_path


# Alternative: gdown library (simpler but requires separate package)
def download_with_gdown(url_or_id: str, output_path: str) -> str:
    """
    Download using gdown library (alternative method).

    Args:
        url_or_id: Google Drive URL or file ID
        output_path: Output file path

    Returns:
        Path to downloaded file

    Note:
        Requires: pip install gdown
    """
    try:
        import gdown

        # Extract file ID if URL
        if 'drive.google.com' in url_or_id:
            match = re.search(r'/d/([a-zA-Z0-9_-]+)', url_or_id)
            if match:
                file_id = match.group(1)
                url = f'https://drive.google.com/uc?id={file_id}'
            else:
                url = url_or_id
        else:
            url = f'https://drive.google.com/uc?id={url_or_id}'

        # Download
        gdown.download(url, output_path, quiet=False)
        return output_path

    except ImportError:
        raise ImportError("gdown library not installed. Install with: pip install gdown")
