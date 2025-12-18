# Project Overview: Pendant Audio Capture

Complete documentation and learning resources for building the M5 Capsule audio pendant.

## 🎯 Project Goal

Build a wearable pendant that:
1. Captures audio from a MEMS microphone
2. Filters for voice frequencies (300-3400 Hz)
3. Detects voice activity (only record when speaking)
4. Records to SD card as WAV files
5. Transfers to phone via Bluetooth (future)
6. Respects ultrasonic "do not record" signals (future)

## 📁 Documentation Structure

### 🚀 Getting Started
1. **[QUICK-START.md](QUICK-START.md)** - Get running in 30 minutes
   - Hardware setup
   - Software installation
   - First build and upload
   - Verification steps

2. **[README.md](README.md)** - Project overview and quick reference
   - Feature list
   - Pin mappings
   - Build commands
   - Troubleshooting

### 📚 Learning Resources
3. **[PENDANT-LEARNING-PATHWAY.md](../docs/PENDANT-LEARNING-PATHWAY.md)** - Comprehensive learning guide
   - Phase 1: Environment Setup (2-3 days)
   - Phase 2: SD Card Integration (3-4 days)
   - Phase 3: I2S Audio Capture (4-5 days)
   - Phase 4: Integration (5-7 days)
   - Phase 5: Optimization (3-4 days)
   - Total: ~3-4 weeks for complete system

### 🔧 Technical Reference
4. **[docs/HARDWARE-REFERENCE.md](docs/HARDWARE-REFERENCE.md)** - Hardware specifications
   - ESP32-S3 details
   - Pin mappings
   - Microphone specs
   - Memory layout
   - Power management
   - Timing considerations

5. **[components/README.md](components/README.md)** - Component architecture
   - How to create components
   - Planned components
   - API design guidelines
   - Best practices

## 🗺️ Learning Pathway Summary

### Phase 1: Basics (Week 1)
**Goal**: Understand ESP-IDF and PlatformIO

- ✅ Install tools
- ✅ Create project
- ✅ Blink LED
- ✅ Understand FreeRTOS tasks
- ✅ Learn component system

**Time**: 2-3 days
**Output**: Working LED blink program

---

### Phase 2: SD Card (Week 1-2)
**Goal**: Store data on SD card

- Mount SD card via SPI
- Create/read/write files
- Understand FAT filesystem
- Learn WAV file format
- Handle errors gracefully

**Time**: 3-4 days
**Output**: Can write files to SD card

---

### Phase 3: Audio (Week 2-3)
**Goal**: Capture audio from microphone

- Configure I2S peripheral
- Read audio samples
- Understand digital audio
- Implement filtering (high-pass)
- Create voice activity detector

**Time**: 4-5 days
**Output**: Can capture and process audio

---

### Phase 4: Integration (Week 3-4)
**Goal**: Complete recording system

- Combine SD + Audio
- Implement state machine
- Write WAV files with audio
- Add error handling
- Test end-to-end

**Time**: 5-7 days
**Output**: Working audio recorder

---

### Phase 5: Polish (Week 4)
**Goal**: Production-ready firmware

- Power optimization
- LED status indicators
- File management
- Performance tuning
- Documentation

**Time**: 3-4 days
**Output**: Reliable, efficient system

---

### Future Phases
**Bluetooth**: Week 5-6
**Ultrasonic**: Week 7
**Phone App**: Week 8+

## 🛠️ Current Implementation Status

### Completed ✅
- [x] Project structure
- [x] PlatformIO configuration
- [x] Basic LED blink example
- [x] Complete documentation suite
- [x] Learning pathway guide

### In Progress 🚧
- [ ] SD card component
- [ ] I2S audio component
- [ ] Audio processing component
- [ ] State machine
- [ ] WAV file writer

### Future 🔮
- [ ] Bluetooth LE
- [ ] Ultrasonic detection
- [ ] Phone companion app
- [ ] Cloud sync
- [ ] Whisper processing

## 📦 Project Structure

```
pendant/
├── docs/
│   └── HARDWARE-REFERENCE.md      # Hardware specs
├── components/
│   ├── README.md                  # Component guide
│   ├── audio_capture/             # I2S microphone (future)
│   ├── audio_processing/          # Filters, VAD (future)
│   ├── sd_storage/                # SD card management (future)
│   └── wav_format/                # WAV encoding (future)
├── src/
│   └── main.c                     # Main application
├── platformio.ini                 # Build configuration
├── PROJECT-OVERVIEW.md            # This file
├── QUICK-START.md                 # 30-minute guide
└── README.md                      # Project README
```

## 🎓 Learning Resources by Topic

### ESP-IDF Fundamentals
- ESP-IDF Programming Guide: https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/
- ESP32 Forum: https://esp32.com/
- GitHub Examples: https://github.com/espressif/esp-idf/tree/master/examples

### PlatformIO
- PlatformIO Docs: https://docs.platformio.org/
- ESP32 Platform: https://docs.platformio.org/en/latest/platforms/espressif32.html
- Community Forum: https://community.platformio.org/

### Digital Audio
- I2S Protocol: https://www.sparkfun.com/datasheets/BreakoutBoards/I2SBUS.pdf
- WAV Format: http://soundfile.sapp.org/doc/WaveFormat/
- DSP Guide: https://www.analog.com/en/design-center/landing-pages/001/beginners-guide-to-dsp.html

### Hardware
- M5 Capsule: https://docs.m5stack.com/en/core/M5Capsule
- ESP32-S3 Datasheet: https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf
- SPM1423 Mic: https://www.knowles.com/docs/default-source/model-downloads/spm1423hm4h-b-revh.pdf

## 🔑 Key Concepts to Master

### 1. FreeRTOS
- **Tasks**: Concurrent execution units
- **Queues**: Inter-task communication
- **Semaphores**: Synchronization
- **Timers**: Delayed/periodic functions

### 2. Peripheral Interfaces
- **I2S**: Digital audio (to/from microphone)
- **SPI**: SD card communication
- **GPIO**: LEDs, buttons
- **UART**: USB serial debugging

### 3. Memory Management
- **DRAM**: General purpose RAM
- **IRAM**: Fast instruction memory
- **PSRAM**: External RAM (slower)
- **Flash**: Program storage

### 4. Audio Processing
- **Sample Rate**: How often to measure (16 kHz)
- **Bit Depth**: Resolution of measurement (16-bit)
- **Filtering**: Remove unwanted frequencies
- **VAD**: Detect speech vs silence

### 5. File Systems
- **FAT32**: SD card filesystem
- **VFS**: Virtual filesystem layer
- **Buffering**: Write efficiency
- **Wear Leveling**: Extend SD life

## 🐛 Common Issues & Solutions

### Issue: Build Errors
```bash
# Solution: Clean rebuild
pio run --target clean
pio pkg update
pio run
```

### Issue: Upload Fails
```
# Solution: Enter bootloader mode
1. Hold BOOT button
2. Press RESET button
3. Release RESET
4. Release BOOT after upload starts
```

### Issue: SD Card Not Detected
```
# Solutions:
1. Format as FAT32 (not exFAT)
2. Use card ≤32GB
3. Check connections
4. Try different card
```

### Issue: No Audio Data
```
# Solutions:
1. Verify I2S pins in code match hardware
2. Check microphone not blocked
3. Enable I2S debug logging
4. Test with simple I2S example
```

### Issue: Out of Memory
```
# Solutions:
1. Enable PSRAM in platformio.ini
2. Reduce buffer sizes
3. Use smaller partition table
4. Check for memory leaks
```

## 📊 Performance Targets

### Audio Quality
- Sample Rate: 16 kHz (wideband speech)
- Bit Depth: 16-bit
- Channels: 1 (mono)
- Data Rate: 32 KB/s

### Recording Capacity (16GB SD Card)
- Hours: ~140 hours
- Files: Limited by FAT32 (~65,000)

### Battery Life (500mAh)
- Active Recording: 3-4 hours
- Standby: 10-14 days
- Deep Sleep: 2-3 months

### System Resources
- Flash Used: ~1-2 MB
- SRAM Used: ~200 KB
- PSRAM Used: ~100 KB

## 🎯 Milestones & Checkpoints

### Milestone 1: "Hello World" ✅
- LED blinks
- Serial output works
- Can upload firmware

### Milestone 2: "Storage"
- SD card mounts
- Can create files
- Can write/read data

### Milestone 3: "Listen"
- I2S initializes
- Audio samples captured
- Data looks reasonable

### Milestone 4: "Record"
- WAV file created
- Audio written continuously
- File plays on PC

### Milestone 5: "Smart"
- Voice detection works
- Filtering reduces noise
- Only records when speaking

### Milestone 6: "Reliable"
- Runs for hours
- Handles errors
- LED shows status

## 🚀 Next Steps

### If You're Just Starting:
1. Read [QUICK-START.md](QUICK-START.md)
2. Get LED blinking
3. Move to Phase 1 of learning pathway

### If LED Works:
1. Read Phase 2: SD Card
2. Implement SD card mounting
3. Test file creation

### If SD Works:
1. Read Phase 3: I2S Audio
2. Capture raw audio samples
3. Verify with oscilloscope/serial

### If Audio Works:
1. Read Phase 4: Integration
2. Combine SD + Audio
3. Record WAV files

### If Recording Works:
1. Read Phase 5: Polish
2. Add filtering and VAD
3. Optimize power usage

## 💡 Tips for Success

1. **Go Slow**: Don't skip phases. Each builds on previous.
2. **Test Early**: Verify each component works before integrating.
3. **Log Everything**: Use ESP_LOG liberally during development.
4. **Check Errors**: Always verify return codes from functions.
5. **Read Docs**: ESP-IDF docs are comprehensive - use them.
6. **Use Examples**: ESP-IDF examples are high quality references.
7. **Ask for Help**: ESP32 community is friendly and active.
8. **Be Patient**: Embedded systems are complex - learning takes time.

## 📞 Getting Help

1. **Documentation**: Check this documentation first
2. **ESP-IDF Examples**: Look for similar example code
3. **Serial Logs**: Enable verbose logging for debugging
4. **Forums**: 
   - https://esp32.com/
   - https://community.platformio.org/
5. **GitHub Issues**: Check existing issues on ESP-IDF repo
6. **Discord**: ESP32 community Discord servers

## 🎉 Success Criteria

You'll know you're successful when:

- ✅ Pendant records voice to SD card
- ✅ Files play back clearly on PC
- ✅ Only records during speech (VAD works)
- ✅ Runs reliably for hours
- ✅ LED indicates current state
- ✅ Handles errors gracefully

**You'll have built a complete audio recording system from scratch!**

---

## 📝 Notes

- This is Phase 1 of the overall Pendant project (see Linear issue MYR-241)
- Future phases will add Bluetooth, ultrasonic detection, and phone app
- Focus on getting audio capture working first - other features later
- Document your progress and learnings as you go

Good luck! 🚀
