# shotdetect

Classify images as screenshots or other content using Ollama vision models.

## Features

- **Multiple Image Formats**: Supports JPG, PNG, GIF, BMP, WEBP, TIFF, HEIC, and DNG (RAW) formats
- **Powerful Vision Models**: Uses Ollama's vision models (default: qwen2.5vl:7b)
- **Batch Processing**: Concurrent processing with configurable batch sizes
- **File Organization**: Copy or move files based on classification results
- **Progress Tracking**: Beautiful terminal progress bars with real-time updates
- **JSON Output**: Machine-readable output for scripting and automation
- **Dry Run Mode**: Preview operations without making changes
- **Model Management**: Automatic model downloading and management

## Installation

```bash
cd ~/work/shotdetect
uv sync
```

Or install globally:

```bash
uv tool install .
```

### Prerequisites

Make sure you have Ollama installed and running:

```bash
# Install Ollama (visit https://ollama.com for instructions)
# Start Ollama
ollama serve
```

### System Dependencies

For HEIC support, you may need additional system libraries:

**macOS:**

```bash
brew install libheif
```

**Ubuntu/Debian:**

```bash
sudo apt-get install libheif-dev
```

**CentOS/RHEL:**

```bash
sudo yum install libheif-devel
```

## Usage

### Basic Classification

Classify all images in a directory:

```bash
uv run shotdetect /path/to/images
```

Or if installed globally:

```bash
shotdetect /path/to/images
```

### Copy Files Based on Classification

Copy screenshots to one folder and other images to another:

```bash
uv run shotdetect /path/to/images --copy /path/to/output
```

This creates:

- `/path/to/output/screenshots/` - Contains detected screenshots
- `/path/to/output/other/` - Contains other images

### Move Files

Move files instead of copying:

```bash
uv run shotdetect /path/to/images --move /path/to/output
```

### Use Different Models

```bash
# Use a specific model
uv run shotdetect /path/to/images --model qwen2.5vl:14b

# Download and use all variants of a model
uv run shotdetect /path/to/images --model qwen2.5vl:* --download-models
```

### Dry Run Mode

Preview what would be done without making changes:

```bash
uv run shotdetect /path/to/images --copy /output --dry-run
```

### JSON Output for Scripts

```bash
uv run shotdetect /path/to/images --json > results.json
```

### Advanced Options

```bash
uv run shotdetect /path/to/images \
  --model qwen2.5vl:7b \
  --batch-size 10 \
  --max-image-size 2048x2048 \
  --copy /output \
  --quiet
```

## Model Management

### Download Models

```bash
# Download a specific model
uv run shotdetect download --model qwen2.5vl:7b

# Download all variants of a model
uv run shotdetect download --model qwen2.5vl:*
```

### List Available Models

```bash
uv run shotdetect models
```

## Supported Image Formats

- **Standard**: JPG, JPEG, PNG, GIF, BMP, WEBP, TIFF, TIF
- **HEIC**: HEIC, HEIF (Apple's modern image format)
- **RAW**: DNG, NEF, CR2, CR3, ARW, ORF, RW2

## Output Formats

### Human-Readable Output

Default terminal output with progress bars, statistics, and colored formatting.

### JSON Output

Machine-readable output for scripting:

```json
{"event": "file_classified", "file_path": "/path/to/image.jpg", "classification": "screenshot", "timestamp": "2024-01-01T12:00:00"}
{"event": "processing_completed", "stats": {"total_files": 100, "screenshots": 45, "other": 55, "errors": 0}}
```

## Configuration

### Batch Size

Adjust concurrent processing:

```bash
# Process 20 images simultaneously (higher memory usage)
uv run shotdetect /images --batch-size 20

# Process 1 image at a time (lower memory usage)
uv run shotdetect /images --batch-size 1
```

### Image Size Limits

Control memory usage by limiting image sizes:

```bash
# Resize large images to 1024x1024 before processing
uv run shotdetect /images --max-image-size 1024x1024

# Use higher resolution for better accuracy
uv run shotdetect /images --max-image-size 2048x2048
```

## Error Handling

- **Corrupted files**: Skipped with error logging
- **Unsupported formats**: Ignored with warnings
- **Network issues**: Automatic retry with exponential backoff
- **Model unavailable**: Automatic download attempt

## Performance

- **HEIC files**: Processed efficiently with hardware acceleration when available
- **RAW files**: Converted to RGB with optimized settings
- **Large files**: Automatically resized to prevent memory issues
- **Concurrent processing**: Configurable batch sizes for optimal performance

## Examples

### Organize Phone Photos

```bash
# Classify and organize iPhone photos (includes HEIC files)
uv run shotdetect ~/Pictures/iPhone --copy ~/Pictures/Organized --recursive
```

### Process RAW Images

```bash
# Classify DNG files from a camera
uv run shotdetect ~/Pictures/RAW --model qwen2.5vl:14b --batch-size 3
```

### Automation Script

```bash
#!/bin/bash
# Auto-organize screenshots daily

uv run shotdetect ~/Downloads \
  --move ~/Pictures/Screenshots \
  --json \
  --quiet > /tmp/shotdetect.log

# Check for errors
if grep -q '"event": "error"' /tmp/shotdetect.log; then
    echo "Errors detected in classification"
    exit 1
fi
```

## Troubleshooting

### Ollama Connection Issues

```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve
```

### Memory Issues

Reduce batch size and image size:

```bash
uv run shotdetect /images --batch-size 1 --max-image-size 512x512
```

### HEIC Support Issues

Install system dependencies:

```bash
# macOS
brew install libheif

# Verify installation
python -c "import pillow_heif; print('HEIC support available')"
```

### DNG Support Issues

```bash
# Verify rawpy installation
python -c "import rawpy; print('RAW support available')"
```

## License

MIT License - see LICENSE file for details.
