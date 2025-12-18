# Pendant Audio Capture

Audio recording pendant based on M5 Capsule (ESP32-S3) for the Pendant project.

## Hardware

- **M5 Capsule** with M5StampS3
  - ESP32-S3 dual-core @ 240MHz
  - SPM1423 MEMS microphone (I2S)
  - microSD card slot (SPI)
  - USB-C programming/power
  - Battery connector (optional)

## Features

### Current
- [ ] I2S audio capture from microphone
- [ ] Voice frequency filtering (300Hz-3400Hz)
- [ ] Voice Activity Detection (VAD)
- [ ] WAV file recording to SD card
- [ ] LED status indicators
- [ ] Power management for battery operation

### Future
- [ ] Bluetooth LE communication with phone
- [ ] Ultrasonic signal detection (TV/music suppression)
- [ ] OTA firmware updates
- [ ] Real-time audio streaming

## Quick Start

### Prerequisites

1. Install [VS Code](https://code.visualstudio.com/)
2. Install [PlatformIO IDE extension](https://platformio.org/install/ide?install=vscode)
3. Connect M5 Capsule via USB-C

### Build & Upload

```bash
# Initialize project (first time only)
pio init

# Build firmware
pio run

# Upload to device
pio run --target upload

# Monitor serial output
pio device monitor

# Build, upload, and monitor in one command
pio run --target upload --target monitor
```

## Pin Configuration

### M5 Capsule (ESP32-S3)

#### Microphone (SPM1423 - I2S)
- **GPIO 5**: I2S Serial Clock (SCK)
- **GPIO 6**: I2S Serial Data (SD)
- **GPIO 7**: I2S Left/Right Clock (WS)

#### SD Card (SPI)
- **GPIO 1**: SPI Clock (SCK)
- **GPIO 2**: SPI MOSI
- **GPIO 3**: SPI Chip Select (CS)
- **GPIO 4**: SPI MISO

#### Status LED
- **GPIO 21**: RGB LED (WS2812)

#### Other
- **GPIO 0**: User Button

## Project Structure

```
pendant/
├── platformio.ini          # PlatformIO configuration
├── src/
│   └── main.c             # Main application
├── components/            # Custom ESP-IDF components
│   ├── audio_capture/     # I2S audio capture
│   ├── sd_storage/        # SD card file management
│   ├── audio_processing/  # Filters, VAD, DSP
│   └── power_mgmt/        # Power optimization
├── include/               # Header files
└── test/                  # Unit tests
```

## Development Workflow

1. **Phase 1**: Blink LED (verify toolchain)
2. **Phase 2**: SD card mount & file I/O
3. **Phase 3**: I2S microphone initialization
4. **Phase 4**: Audio capture & WAV recording
5. **Phase 5**: Voice filtering & VAD
6. **Phase 6**: Power optimization

See [PENDANT-LEARNING-PATHWAY.md](../docs/PENDANT-LEARNING-PATHWAY.md) for detailed learning guide.

## Configuration

Key parameters in `src/config.h`:

- `SAMPLE_RATE`: Audio sample rate (16000 Hz default)
- `BITS_PER_SAMPLE`: Audio bit depth (16-bit default)
- `VAD_THRESHOLD`: Voice activity detection threshold
- `HPF_CUTOFF`: High-pass filter cutoff frequency (80 Hz)

## Troubleshooting

### SD Card Not Detected
- Check card is formatted as FAT32
- Verify card capacity is ≤32GB (SDHC)
- Ensure card is fully inserted
- Try different card

### No Audio Data
- Verify I2S pins are correct for M5 Capsule
- Check microphone is not physically blocked
- Increase logging level to debug I2S initialization
- Test with simple I2S example first

### Build Errors
- Ensure ESP-IDF platform is up to date: `pio pkg update`
- Clean build: `pio run --target clean`
- Check component dependencies in `CMakeLists.txt`

## Resources

- [M5 Capsule Documentation](https://docs.m5stack.com/en/core/M5Capsule)
- [ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/)
- [Learning Pathway](../docs/PENDANT-LEARNING-PATHWAY.md)

## License

See [LICENSE](../LICENSE) in repository root.
