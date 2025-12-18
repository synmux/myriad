# ESP-IDF Components

Custom components for the Pendant audio capture system.

## Structure

Each component should follow this structure:

```
components/
└── component_name/
    ├── CMakeLists.txt        # Build configuration
    ├── Kconfig               # Configuration options (optional)
    ├── include/
    │   └── component_name.h  # Public API header
    ├── src/
    │   └── component_name.c  # Implementation
    └── test/
        └── test_component.c  # Unit tests (optional)
```

## Example Component

### CMakeLists.txt

```cmake
idf_component_register(
    SRCS "src/audio_capture.c"
    INCLUDE_DIRS "include"
    REQUIRES driver esp_system freertos
)
```

### include/audio_capture.h

```c
#ifndef AUDIO_CAPTURE_H
#define AUDIO_CAPTURE_H

#include "esp_err.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Initialize audio capture subsystem
 * @return ESP_OK on success
 */
esp_err_t audio_capture_init(void);

/**
 * Start recording audio
 * @return ESP_OK on success
 */
esp_err_t audio_capture_start(void);

/**
 * Stop recording audio
 * @return ESP_OK on success
 */
esp_err_t audio_capture_stop(void);

#ifdef __cplusplus
}
#endif

#endif // AUDIO_CAPTURE_H
```

### src/audio_capture.c

```c
#include "audio_capture.h"
#include "esp_log.h"

static const char *TAG = "AUDIO_CAPTURE";

esp_err_t audio_capture_init(void) {
    ESP_LOGI(TAG, "Initializing audio capture");
    // Implementation here
    return ESP_OK;
}

esp_err_t audio_capture_start(void) {
    ESP_LOGI(TAG, "Starting audio capture");
    // Implementation here
    return ESP_OK;
}

esp_err_t audio_capture_stop(void) {
    ESP_LOGI(TAG, "Stopping audio capture");
    // Implementation here
    return ESP_OK;
}
```

## Planned Components

### 1. audio_capture
**Purpose**: I2S audio input from SPM1423 microphone

**API**:
- `audio_capture_init()` - Configure I2S peripheral
- `audio_capture_start()` - Begin DMA transfers
- `audio_capture_stop()` - Stop capture
- `audio_capture_read()` - Get audio samples
- `audio_capture_set_callback()` - Set callback for new data

**Dependencies**: `driver`, `freertos`

---

### 2. audio_processing
**Purpose**: Digital signal processing (filters, VAD)

**API**:
- `audio_processing_init()` - Initialize DSP components
- `hpf_process()` - High-pass filter
- `lpf_process()` - Low-pass filter (future)
- `vad_process()` - Voice activity detection
- `noise_gate_process()` - Noise gate (future)

**Dependencies**: None (pure math)

---

### 3. sd_storage
**Purpose**: SD card file management

**API**:
- `sd_storage_init()` - Mount SD card
- `sd_storage_create_file()` - Create new recording file
- `sd_storage_write()` - Write audio data
- `sd_storage_close_file()` - Finalize file
- `sd_storage_list_files()` - Get recording list
- `sd_storage_delete_old()` - Clean up old files

**Dependencies**: `fatfs`, `sdmmc`, `driver`

---

### 4. wav_format
**Purpose**: WAV file format encoding/decoding

**API**:
- `wav_write_header()` - Write WAV header
- `wav_update_header()` - Update sizes after recording
- `wav_validate()` - Check WAV file integrity
- `wav_get_info()` - Read file metadata

**Dependencies**: None (pure formatting)

---

### 5. power_mgmt
**Purpose**: Battery optimization and power management

**API**:
- `power_mgmt_init()` - Configure power settings
- `power_mgmt_sleep()` - Enter low-power mode
- `power_mgmt_wake()` - Resume from sleep
- `power_mgmt_get_battery()` - Read battery level

**Dependencies**: `esp_pm`, `driver`

---

### 6. ultrasonic (Future)
**Purpose**: Detect ultrasonic suppression signals

**API**:
- `ultrasonic_init()` - Configure detection
- `ultrasonic_start()` - Begin monitoring
- `ultrasonic_is_detected()` - Check if signal present
- `ultrasonic_get_source()` - Identify which device

**Dependencies**: `audio_capture`, `fft` library

---

### 7. bluetooth_transfer (Future)
**Purpose**: BLE file transfer to phone

**API**:
- `bt_transfer_init()` - Initialize BLE stack
- `bt_transfer_connect()` - Connect to phone
- `bt_transfer_send_file()` - Send recording
- `bt_transfer_get_status()` - Check transfer progress

**Dependencies**: `esp_bt`, `nimble`

---

## Creating a New Component

1. **Create directory structure**:
   ```bash
   mkdir -p components/my_component/{include,src,test}
   ```

2. **Create CMakeLists.txt**:
   ```cmake
   idf_component_register(
       SRCS "src/my_component.c"
       INCLUDE_DIRS "include"
       REQUIRES <dependencies>
   )
   ```

3. **Create header** in `include/my_component.h`:
   - Add include guards
   - Declare public API
   - Add documentation comments

4. **Implement** in `src/my_component.c`:
   - Include header
   - Implement functions
   - Add logging

5. **Test**:
   - Use in main.c
   - Verify functionality
   - Add unit tests if complex

## Best Practices

1. **Single Responsibility**: Each component does one thing well
2. **Clear API**: Public functions in header, internal functions static
3. **Error Handling**: Always return `esp_err_t`, check return values
4. **Logging**: Use ESP_LOG macros with unique TAG
5. **Resource Management**: Initialize in `_init()`, cleanup in `_deinit()`
6. **Documentation**: Comment public functions with purpose, params, returns
7. **Thread Safety**: Use mutexes if component will be called from multiple tasks

## Dependencies

Components can depend on:
- ESP-IDF components (driver, freertos, esp_system, etc.)
- Other custom components
- Third-party libraries (added via `lib_deps` in platformio.ini)

Declare dependencies in `CMakeLists.txt`:

```cmake
idf_component_register(
    SRCS "src/my_component.c"
    INCLUDE_DIRS "include"
    REQUIRES driver freertos    # ESP-IDF components
    PRIV_REQUIRES other_comp    # Private dependency
)
```

## Further Reading

- [ESP-IDF Component System](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-guides/build-system.html#component-cmakelists-files)
- [Component Configuration (Kconfig)](https://docs.espressif.com/projects/esp-idf/en/latest/esp32s3/api-reference/kconfig.html)
