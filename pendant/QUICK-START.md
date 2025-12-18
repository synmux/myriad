# Quick Start Guide - M5 Capsule Pendant

Get your M5 Capsule recording audio to SD card in 30 minutes.

## Hardware Checklist

- [ ] M5 Capsule with M5StampS3
- [ ] USB-C cable
- [ ] microSD card (≤32GB, FAT32 formatted)
- [ ] Computer with VS Code

## Software Setup (10 minutes)

### 1. Install PlatformIO

```bash
# In VS Code:
# 1. Open Extensions (Ctrl+Shift+X)
# 2. Search "PlatformIO IDE"
# 3. Click Install
# 4. Restart VS Code
```

### 2. Open Project

```bash
# In VS Code:
# File → Open Folder → Select /workspace/pendant
```

### 3. Connect Hardware

1. Insert microSD card into M5 Capsule
2. Connect USB-C cable from M5 Capsule to computer
3. Verify device detected:

```bash
# Linux/Mac
ls /dev/tty* | grep -i usb

# Windows (in Device Manager)
# Look for "Silicon Labs CP210x" or "USB Serial Device"
```

## First Build (15 minutes)

### 1. Build Firmware

```bash
# Click PlatformIO icon in left sidebar
# Click "Build" (checkmark icon)
# Or use terminal:
cd /workspace/pendant
pio run
```

**First build takes ~10 minutes** (downloads ESP-IDF toolchain)

### 2. Upload to Device

```bash
# Click "Upload" (arrow icon) in PlatformIO
# Or use terminal:
pio run --target upload
```

### 3. Monitor Output

```bash
# Click "Serial Monitor" (plug icon)
# Or use terminal:
pio device monitor

# Expected output:
# I (123) MAIN: M5 Capsule Audio Recorder v0.1.0
# I (456) MAIN: LED ON
# I (1456) MAIN: LED OFF
```

Press `Ctrl+C` to exit monitor.

## Verify It Works (5 minutes)

### LED Should Blink

- **GPIO 21** LED should blink every second
- Serial monitor shows "LED ON" / "LED OFF"

### If Not Working

1. **No serial output?**
   - Press RESET button on M5 Capsule
   - Check USB cable (must support data, not charge-only)
   - Try different USB port

2. **Upload fails?**
   - Hold BOOT button while clicking RESET
   - Keep BOOT held until upload starts
   - Check correct port in `platformio.ini`

3. **Build errors?**
   ```bash
   # Clean and rebuild
   pio run --target clean
   pio run
   ```

## Next Steps

Now that basic firmware works, follow the learning pathway:

### Phase 1: SD Card (Next)
See: [PENDANT-LEARNING-PATHWAY.md](../docs/PENDANT-LEARNING-PATHWAY.md#phase-2-sd-card-integration-3-4-days)

```c
// Add to main.c:
#include "esp_vfs_fat.h"
#include "sdmmc_cmd.h"

// Implement sd_card_init() function
// Test by creating a file
```

### Phase 2: I2S Audio
Once SD card works, move to audio capture:

```c
#include "driver/i2s_std.h"

// Configure I2S for SPM1423 microphone
// Read audio samples
// Print to serial to verify
```

### Phase 3: Record to SD
Combine SD card + I2S:

```c
// Create WAV file
// Write audio samples
// Verify playback on PC
```

## Useful Commands

```bash
# Build
pio run

# Upload
pio run -t upload

# Monitor (serial output)
pio device monitor

# Upload + Monitor (most common)
pio run -t upload -t monitor

# Clean build
pio run -t clean

# Update dependencies
pio pkg update

# List connected devices
pio device list
```

## Pin Reference (M5 Capsule)

```
Microphone (I2S):
  SCK: GPIO 5
  SD:  GPIO 6
  WS:  GPIO 7

SD Card (SPI):
  CLK:  GPIO 1
  MOSI: GPIO 2
  CS:   GPIO 3
  MISO: GPIO 4

Status:
  LED: GPIO 21
  BTN: GPIO 0
```

## Common Issues

### "Permission denied" on Linux
```bash
sudo usermod -a -G dialout $USER
# Logout and login again
```

### SD Card Not Detected
- Format as FAT32 (not exFAT)
- Use card ≤32GB
- Try different card
- Check card is fully inserted

### Out of Memory
- Check `board_build.partitions` in platformio.ini
- Reduce buffer sizes
- Enable PSRAM usage

## Resources

- **Learning Pathway**: [PENDANT-LEARNING-PATHWAY.md](../docs/PENDANT-LEARNING-PATHWAY.md)
- **M5 Capsule Docs**: https://docs.m5stack.com/en/core/M5Capsule
- **ESP-IDF Guide**: https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/
- **PlatformIO Docs**: https://docs.platformio.org/

## Getting Help

1. Check serial monitor output for error messages
2. Review relevant section in learning pathway
3. Search ESP-IDF documentation
4. ESP32 forum: https://esp32.com/
5. PlatformIO community: https://community.platformio.org/

---

**You're ready to start!** 🚀

Follow the detailed learning pathway at [PENDANT-LEARNING-PATHWAY.md](../docs/PENDANT-LEARNING-PATHWAY.md) for step-by-step guidance.
