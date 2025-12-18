# Pendant Learning Progress Checklist

Track your progress through the ESP-IDF learning pathway for the M5 Capsule audio pendant.

## 📋 How to Use This Checklist

1. Work through phases sequentially
2. Check off items as you complete them
3. Don't skip ahead - each phase builds on previous
4. Commit your code after each major milestone
5. Take notes on challenges and solutions

---

## Phase 1: Environment Setup & Basics

**Target**: 2-3 days | **Status**: [ ] Complete

### Milestone 1.1: PlatformIO + ESP-IDF Setup
- [ ] Install VS Code
- [ ] Install PlatformIO extension
- [ ] Create pendant project
- [ ] Configure `platformio.ini` for ESP32-S3
- [ ] Understand partition tables
- [ ] Connect M5 Capsule via USB
- [ ] Verify device detection

### Milestone 1.2: First Program
- [ ] Write LED blink code
- [ ] Understand GPIO configuration
- [ ] Use `gpio_set_level()`
- [ ] Implement FreeRTOS delay
- [ ] Build firmware successfully
- [ ] Upload to device
- [ ] Verify LED blinks at 1Hz
- [ ] See serial output in monitor

### Milestone 1.3: ESP-IDF Components
- [ ] Understand component directory structure
- [ ] Create `CMakeLists.txt` for component
- [ ] Write simple header file with include guards
- [ ] Implement component source file
- [ ] Declare component dependencies
- [ ] Build project with custom component
- [ ] Call component from `main.c`

**Checkpoint**: LED blinks, serial works, understand components

---

## Phase 2: SD Card Integration

**Target**: 3-4 days | **Status**: [ ] Complete

### Milestone 2.1: SD Card Hardware
- [ ] Insert microSD card (≤32GB, FAT32)
- [ ] Verify card format
- [ ] Understand SPI bus configuration
- [ ] Know M5 Capsule SD pin mappings
  - CLK: GPIO1
  - MOSI: GPIO2
  - CS: GPIO3
  - MISO: GPIO4

### Milestone 2.2: SD Card Initialization
- [ ] Include `esp_vfs_fat.h` and `sdmmc_cmd.h`
- [ ] Configure SPI bus
- [ ] Set up mount configuration
- [ ] Initialize SPI bus with `spi_bus_initialize()`
- [ ] Mount SD card with `esp_vfs_fat_sdspi_mount()`
- [ ] Handle mount errors gracefully
- [ ] Print card info to serial
- [ ] Unmount on error

### Milestone 2.3: File Operations
- [ ] Open file for writing with `fopen()`
- [ ] Write text data with `fprintf()`
- [ ] Close file with `fclose()`
- [ ] Open file for reading
- [ ] Read data with `fgets()` or `fread()`
- [ ] List files in directory
- [ ] Delete files
- [ ] Check free space

### Milestone 2.4: WAV File Format
- [ ] Understand WAV header structure
- [ ] Create `wav_header_t` struct
- [ ] Write `write_wav_header()` function
- [ ] Write `update_wav_header()` function
- [ ] Generate test sine wave in memory
- [ ] Write sine wave as WAV file
- [ ] Transfer file to PC
- [ ] Verify playback in audio software

**Checkpoint**: Can read/write files, WAV format understood

---

## Phase 3: I2S Audio Capture

**Target**: 4-5 days | **Status**: [ ] Complete

### Milestone 3.1: I2S Theory
- [ ] Understand I2S protocol (BCLK, WS, SD)
- [ ] Know difference between PDM and standard I2S
- [ ] Understand sample rate concept
- [ ] Understand bit depth (16/24/32)
- [ ] Know mono vs stereo
- [ ] Understand DMA buffers

### Milestone 3.2: I2S Hardware
- [ ] Know M5 Capsule I2S pins:
  - SCK: GPIO5
  - SD: GPIO6
  - WS: GPIO7
- [ ] Understand SPM1423 microphone
- [ ] Know microphone characteristics
  - Frequency range: 50Hz-10kHz
  - Sensitivity: -26dBFS
  - SNR: 64dB

### Milestone 3.3: I2S Configuration
- [ ] Include `driver/i2s_std.h`
- [ ] Configure channel with `i2s_chan_config_t`
- [ ] Create channel with `i2s_new_channel()`
- [ ] Configure standard mode with `i2s_std_config_t`
- [ ] Set sample rate (16kHz recommended)
- [ ] Configure bit width (32-bit)
- [ ] Set mono mode
- [ ] Map GPIO pins
- [ ] Initialize with `i2s_channel_init_std_mode()`
- [ ] Enable channel with `i2s_channel_enable()`

### Milestone 3.4: Reading Audio
- [ ] Allocate read buffer (int32_t array)
- [ ] Create FreeRTOS task for reading
- [ ] Call `i2s_channel_read()` in loop
- [ ] Check return value for errors
- [ ] Verify `bytes_read` is non-zero
- [ ] Print sample values to serial
- [ ] Verify values change with sound
- [ ] Calculate samples per second
- [ ] Monitor buffer overflow

### Milestone 3.5: Audio Processing Basics
- [ ] Understand DC offset removal
- [ ] Understand high-pass filtering
- [ ] Implement simple high-pass filter
- [ ] Apply filter to samples
- [ ] Calculate RMS energy
- [ ] Detect silence vs. sound
- [ ] Implement threshold-based VAD
- [ ] Tune VAD threshold

**Checkpoint**: Microphone works, can capture audio, filtering works

---

## Phase 4: Integration

**Target**: 5-7 days | **Status**: [ ] Complete

### Milestone 4.1: State Machine Design
- [ ] Define audio states enum:
  - IDLE
  - RECORDING
  - PAUSED
  - STOPPED
- [ ] Create recorder struct
- [ ] Add state variable
- [ ] Add FILE pointer for WAV
- [ ] Add sample counter
- [ ] Add filter structs
- [ ] Add state mutex for thread safety

### Milestone 4.2: State Transitions
- [ ] Write `audio_state_transition()` function
- [ ] Handle IDLE → RECORDING
  - Create timestamped filename
  - Open file
  - Write WAV header
  - Reset sample counter
- [ ] Handle RECORDING → STOPPED
  - Update WAV header with sizes
  - Close file
  - Log statistics
- [ ] Handle RECORDING → PAUSED
  - Pause writing (future: ultrasonic)
- [ ] Handle PAUSED → RECORDING
  - Resume writing

### Milestone 4.3: Recording Task
- [ ] Create `audio_recording_task()`
- [ ] Allocate I2S buffer (int32_t)
- [ ] Allocate WAV buffer (int16_t)
- [ ] Read from I2S in loop
- [ ] Apply high-pass filter
- [ ] Convert 32-bit to 16-bit
- [ ] Run VAD on samples
- [ ] Write to file if recording and speaking
- [ ] Flush file periodically
- [ ] Log progress (seconds recorded)

### Milestone 4.4: Complete System
- [ ] Initialize SD card in `app_main()`
- [ ] Initialize I2S in `app_main()`
- [ ] Initialize recorder struct
- [ ] Create state mutex
- [ ] Initialize filters
- [ ] Start recording task
- [ ] Trigger state transitions
- [ ] Test recording for 10 seconds
- [ ] Verify file created on SD card

### Milestone 4.5: Testing & Validation
- [ ] Record 10-second test file
- [ ] Transfer to PC
- [ ] Play in audio software (Audacity, VLC, etc.)
- [ ] Verify audio quality
- [ ] Test silence detection
- [ ] Test multiple recording sessions
- [ ] Test SD card removal/reinsertion
- [ ] Monitor memory usage
- [ ] Check for memory leaks
- [ ] Verify no buffer overruns

**Checkpoint**: End-to-end recording works reliably

---

## Phase 5: Optimization & Features

**Target**: 3-4 days | **Status**: [ ] Complete

### Milestone 5.1: Power Management
- [ ] Include `esp_pm.h`
- [ ] Configure dynamic frequency scaling
- [ ] Enable light sleep
- [ ] Test battery life
- [ ] Disable I2S when not recording
- [ ] Reduce LED brightness
- [ ] Implement deep sleep (future)

### Milestone 5.2: LED Status Indicators
- [ ] Create `led_task()` function
- [ ] Implement state-based patterns:
  - IDLE: Slow pulse (2s on, 2s off)
  - RECORDING: Fast blink (200ms)
  - PAUSED: Solid on
  - STOPPED: Brief flash
- [ ] Use different colors if RGB LED
- [ ] Add error indication (red)

### Milestone 5.3: File Management
- [ ] Include SNTP for time sync (optional)
- [ ] Generate timestamped filenames
  - Format: `rec_YYYYMMDD_HHMMSS.wav`
- [ ] Implement maximum file size limit
- [ ] Automatically start new file when limit reached
- [ ] Delete oldest files when storage full
- [ ] Add file metadata (JSON sidecar files)

### Milestone 5.4: Error Handling
- [ ] Handle SD card full
- [ ] Handle SD card removed
- [ ] Handle microphone failure
- [ ] Handle buffer overflow
- [ ] Implement watchdog timer
- [ ] Log errors to SD card
- [ ] Recover from errors gracefully
- [ ] Add error LED indication

### Milestone 5.5: Configuration
- [ ] Create `config.h` header
- [ ] Define configurable parameters:
  - Sample rate
  - Bit depth
  - VAD threshold
  - Filter cutoff
  - Buffer sizes
- [ ] Add runtime configuration (future: SD card config file)

**Checkpoint**: Production-ready, stable, efficient system

---

## Phase 6: Future Features

**Target**: TBD | **Status**: [ ] Not Started

### Bluetooth LE (Future)
- [ ] Include BLE libraries
- [ ] Create GATT service
- [ ] Implement file transfer
- [ ] Pair with phone app
- [ ] Stream audio in real-time

### Ultrasonic Detection (Future)
- [ ] Research ultrasonic frequencies (~20kHz)
- [ ] Implement FFT analysis
- [ ] Detect ultrasonic signals
- [ ] Pause recording when detected
- [ ] Decode signal source ID
- [ ] Log suppression events

### Phone App (Future)
- [ ] Design UI
- [ ] Implement Bluetooth connection
- [ ] Download recordings
- [ ] Display transcripts
- [ ] Show action items
- [ ] Sync to cloud

---

## 🎯 Overall Progress

- [ ] Phase 1: Environment Setup (2-3 days)
- [ ] Phase 2: SD Card (3-4 days)
- [ ] Phase 3: I2S Audio (4-5 days)
- [ ] Phase 4: Integration (5-7 days)
- [ ] Phase 5: Optimization (3-4 days)

**Total Estimated Time**: 3-4 weeks

---

## 📝 Notes & Challenges

Use this space to document issues you encountered and how you solved them:

```
Date: _______________
Issue: 

Solution:


---

Date: _______________
Issue:

Solution:


---

Date: _______________
Issue:

Solution:


```

---

## 🏆 Achievement Unlocked

Check these off when you reach major milestones:

- [ ] 🎉 First successful build
- [ ] 💾 First file written to SD card
- [ ] 🎤 First audio samples captured
- [ ] 🎵 First WAV file plays on PC
- [ ] 🤖 Voice activity detection works
- [ ] ⚡ System runs for 1 hour without issues
- [ ] 🔋 Battery operation successful
- [ ] 🚀 Production-ready firmware complete

---

## 📚 Resources Used

Keep track of helpful resources you found:

- [ ] ESP-IDF documentation: _______________________
- [ ] Forum threads: _______________________
- [ ] GitHub repos: _______________________
- [ ] YouTube videos: _______________________
- [ ] Blog posts: _______________________

---

**Last Updated**: _______________
**Current Phase**: _______________
**Days Invested**: _______________
