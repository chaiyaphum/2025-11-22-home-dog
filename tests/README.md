# Test Suite

This directory contains all tests for the dog bark detection system.

## Test Files

### Installation & Setup Tests
- **test_installation.py**: Verifies system installation and dependencies
  - Tests if all required packages can be imported
  - Tests if dog_bark_detector package can be imported
  - Tests component initialization
  - Tests ffmpeg availability

### Google Drive Integration Tests
- **test_gdrive.py**: Comprehensive Google Drive downloader tests
  - URL pattern matching
  - File ID extraction
  - Various URL format support
  - Actual file download (optional, interactive)

- **test_gdrive_simple.py**: Simple URL parsing tests (no dependencies)
  - Lightweight regex pattern testing
  - No external dependencies required
  - Good for quick validation

- **test_real_gdrive.py**: Real Google Drive file download test
  - Tests actual download from Google Drive
  - File type detection
  - Basic download functionality

- **test_download_large.py**: Large file download with virus scan handling
  - Tests large file downloads
  - Handles Google Drive virus scan warnings
  - Progress tracking with tqdm

## Running Tests

### Run all tests
```bash
pytest
```

### Run specific test file
```bash
pytest tests/test_installation.py
```

### Run with verbose output
```bash
pytest -v
```

### Run tests by marker
```bash
# Run only unit tests (no external resources)
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"

# Skip tests requiring internet
pytest -m "not requires_internet"
```

### Run specific test function
```bash
pytest tests/test_gdrive.py::test_url_parsing
```

## Test Categories

Tests are marked with the following categories:

- **unit**: Fast tests that don't require external resources
- **integration**: Tests that may download files or use external APIs
- **slow**: Tests that take a long time to run
- **requires_internet**: Tests that require internet connection
- **requires_ffmpeg**: Tests that require ffmpeg to be installed

## Interactive Tests

Some tests (like `test_gdrive.py`) include interactive prompts for downloading actual files. These can be run manually but should be skipped in automated test suites.

## Dependencies

Most tests require the packages in `requirements.txt`. However:
- `test_gdrive_simple.py` only requires Python standard library
- Download tests require `requests` and `tqdm`
- Installation test checks for all dependencies

## CI/CD Integration

For CI/CD pipelines, consider:
1. Running `test_installation.py` first to verify setup
2. Skipping interactive and slow tests: `pytest -m "not slow"`
3. Mocking external resources for faster, more reliable tests
