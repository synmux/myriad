# Hardware Reference - M5 Capsule

Detailed hardware specifications and pin mappings for the M5 Capsule pendant device.

## Overview

The M5 Capsule is a compact development kit featuring:
- ESP32-S3 SoC (dual-core Xtensa LX7 @ 240MHz)
- SPM1423 MEMS microphone
- microSD card slot
- USB-C interface
- Battery management (optional)
- RGB LED
- User button

## Block Diagram

```
┌─────────────────────────────────────────────────────┐
│                    M5 Capsule                       │
│                                                     │
│  ┌─────────────────────────────────────────────┐   │
│  │         ESP32-S3 (M5StampS3)                │   │
│  │  ┌──────────────┐      ┌──────────────┐    │   │
│  │  │ Xtensa Core 0│      │ Xtensa Core 1│    │   │
│  │  │   240 MHz    │      │   240 MHz    │    │   │
│  │  └──────────────┘      └──────────────┘    │   │
│  │                                             │   │
│  │  ┌──────────────────────────────────────┐  │   │
│  │  │         8MB PSRAM (Octal)            │  │   │
│  │  └──────────────────────────────────────┘  │   │
│  │                                             │   │
│  │  ┌──────────────────────────────────────┐  │   │
│  │  │      16MB Flash (Quad)               │  │   │
│  │  └──────────────────────────────────────┘  │   │
│  └─────────────────────────────────────────────┘   │
│                                                     │
│  Peripherals:                                       │
│  ┌──────────────┐  ┌──────────────┐                │
│  │  SPM1423     │  │  microSD     │                │
│  │  Microphone  │  │  Card Slot   │                │
│  │  (I2S)       │  │  (SPI)       │                │
│  └──────────────┘  └──────────────┘                │
│                                                     │
│  ┌──────────────┐  ┌──────────────┐                │
│  │  WS2812      │  │  User Button │                │
│  │  RGB LED     │  │  (GPIO 0)    │                │
│  └──────────────┘  └──────────────┘                │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │            USB-C (CP2104)                    │  │
│  │  - Serial programming/debug                  │  │
│  │  - Power (5V)                                │  │
│  └──────────────────────────────────────────────┘  │
│                                                     │
│  ┌──────────────────────────────────────────────┐  │
│  │        Battery Management (IP5306)           │  │
│  │  - LiPo charging                             │  │
│  │  - Power path management                     │  │
│  └──────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────┘
```

## ESP32-S3 Specifications

### CPU
- **Architecture**: Dual-core Xtensa LX7 32-bit
- **Clock Speed**: 240 MHz (configurable down to 10 MHz)
- **Instruction Set**: Xtensa 32-bit RISC
- **FPU**: Single-precision floating point unit

### Memory
- **ROM**: 384 KB
- **SRAM**: 512 KB
- **PSRAM**: 8 MB (Octal SPI, OPI mode)
- **Flash**: 16 MB (Quad SPI, QIO mode)

### Wireless (Not used in Phase 1)
- **WiFi**: 802.11 b/g/n (2.4 GHz)
- **Bluetooth**: BLE 5.0

### Power
- **Operating Voltage**: 3.0V - 3.6V
- **Deep Sleep Current**: ~5 µA
- **Modem Sleep Current**: ~20 mA
- **Active Current**: ~50-200 mA (depending on workload)

## Pin Mapping

### SPM1423 Microphone (I2S)

| Function | GPIO | ESP32-S3 Pin | Direction |
|----------|------|--------------|-----------|
| I2S_SCK  | 5    | GPIO5        | Output    |
| I2S_SD   | 6    | GPIO6        | Input     |
| I2S_WS   | 7    | GPIO7        | Output    |

**I2S Configuration**:
- Mode: Master, PDM/Standard
- Sample Rate: 16 kHz (configurable)
- Bits: 32-bit (actual data in upper 24 bits)
- Channel: Mono (left channel)
- DMA: Yes

### microSD Card (SPI)

| Function | GPIO | ESP32-S3 Pin | Direction |
|----------|------|--------------|-----------|
| SPI_CLK  | 1    | GPIO1        | Output    |
| SPI_MOSI | 2    | GPIO2        | Output    |
| SPI_CS   | 3    | GPIO3        | Output    |
| SPI_MISO | 4    | GPIO4        | Input     |

**SPI Configuration**:
- Host: SPI2_HOST
- Mode: Mode 0 (CPOL=0, CPHA=0)
- Clock: Up to 20 MHz (SDHC)
- Card Type: SDHC (≤32GB), FAT32

### Status Indicators

| Function    | GPIO | Type   | Notes                  |
|-------------|------|--------|------------------------|
| RGB LED     | 21   | Output | WS2812 (programmable)  |
| User Button | 0    | Input  | Active LOW, pull-up    |

**LED Colors** (Example usage):
- Blue: Idle
- Green: Recording
- Red: Error
- Yellow: Paused (ultrasonic detected)
- Purple: Bluetooth transfer

### USB Interface

| Function | Chip   | Notes                    |
|----------|--------|--------------------------|
| USB-UART | CP2104 | Silicon Labs USB bridge  |
| VBUS     | 5V     | USB power input          |

**Serial Configuration**:
- Baud Rate: 115200 (default)
- Data: 8 bits
- Parity: None
- Stop: 1 bit
- Flow Control: None

## SPM1423 Microphone Specifications

### Electrical
- **Supply Voltage**: 1.6V - 3.6V
- **Current**: 650 µA typical
- **Interface**: I2S/PCM
- **Frequency Range**: 50 Hz - 10 kHz (-3dB)
- **Sensitivity**: -26 dBFS (1 kHz @ 94 dB SPL)
- **SNR**: 64 dB
- **THD**: <1%

### Acoustic
- **Directionality**: Omnidirectional
- **Max SPL**: 120 dB
- **Dynamic Range**: 64 dB

### I2S Format
```
Left Channel (Data):
WS LOW: Microphone data (24-bit PCM)
Bit 31: MSB
Bit 8:  LSB
Bit 7-0: Zero-padded

Right Channel (No data):
WS HIGH: Zeros
```

## microSD Card Specifications

### Supported Cards
- **Type**: SDHC (High Capacity)
- **Capacity**: Up to 32 GB
- **Format**: FAT32
- **Speed Class**: Class 4 minimum (4 MB/s)

### Recommended Cards
- SanDisk Ultra (Class 10)
- Samsung EVO Select
- Kingston Canvas Select

### File System
- **Type**: FAT32
- **Cluster Size**: 16 KB (recommended for audio)
- **Max File Size**: 4 GB
- **Max Files**: Depends on card size

## Power Management

### Power Modes

| Mode           | CPU    | WiFi/BT | I2S  | Current   | Wake Time |
|----------------|--------|---------|------|-----------|-----------|
| Active         | 240MHz | ON      | ON   | 150-200mA | N/A       |
| Modem Sleep    | 240MHz | OFF     | ON   | 50-80mA   | <10µs     |
| Light Sleep    | OFF    | OFF     | OFF  | 1-2mA     | <5ms      |
| Deep Sleep     | OFF    | OFF     | OFF  | 5-10µA    | 200-300ms |

### Battery Operation

**Typical Battery**: 3.7V 500mAh LiPo

**Runtime Estimates**:
- Active Recording: ~3-4 hours
- Standby (light sleep): ~10-14 days
- Deep Sleep: ~2-3 months

**Charging**: 
- Via USB-C: 5V @ 500mA
- Charge Time: ~1-2 hours for 500mAh

## Memory Usage Estimates

### Flash (Program Storage)
- Bootloader: ~30 KB
- Partition Table: ~4 KB
- App Code: ~500 KB - 2 MB (depending on features)
- OTA Partition (future): ~2 MB
- **Total Available**: 16 MB

### PSRAM (Dynamic Data)
- Audio Buffers: 32-64 KB
- SD Card Cache: 32 KB
- Bluetooth Stack (future): ~100 KB
- **Total Available**: 8 MB

### SRAM (Fast Access)
- FreeRTOS: ~30 KB
- Stack/Heap: ~200 KB
- DMA Buffers: ~32 KB
- **Total Available**: 512 KB

## Timing Considerations

### I2S Sample Rates

| Sample Rate | Period   | Bit Clock | Notes                    |
|-------------|----------|-----------|--------------------------|
| 8 kHz       | 125 µs   | 512 kHz   | Narrowband (phone)       |
| 16 kHz      | 62.5 µs  | 1.024 MHz | Wideband (recommended)   |
| 44.1 kHz    | 22.7 µs  | 2.8224 MHz| CD quality (overkill)    |
| 48 kHz      | 20.8 µs  | 3.072 MHz | Professional audio       |

**Recommended**: 16 kHz for voice recording (good quality, reasonable file size)

### SD Card Performance

**Sequential Write**:
- Minimum: 500 KB/s (Class 2)
- Recommended: 4 MB/s (Class 10)

**Audio Data Rate**:
- 16 kHz, 16-bit, mono: 32 KB/s
- 44.1 kHz, 16-bit, mono: 88.2 KB/s

**Buffer Size**: 4-16 KB recommended for smooth writes

## Schematic Reference

### I2S Audio Path
```
ESP32-S3          SPM1423
  GPIO5  ───────> SCK (Serial Clock)
  GPIO7  ───────> WS  (Word Select)
  GPIO6  <─────── SD  (Serial Data)
  3.3V   ───────> VDD
  GND    ───────> GND
```

### SPI SD Card Path
```
ESP32-S3          SD Card
  GPIO1  ───────> CLK  (Clock)
  GPIO2  ───────> CMD  (MOSI)
  GPIO4  <─────── DAT0 (MISO)
  GPIO3  ───────> DAT3 (CS)
  3.3V   ───────> VDD
  GND    ───────> GND
```

### LED & Button
```
ESP32-S3          Components
  GPIO21 ───────> WS2812 DIN
  GPIO0  <─────── Button (to GND)
```

## Physical Dimensions

- **Length**: ~70 mm
- **Width**: ~35 mm
- **Height**: ~15 mm
- **Weight**: ~20g (without battery)

## Environmental

- **Operating Temperature**: -20°C to +60°C
- **Storage Temperature**: -40°C to +85°C
- **Humidity**: 10% - 90% RH (non-condensing)

## Further Reading

- [M5 Capsule Official Docs](https://docs.m5stack.com/en/core/M5Capsule)
- [ESP32-S3 Datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf)
- [ESP32-S3 Technical Reference Manual](https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf)
- [SPM1423 Datasheet](https://www.knowles.com/docs/default-source/model-downloads/spm1423hm4h-b-revh.pdf)
