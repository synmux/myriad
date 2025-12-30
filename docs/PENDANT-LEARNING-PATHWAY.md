# Pendant Audio Capture Learning Pathway

## ESP-IDF via PlatformIO for M5 Capsule (ESP32-S3)

> **Goal**: Build audio capture to SD card functionality for the M5 Capsule pendant device

---

## 📋 Prerequisites

### Hardware

- **M5 Capsule** ([M5Stack Capsule Kit with M5StampS3](https://shop.m5stack.com/products/m5stack-capsule-kit-w-m5stamps3))
  - ESP32-S3 (dual-core, 240MHz)
  - Built-in SPM1423 MEMS microphone (I2S interface)
  - microSD card slot (SPI interface)
  - USB-C for programming/power
  - Battery support (optional)

### Software

- PlatformIO IDE (VS Code extension recommended)
- Python 3.7+ (for esptool)
- Git

### Knowledge Baseline

- Basic C/C++ programming
- Understanding of embedded systems concepts (GPIO, interrupts, peripherals)
- Familiarity with command line/terminal

---

## 🎯 Learning Pathway Structure

This pathway is divided into progressive milestones. Complete each before moving to the next.

---

## **Phase 1: Environment Setup & Basics** (2-3 days)

### Milestone 1.1: PlatformIO + ESP-IDF Setup

**Goal**: Get a "Hello World" running on the M5 Capsule

#### Steps:

1. **Install PlatformIO**

   ```bash
   # Install VS Code extension "PlatformIO IDE"
   # Or via CLI:
   pip install platformio
   ```

2. **Create First Project**

   ```bash
   mkdir pendant-audio-capture
   cd pendant-audio-capture
   pio init --board esp32-s3-devkitc-1
   ```

3. **Configure `platformio.ini`**

   ```ini
   [env:m5stack-capsule]
   platform = espressif32
   board = esp32-s3-devkitc-1
   framework = espidf
   monitor_speed = 115200
   upload_speed = 921600

   ; ESP32-S3 specific
   board_build.mcu = esp32s3
   board_build.f_cpu = 240000000L
   board_build.flash_mode = qio
   board_build.psram_type = opi

   ; Partition for larger apps (audio + SD)
   board_build.partitions = huge_app.csv
   ```

4. **First Program: Blink LED**

   ```c
   // src/main.c
   #include <stdio.h>
   #include "freertos/FreeRTOS.h"
   #include "freertos/task.h"
   #include "driver/gpio.h"

   #define LED_GPIO GPIO_NUM_21  // M5 Capsule LED pin

   void app_main(void) {
       gpio_reset_pin(LED_GPIO);
       gpio_set_direction(LED_GPIO, GPIO_MODE_OUTPUT);

       while(1) {
           gpio_set_level(LED_GPIO, 1);
           vTaskDelay(pdMS_TO_TICKS(1000));
           gpio_set_level(LED_GPIO, 0);
           vTaskDelay(pdMS_TO_TICKS(1000));
           printf("LED toggled\n");
       }
   }
   ```

5. **Build & Flash**
   ```bash
   pio run --target upload --target monitor
   ```

#### Learning Resources:

- [PlatformIO ESP-IDF Tutorial](https://docs.platformio.org/en/latest/frameworks/espidf.html)
- [ESP-IDF Get Started](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/get-started/)
- [M5 Capsule Documentation](https://docs.m5stack.com/en/core/M5Capsule)

#### Success Criteria:

✅ LED blinks at 1Hz
✅ Serial output visible in monitor
✅ Understanding of FreeRTOS tasks and delays

---

### Milestone 1.2: ESP-IDF Component System

**Goal**: Understand ESP-IDF's component architecture and create custom components

#### Concepts to Learn:

1. **Component Structure**

   ```
   components/
   ├── audio_capture/
   │   ├── CMakeLists.txt
   │   ├── include/
   │   │   └── audio_capture.h
   │   └── audio_capture.c
   └── sd_storage/
       ├── CMakeLists.txt
       ├── include/
       │   └── sd_storage.h
       └── sd_storage.c
   ```

2. **CMakeLists.txt Basics**

   ```cmake
   idf_component_register(
       SRCS "audio_capture.c"
       INCLUDE_DIRS "include"
       REQUIRES driver esp_system
   )
   ```

3. **Header Guards & APIs**

   ```c
   // include/audio_capture.h
   #ifndef AUDIO_CAPTURE_H
   #define AUDIO_CAPTURE_H

   #include "esp_err.h"

   esp_err_t audio_init(void);
   esp_err_t audio_start_recording(void);
   esp_err_t audio_stop_recording(void);

   #endif
   ```

#### Practice Exercise:

Create a `logger` component that wraps ESP_LOG with custom formatting.

#### Learning Resources:

- [ESP-IDF Build System](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-guides/build-system.html)
- [Component Architecture](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-guides/build-system.html#component-cmakelists-files)

#### Success Criteria:

✅ Created and integrated a custom component
✅ Understand component dependencies
✅ Can build multi-component projects

---

## **Phase 2: SD Card Integration** (3-4 days)

### Milestone 2.1: SD Card Initialization & File I/O

**Goal**: Mount SD card and perform basic file operations

#### M5 Capsule SD Card Pins:

```c
// SPI pins for M5 Capsule
#define PIN_SD_MISO  GPIO_NUM_4
#define PIN_SD_MOSI  GPIO_NUM_2
#define PIN_SD_CLK   GPIO_NUM_1
#define PIN_SD_CS    GPIO_NUM_3
```

#### Implementation:

```c
#include "esp_vfs_fat.h"
#include "sdmmc_cmd.h"
#include "driver/sdspi_host.h"

#define MOUNT_POINT "/sdcard"

esp_err_t sd_card_init(void) {
    esp_err_t ret;

    // Options for mounting
    esp_vfs_fat_sdmmc_mount_config_t mount_config = {
        .format_if_mount_failed = false,
        .max_files = 5,
        .allocation_unit_size = 16 * 1024
    };

    sdmmc_card_t *card;
    const char mount_point[] = MOUNT_POINT;

    // SPI bus configuration
    sdmmc_host_t host = SDSPI_HOST_DEFAULT();
    host.max_freq_khz = SDMMC_FREQ_HIGHSPEED;

    spi_bus_config_t bus_cfg = {
        .mosi_io_num = PIN_SD_MOSI,
        .miso_io_num = PIN_SD_MISO,
        .sclk_io_num = PIN_SD_CLK,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
        .max_transfer_sz = 4096,
    };

    ret = spi_bus_initialize(host.slot, &bus_cfg, SDSPI_DEFAULT_DMA);
    if (ret != ESP_OK) {
        ESP_LOGE("SD", "Failed to initialize bus.");
        return ret;
    }

    // Slot configuration
    sdspi_device_config_t slot_config = SDSPI_DEVICE_CONFIG_DEFAULT();
    slot_config.gpio_cs = PIN_SD_CS;
    slot_config.host_id = host.slot;

    ret = esp_vfs_fat_sdspi_mount(mount_point, &host, &slot_config,
                                   &mount_config, &card);

    if (ret != ESP_OK) {
        ESP_LOGE("SD", "Failed to mount filesystem.");
        return ret;
    }

    // Print card info
    sdmmc_card_print_info(stdout, card);

    return ESP_OK;
}
```

#### File Operations:

```c
#include <stdio.h>
#include <sys/stat.h>

void test_sd_write(void) {
    FILE *f = fopen("/sdcard/test.txt", "w");
    if (f == NULL) {
        ESP_LOGE("SD", "Failed to open file for writing");
        return;
    }
    fprintf(f, "Hello from M5 Capsule!\n");
    fclose(f);
    ESP_LOGI("SD", "File written successfully");

    // Read back
    f = fopen("/sdcard/test.txt", "r");
    if (f == NULL) {
        ESP_LOGE("SD", "Failed to open file for reading");
        return;
    }
    char line[128];
    fgets(line, sizeof(line), f);
    fclose(f);
    ESP_LOGI("SD", "Read: %s", line);
}
```

#### Learning Resources:

- [ESP-IDF SD Card Example](https://github.com/espressif/esp-idf/tree/master/examples/storage/sd_card)
- [FAT Filesystem API](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/storage/fatfs.html)

#### Success Criteria:

✅ SD card mounts successfully
✅ Can create, write, read, and delete files
✅ Understand SPI vs SDMMC modes
✅ Handle error cases (no card, full card, etc.)

---

### Milestone 2.2: Binary Data & WAV File Format

**Goal**: Write audio data in WAV format

#### WAV Header Structure:

```c
typedef struct {
    // RIFF Header
    char riff_header[4];      // "RIFF"
    uint32_t wav_size;        // File size - 8
    char wave_header[4];      // "WAVE"

    // Format Header
    char fmt_header[4];       // "fmt "
    uint32_t fmt_chunk_size;  // 16 for PCM
    uint16_t audio_format;    // 1 for PCM
    uint16_t num_channels;    // 1 for mono, 2 for stereo
    uint32_t sample_rate;     // 16000, 44100, etc.
    uint32_t byte_rate;       // sample_rate * num_channels * bits_per_sample/8
    uint16_t block_align;     // num_channels * bits_per_sample/8
    uint16_t bits_per_sample; // 16, 24, 32

    // Data Header
    char data_header[4];      // "data"
    uint32_t data_bytes;      // Size of audio data
} wav_header_t;

void write_wav_header(FILE *f, uint32_t sample_rate, uint16_t bits_per_sample,
                      uint16_t channels) {
    wav_header_t header = {0};

    memcpy(header.riff_header, "RIFF", 4);
    memcpy(header.wave_header, "WAVE", 4);
    memcpy(header.fmt_header, "fmt ", 4);
    memcpy(header.data_header, "data", 4);

    header.fmt_chunk_size = 16;
    header.audio_format = 1; // PCM
    header.num_channels = channels;
    header.sample_rate = sample_rate;
    header.bits_per_sample = bits_per_sample;
    header.byte_rate = sample_rate * channels * bits_per_sample / 8;
    header.block_align = channels * bits_per_sample / 8;

    // Will be updated when closing file
    header.wav_size = 36; // Minimum size
    header.data_bytes = 0;

    fwrite(&header, sizeof(wav_header_t), 1, f);
}

void update_wav_header(FILE *f, uint32_t data_size) {
    fseek(f, 4, SEEK_SET);
    uint32_t wav_size = data_size + 36;
    fwrite(&wav_size, sizeof(uint32_t), 1, f);

    fseek(f, 40, SEEK_SET);
    fwrite(&data_size, sizeof(uint32_t), 1, f);
}
```

#### Practice Exercise:

1. Generate a sine wave in memory
2. Write it as a WAV file to SD card
3. Verify with audio software on PC

#### Success Criteria:

✅ Can generate valid WAV files
✅ Files play correctly on PC
✅ Understand PCM audio format

---

## **Phase 3: I2S Audio Capture** (4-5 days)

### Milestone 3.1: I2S Basics & Configuration

**Goal**: Understand I2S protocol and capture raw audio data

#### I2S Protocol Overview:

- **I2S**: Inter-IC Sound (digital audio interface)
- **Key Signals**:
  - **BCLK** (Bit Clock): Timing for each bit
  - **WS** (Word Select/LRCLK): Left/Right channel selection
  - **SD** (Serial Data): Actual audio data
  - **MCLK** (Master Clock): Optional, for ADC/DAC

#### M5 Capsule Microphone (SPM1423):

```c
// I2S pins for M5 Capsule SPM1423 microphone
#define I2S_MIC_SERIAL_CLOCK  GPIO_NUM_5
#define I2S_MIC_SERIAL_DATA   GPIO_NUM_6
#define I2S_MIC_LEFT_RIGHT_CLK GPIO_NUM_7
```

#### I2S Configuration:

```c
#include "driver/i2s_std.h"

#define SAMPLE_RATE     16000
#define I2S_NUM         I2S_NUM_0
#define DMA_BUF_COUNT   8
#define DMA_BUF_LEN     1024

i2s_chan_handle_t rx_handle;

esp_err_t i2s_mic_init(void) {
    i2s_chan_config_t chan_cfg = I2S_CHANNEL_DEFAULT_CONFIG(I2S_NUM, I2S_ROLE_MASTER);
    chan_cfg.dma_desc_num = DMA_BUF_COUNT;
    chan_cfg.dma_frame_num = DMA_BUF_LEN;

    esp_err_t ret = i2s_new_channel(&chan_cfg, NULL, &rx_handle);
    if (ret != ESP_OK) {
        ESP_LOGE("I2S", "Failed to create I2S channel");
        return ret;
    }

    i2s_std_config_t std_cfg = {
        .clk_cfg = I2S_STD_CLK_DEFAULT_CONFIG(SAMPLE_RATE),
        .slot_cfg = I2S_STD_MSB_SLOT_DEFAULT_CONFIG(I2S_DATA_BIT_WIDTH_32BIT, I2S_SLOT_MODE_MONO),
        .gpio_cfg = {
            .mclk = I2S_GPIO_UNUSED,
            .bclk = I2S_MIC_SERIAL_CLOCK,
            .ws = I2S_MIC_LEFT_RIGHT_CLK,
            .dout = I2S_GPIO_UNUSED,
            .din = I2S_MIC_SERIAL_DATA,
            .invert_flags = {
                .mclk_inv = false,
                .bclk_inv = false,
                .ws_inv = false,
            },
        },
    };

    ret = i2s_channel_init_std_mode(rx_handle, &std_cfg);
    if (ret != ESP_OK) {
        ESP_LOGE("I2S", "Failed to initialize I2S standard mode");
        return ret;
    }

    ret = i2s_channel_enable(rx_handle);
    if (ret != ESP_OK) {
        ESP_LOGE("I2S", "Failed to enable I2S channel");
        return ret;
    }

    ESP_LOGI("I2S", "I2S microphone initialized");
    return ESP_OK;
}
```

#### Reading Audio Data:

```c
#define READ_BUF_SIZE 4096

void i2s_read_task(void *param) {
    int32_t *i2s_read_buff = (int32_t *)calloc(READ_BUF_SIZE, sizeof(int32_t));
    size_t bytes_read = 0;

    while (1) {
        esp_err_t ret = i2s_channel_read(rx_handle, i2s_read_buff,
                                         READ_BUF_SIZE * sizeof(int32_t),
                                         &bytes_read, portMAX_DELAY);

        if (ret == ESP_OK && bytes_read > 0) {
            // Process audio data
            int samples_read = bytes_read / sizeof(int32_t);
            ESP_LOGI("I2S", "Read %d samples", samples_read);

            // Example: Print first sample
            ESP_LOGI("I2S", "Sample[0]: %ld", i2s_read_buff[0]);
        }

        vTaskDelay(pdMS_TO_TICKS(10));
    }

    free(i2s_read_buff);
}
```

#### Learning Resources:

- [ESP-IDF I2S Driver](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/peripherals/i2s.html)
- [I2S Protocol Explained](https://www.sparkfun.com/datasheets/BreakoutBoards/I2SBUS.pdf)
- [ESP32-S3 I2S Examples](https://github.com/espressif/esp-idf/tree/master/examples/peripherals/i2s)

#### Practice Exercise:

1. Read audio samples continuously
2. Calculate and print average amplitude every second
3. Detect silence vs. sound

#### Success Criteria:

✅ I2S successfully reads from microphone
✅ Can see varying values when making sounds
✅ Understand bit depth and sample rate concepts

---

### Milestone 3.2: Audio Processing & Filtering

**Goal**: Implement voice frequency filtering and noise reduction

#### Concepts:

1. **Voice Frequency Range**: ~300Hz - 3400Hz (telephone quality) or ~80Hz - 8000Hz (wideband)
2. **Simple High-Pass Filter**: Remove DC offset and low-frequency noise
3. **Amplitude Detection**: Determine if someone is speaking

#### Basic High-Pass Filter:

```c
typedef struct {
    float alpha;
    int32_t prev_input;
    int32_t prev_output;
} high_pass_filter_t;

void hpf_init(high_pass_filter_t *filter, float cutoff_freq, float sample_rate) {
    float rc = 1.0f / (2.0f * M_PI * cutoff_freq);
    float dt = 1.0f / sample_rate;
    filter->alpha = rc / (rc + dt);
    filter->prev_input = 0;
    filter->prev_output = 0;
}

int32_t hpf_process(high_pass_filter_t *filter, int32_t input) {
    int32_t output = filter->alpha * (filter->prev_output + input - filter->prev_input);
    filter->prev_input = input;
    filter->prev_output = output;
    return output;
}
```

#### Voice Activity Detection (Simple):

```c
typedef struct {
    int32_t threshold;
    int32_t window_size;
    int32_t *energy_window;
    int window_index;
    bool is_speaking;
} vad_t;

void vad_init(vad_t *vad, int32_t threshold, int32_t window_size) {
    vad->threshold = threshold;
    vad->window_size = window_size;
    vad->energy_window = (int32_t *)calloc(window_size, sizeof(int32_t));
    vad->window_index = 0;
    vad->is_speaking = false;
}

bool vad_process(vad_t *vad, int32_t *samples, int num_samples) {
    // Calculate RMS energy
    int64_t sum = 0;
    for (int i = 0; i < num_samples; i++) {
        int32_t sample = samples[i] >> 16; // Convert from 32-bit to 16-bit
        sum += (int64_t)sample * sample;
    }
    int32_t rms = sqrt(sum / num_samples);

    // Update sliding window
    vad->energy_window[vad->window_index] = rms;
    vad->window_index = (vad->window_index + 1) % vad->window_size;

    // Calculate average energy
    int64_t avg_energy = 0;
    for (int i = 0; i < vad->window_size; i++) {
        avg_energy += vad->energy_window[i];
    }
    avg_energy /= vad->window_size;

    // Determine if speaking
    vad->is_speaking = (avg_energy > vad->threshold);
    return vad->is_speaking;
}
```

#### Learning Resources:

- [Digital Signal Processing Basics](https://www.analog.com/en/design-center/landing-pages/001/beginners-guide-to-dsp.html)
- [Voice Activity Detection Overview](https://en.wikipedia.org/wiki/Voice_activity_detection)

#### Success Criteria:

✅ Filter removes DC offset and low-frequency noise
✅ VAD accurately detects speech vs. silence
✅ Understand trade-offs between false positives/negatives

---

## **Phase 4: Integration** (5-7 days)

### Milestone 4.1: Audio Recording State Machine

**Goal**: Create a robust state machine for recording lifecycle

#### States:

1. **IDLE**: Waiting to start recording
2. **RECORDING**: Actively capturing audio
3. **PAUSED**: Temporarily stopped (ultrasonic detected)
4. **STOPPED**: Recording complete, writing to SD

#### Implementation:

```c
typedef enum {
    AUDIO_STATE_IDLE,
    AUDIO_STATE_RECORDING,
    AUDIO_STATE_PAUSED,
    AUDIO_STATE_STOPPED
} audio_state_t;

typedef struct {
    audio_state_t state;
    FILE *wav_file;
    uint32_t samples_recorded;
    uint32_t recording_id;
    high_pass_filter_t hpf;
    vad_t vad;
    SemaphoreHandle_t state_mutex;
} audio_recorder_t;

void audio_state_transition(audio_recorder_t *rec, audio_state_t new_state) {
    xSemaphoreTake(rec->state_mutex, portMAX_DELAY);

    ESP_LOGI("AUDIO", "State transition: %d -> %d", rec->state, new_state);

    switch (new_state) {
        case AUDIO_STATE_RECORDING:
            if (rec->state == AUDIO_STATE_IDLE) {
                // Create new file
                char filename[64];
                snprintf(filename, sizeof(filename),
                         "/sdcard/rec_%lu.wav", rec->recording_id++);
                rec->wav_file = fopen(filename, "wb");
                if (rec->wav_file) {
                    write_wav_header(rec->wav_file, SAMPLE_RATE, 16, 1);
                    rec->samples_recorded = 0;
                    ESP_LOGI("AUDIO", "Started recording: %s", filename);
                }
            }
            break;

        case AUDIO_STATE_STOPPED:
            if (rec->wav_file) {
                update_wav_header(rec->wav_file, rec->samples_recorded * 2);
                fclose(rec->wav_file);
                rec->wav_file = NULL;
                ESP_LOGI("AUDIO", "Stopped recording. Samples: %lu",
                         rec->samples_recorded);
            }
            break;

        case AUDIO_STATE_PAUSED:
            ESP_LOGI("AUDIO", "Recording paused (ultrasonic detected)");
            break;

        default:
            break;
    }

    rec->state = new_state;
    xSemaphoreGive(rec->state_mutex);
}
```

#### Success Criteria:

✅ State machine handles all transitions correctly
✅ Files are properly closed and headers updated
✅ Thread-safe state management

---

### Milestone 4.2: Complete Audio Recording System

**Goal**: Integrate all components into a working system

#### Main Recording Task:

```c
#define RECORDING_CHUNK_SIZE 1024

void audio_recording_task(void *param) {
    audio_recorder_t *rec = (audio_recorder_t *)param;

    int32_t *i2s_buffer = (int32_t *)calloc(RECORDING_CHUNK_SIZE, sizeof(int32_t));
    int16_t *wav_buffer = (int16_t *)calloc(RECORDING_CHUNK_SIZE, sizeof(int16_t));

    size_t bytes_read = 0;

    while (1) {
        // Read from I2S
        esp_err_t ret = i2s_channel_read(rx_handle, i2s_buffer,
                                         RECORDING_CHUNK_SIZE * sizeof(int32_t),
                                         &bytes_read, portMAX_DELAY);

        if (ret != ESP_OK || bytes_read == 0) {
            continue;
        }

        int samples = bytes_read / sizeof(int32_t);

        // Process samples
        for (int i = 0; i < samples; i++) {
            // Apply high-pass filter
            int32_t filtered = hpf_process(&rec->hpf, i2s_buffer[i]);

            // Convert 32-bit to 16-bit
            wav_buffer[i] = (int16_t)(filtered >> 16);
        }

        // Voice activity detection
        bool is_speaking = vad_process(&rec->vad, i2s_buffer, samples);

        xSemaphoreTake(rec->state_mutex, portMAX_DELAY);
        audio_state_t current_state = rec->state;
        xSemaphoreGive(rec->state_mutex);

        // Write to file if recording and speaking
        if (current_state == AUDIO_STATE_RECORDING && is_speaking) {
            if (rec->wav_file) {
                size_t written = fwrite(wav_buffer, sizeof(int16_t), samples,
                                       rec->wav_file);
                rec->samples_recorded += written;

                // Periodic flush to ensure data is written
                if (rec->samples_recorded % (SAMPLE_RATE * 5) == 0) {
                    fflush(rec->wav_file);
                    ESP_LOGI("AUDIO", "Recorded %lu seconds",
                            rec->samples_recorded / SAMPLE_RATE);
                }
            }
        }
    }

    free(i2s_buffer);
    free(wav_buffer);
}
```

#### Complete System Initialization:

```c
void app_main(void) {
    ESP_LOGI("MAIN", "M5 Capsule Audio Recorder Starting...");

    // Initialize SD card
    esp_err_t ret = sd_card_init();
    if (ret != ESP_OK) {
        ESP_LOGE("MAIN", "SD card initialization failed");
        return;
    }

    // Initialize I2S microphone
    ret = i2s_mic_init();
    if (ret != ESP_OK) {
        ESP_LOGE("MAIN", "I2S initialization failed");
        return;
    }

    // Initialize audio recorder
    audio_recorder_t recorder = {0};
    recorder.state = AUDIO_STATE_IDLE;
    recorder.recording_id = 0;
    recorder.state_mutex = xSemaphoreCreateMutex();

    hpf_init(&recorder.hpf, 80.0f, SAMPLE_RATE);  // 80 Hz cutoff
    vad_init(&recorder.vad, 500, 10);  // Threshold and window size

    // Start recording task
    xTaskCreate(audio_recording_task, "audio_record", 8192, &recorder, 5, NULL);

    // Start recording
    vTaskDelay(pdMS_TO_TICKS(1000));
    audio_state_transition(&recorder, AUDIO_STATE_RECORDING);

    // Record for 10 seconds (example)
    vTaskDelay(pdMS_TO_TICKS(10000));
    audio_state_transition(&recorder, AUDIO_STATE_STOPPED);

    ESP_LOGI("MAIN", "Recording complete");

    while (1) {
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
```

#### Testing Checklist:

- [ ] Records audio to SD card
- [ ] WAV file plays correctly on PC
- [ ] Voice activity detection filters silence
- [ ] Can record multiple sessions
- [ ] Handles SD card removal gracefully
- [ ] Memory usage is stable (no leaks)

#### Success Criteria:

✅ Complete end-to-end recording works
✅ Audio quality is acceptable for speech
✅ System runs stably for extended periods
✅ File management works correctly

---

## **Phase 5: Optimization & Features** (3-4 days)

### Milestone 5.1: Power Management

**Goal**: Optimize for battery operation

#### Techniques:

1. **Dynamic Frequency Scaling**: Lower CPU frequency when idle
2. **Light Sleep**: Between recordings
3. **I2S Power Down**: Disable when not recording

```c
#include "esp_pm.h"

void power_management_init(void) {
    esp_pm_config_t pm_config = {
        .max_freq_mhz = 240,
        .min_freq_mhz = 80,
        .light_sleep_enable = true
    };
    esp_pm_configure(&pm_config);
}
```

---

### Milestone 5.2: File Management

**Goal**: Automatic file rotation, deletion of old files

#### Features:

- Timestamp-based filenames
- Maximum storage limit
- Automatic cleanup

```c
#include "esp_sntp.h"
#include <time.h>

void generate_timestamped_filename(char *buffer, size_t size) {
    time_t now;
    struct tm timeinfo;
    time(&now);
    localtime_r(&now, &timeinfo);

    strftime(buffer, size, "/sdcard/rec_%Y%m%d_%H%M%S.wav", &timeinfo);
}
```

---

### Milestone 5.3: Status Indicators

**Goal**: LED patterns for different states

```c
void led_task(void *param) {
    audio_recorder_t *rec = (audio_recorder_t *)param;

    while (1) {
        xSemaphoreTake(rec->state_mutex, portMAX_DELAY);
        audio_state_t state = rec->state;
        xSemaphoreGive(rec->state_mutex);

        switch (state) {
            case AUDIO_STATE_IDLE:
                // Slow pulse
                gpio_set_level(LED_GPIO, 1);
                vTaskDelay(pdMS_TO_TICKS(2000));
                gpio_set_level(LED_GPIO, 0);
                vTaskDelay(pdMS_TO_TICKS(2000));
                break;

            case AUDIO_STATE_RECORDING:
                // Fast blink
                gpio_set_level(LED_GPIO, 1);
                vTaskDelay(pdMS_TO_TICKS(200));
                gpio_set_level(LED_GPIO, 0);
                vTaskDelay(pdMS_TO_TICKS(200));
                break;

            case AUDIO_STATE_PAUSED:
                // Solid on
                gpio_set_level(LED_GPIO, 1);
                vTaskDelay(pdMS_TO_TICKS(100));
                break;

            default:
                vTaskDelay(pdMS_TO_TICKS(100));
                break;
        }
    }
}
```

---

## **Phase 6: Future Extensions** (Next Steps)

### Bluetooth Transfer (Future)

- BLE GATT service for file transfer
- Nordic UART Service (NUS) protocol
- Pairing with phone app

### Ultrasonic Detection (Future)

- Additional microphone or use existing with FFT
- Frequency detection (~20kHz range)
- Coded signals for device identification

---

## 📚 **Essential References**

### Documentation

- [M5 Capsule Docs](https://docs.m5stack.com/en/core/M5Capsule)
- [ESP32-S3 Technical Reference](https://www.espressif.com/sites/default/files/documentation/esp32-s3_technical_reference_manual_en.pdf)
- [ESP-IDF Programming Guide](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/)
- [PlatformIO ESP32 Docs](https://docs.platformio.org/en/latest/platforms/espressif32.html)

### Code Examples

- [ESP-IDF Examples Repository](https://github.com/espressif/esp-idf/tree/master/examples)
- [M5Stack Community Examples](https://github.com/m5stack/M5Unified/tree/master/examples)

### Tools

- [Audacity](https://www.audacityteam.org/) - For analyzing WAV files
- [esptool.py](https://github.com/espressif/esptool) - Flash tool
- [Logic Analyzer](https://www.saleae.com/) - For I2S debugging (if available)

---

## 🎯 **Success Metrics**

By the end of this pathway, you should be able to:

1. ✅ Configure ESP-IDF projects using PlatformIO
2. ✅ Interface with SPI peripherals (SD card)
3. ✅ Capture audio using I2S protocol
4. ✅ Process audio data in real-time
5. ✅ Manage files and storage efficiently
6. ✅ Debug embedded systems issues
7. ✅ Write production-quality embedded code
8. ✅ Have a working pendant that records voice to SD card

---

## 💡 **Tips for Success**

1. **Start Simple**: Get each component working independently before integration
2. **Use Serial Logging**: ESP_LOG is your friend - log everything during development
3. **Check Return Values**: Always check `esp_err_t` return values
4. **Memory Management**: Use `heap_caps_get_free_size()` to monitor memory
5. **DMA Buffers**: Ensure they're in correct memory region (DRAM)
6. **Test Incrementally**: Add one feature at a time
7. **Hardware First**: If something doesn't work, verify hardware with oscilloscope/logic analyzer
8. **Community Help**: ESP32 community is active on forums and Discord

---

## 🚀 **Next Steps**

Once you complete this pathway:

1. Add Bluetooth LE for phone communication
2. Implement ultrasonic detection for TV/music filtering
3. Create phone companion app
4. Set up local Whisper processing
5. Build additional capture devices (desktop unit)

Good luck! 🎉
