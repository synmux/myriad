/**
 * M5 Capsule Audio Recorder - Main Application
 * 
 * Captures audio from SPM1423 MEMS microphone via I2S and records to SD card.
 * Implements voice activity detection and high-pass filtering.
 */

#include <stdio.h>
#include <string.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_log.h"
#include "esp_system.h"
#include "driver/gpio.h"

static const char *TAG = "MAIN";

// Pin definitions for M5 Capsule
#define LED_GPIO GPIO_NUM_21

/**
 * Initialize basic system components
 */
void system_init(void) {
    ESP_LOGI(TAG, "M5 Capsule Audio Recorder v0.1.0");
    ESP_LOGI(TAG, "ESP-IDF Version: %s", esp_get_idf_version());
    ESP_LOGI(TAG, "Chip: %s", CONFIG_IDF_TARGET);
    
    // Print chip info
    esp_chip_info_t chip_info;
    esp_chip_info(&chip_info);
    ESP_LOGI(TAG, "Cores: %d", chip_info.cores);
    ESP_LOGI(TAG, "Flash: %dMB %s", 
             spi_flash_get_chip_size() / (1024 * 1024),
             (chip_info.features & CHIP_FEATURE_EMB_FLASH) ? "embedded" : "external");
    
    // Configure LED GPIO
    gpio_reset_pin(LED_GPIO);
    gpio_set_direction(LED_GPIO, GPIO_MODE_OUTPUT);
    
    ESP_LOGI(TAG, "System initialization complete");
}

/**
 * Main application entry point
 */
void app_main(void) {
    system_init();
    
    ESP_LOGI(TAG, "Starting LED blink test...");
    ESP_LOGI(TAG, "Next step: Implement SD card initialization");
    ESP_LOGI(TAG, "See PENDANT-LEARNING-PATHWAY.md for guidance");
    
    // Simple blink to verify system is working
    while (1) {
        gpio_set_level(LED_GPIO, 1);
        ESP_LOGI(TAG, "LED ON");
        vTaskDelay(pdMS_TO_TICKS(1000));
        
        gpio_set_level(LED_GPIO, 0);
        ESP_LOGI(TAG, "LED OFF");
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}
