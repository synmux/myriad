import json

import plotly.graph_objects as go

# Data - all 11 chips
data = {
    "chips": [
        {
            "name": "nRF52805",
            "cpu": "Cortex-M4",
            "clock": "64 MHz",
            "flash": "192 KB",
            "ram": "24 KB",
            "features": "BLE 5.4, minimal peripherals",
            "useCase": "Simple beacons",
        },
        {
            "name": "nRF52810",
            "cpu": "Cortex-M4",
            "clock": "64 MHz",
            "flash": "192 KB",
            "ram": "24 KB",
            "features": "BLE 5.4, ADC, PWM",
            "useCase": "Simple sensor nodes",
        },
        {
            "name": "nRF52820",
            "cpu": "Cortex-M4",
            "clock": "64 MHz",
            "flash": "256 KB",
            "ram": "32 KB",
            "features": "BLE 5.4, USB, QSPI",
            "useCase": "USB-enabled BLE devices",
        },
        {
            "name": "nRF52832",
            "cpu": "Cortex-M4 + FPU",
            "clock": "64 MHz",
            "flash": "512 KB",
            "ram": "64 KB",
            "features": "BLE 5.4, NFC, Mesh",
            "useCase": "Consumer electronics",
        },
        {
            "name": "nRF52833",
            "cpu": "Cortex-M4 + FPU",
            "clock": "64 MHz",
            "flash": "512 KB",
            "ram": "128 KB",
            "features": "BLE 5.4, Direction Finding, USB",
            "useCase": "Asset tracking, location",
        },
        {
            "name": "nRF52840",
            "cpu": "Cortex-M4 + FPU",
            "clock": "64 MHz",
            "flash": "1 MB",
            "ram": "256 KB",
            "features": "BLE 5.4, USB, QSPI, all protocols",
            "useCase": "High-feature applications",
        },
        {
            "name": "nRF5340",
            "cpu": "Dual Cortex-M33 + 64MHz M33",
            "clock": "128/64 MHz",
            "flash": "1 MB + 256 KB",
            "ram": "512 KB + 64 KB",
            "features": "BLE 5.3, dual-core, QSPI, Thread",
            "useCase": "Complex multi-protocol apps",
        },
        {
            "name": "nRF54L05",
            "cpu": "Cortex-M33 + RISC-V",
            "clock": "128 MHz",
            "flash": "500 KB RRAM",
            "ram": "96 KB",
            "features": "BLE 6.0, RRAM, software peripherals",
            "useCase": "Low-power beacons",
        },
        {
            "name": "nRF54L10",
            "cpu": "Cortex-M33 + RISC-V",
            "clock": "128 MHz",
            "flash": "1 MB RRAM",
            "ram": "256 KB",
            "features": "BLE 6.0, RRAM, balanced",
            "useCase": "Mid-range IoT devices",
        },
        {
            "name": "nRF54L15",
            "cpu": "Cortex-M33 + RISC-V",
            "clock": "128 MHz",
            "flash": "1.5 MB RRAM",
            "ram": "512 KB",
            "features": "BLE 6.0, Thread, Matter, RRAM",
            "useCase": "Complex multi-protocol IoT",
        },
        {
            "name": "nRF54H20",
            "cpu": "Dual Cortex-M33 + RISC-V",
            "clock": "320 MHz",
            "flash": "2 MB",
            "ram": "1 MB",
            "features": "BLE 6.0, ML, 4th gen radio",
            "useCase": "High-performance wireless AI",
        },
    ]
}

# Extract data into columns
chips = data["chips"]
chip_names = [chip["name"] for chip in chips]
cpus = [chip["cpu"] for chip in chips]
clocks = [chip["clock"] for chip in chips]
flash = [chip["flash"] for chip in chips]
ram = [chip["ram"] for chip in chips]
features = [chip["features"] for chip in chips]
use_cases = [chip["useCase"] for chip in chips]

# Verify we have all 11 chips
print(f"Total chips in table: {len(chip_names)}")
print(f"Chip names: {chip_names}")

# Create the table with optimized column widths for better readability
fig = go.Figure(
    data=[
        go.Table(
            columnwidth=[85, 160, 95, 120, 75, 220, 170],  # Optimized widths
            header=dict(
                values=[
                    "<b>Chip Name</b>",
                    "<b>CPU Core</b>",
                    "<b>Clock Speed</b>",
                    "<b>Flash Memory</b>",
                    "<b>RAM</b>",
                    "<b>Key Features</b>",
                    "<b>Primary Use Case</b>",
                ],
                fill_color="#1FB8CD",
                align="left",
                font=dict(color="white", size=13),
                height=42,
                line_color="white",
                line_width=2,
            ),
            cells=dict(
                values=[chip_names, cpus, clocks, flash, ram, features, use_cases],
                fill_color=[
                    [
                        "#f8f9fa" if i % 2 == 0 else "white"
                        for i in range(len(chip_names))
                    ]
                ],
                align="left",
                font=dict(color="#13343B", size=11),
                height=50,  # Increased height for better text display
                line_color="#e0e0e0",
                line_width=1,
            ),
        )
    ]
)

# Update layout
fig.update_layout(
    title={
        "text": "nRF Chip Families: Technical Comparison Matrix<br><span style='font-size: 18px; font-weight: normal;'>Evolution from basic BLE to AI-enabled wireless platforms</span>"
    }
)

# Save as PNG and SVG
fig.write_image("nrf_comparison_table.png")
fig.write_image("nrf_comparison_table.svg", format="svg")

print("Chart saved successfully!")
