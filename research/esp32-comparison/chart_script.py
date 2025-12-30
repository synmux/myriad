import json

# Load the data
data = {
    "architecture_groups": [
        {
            "name": "Xtensa Cores",
            "color": "#ff8c42",
            "chips": ["ESP32", "ESP32-S2", "ESP32-S3", "ESP32-U4"],
        },
        {
            "name": "RISC-V Cores",
            "color": "#4a90e2",
            "chips": [
                "ESP32-C2",
                "ESP32-C3",
                "ESP32-C5",
                "ESP32-C6",
                "ESP32-H2",
                "ESP32-P4",
            ],
        },
    ]
}

# Create mermaid diagram
diagram_code = """
graph TB
    Root[ESP32 Variants]
    
    Xtensa[Xtensa Cores]
    RISCV[RISC-V Cores]
    
    ESP32[ESP32]
    ESP32S2[ESP32-S2]
    ESP32S3[ESP32-S3]
    ESP32U4[ESP32-U4]
    
    ESP32C2[ESP32-C2]
    ESP32C3[ESP32-C3]
    ESP32C5[ESP32-C5]
    ESP32C6[ESP32-C6]
    ESP32H2[ESP32-H2]
    ESP32P4[ESP32-P4]
    
    Root --> Xtensa
    Root --> RISCV
    
    Xtensa --> ESP32
    Xtensa --> ESP32S2
    Xtensa --> ESP32S3
    Xtensa --> ESP32U4
    
    RISCV --> ESP32C2
    RISCV --> ESP32C3
    RISCV --> ESP32C5
    RISCV --> ESP32C6
    RISCV --> ESP32H2
    RISCV --> ESP32P4
    
    classDef xtensaStyle fill:#ff8c42,stroke:#d97335,color:#000
    classDef riscvStyle fill:#4a90e2,stroke:#3a7bc8,color:#fff
    classDef rootStyle fill:#e0e0e0,stroke:#999,color:#000
    
    class Xtensa,ESP32,ESP32S2,ESP32S3,ESP32U4 xtensaStyle
    class RISCV,ESP32C2,ESP32C3,ESP32C5,ESP32C6,ESP32H2,ESP32P4 riscvStyle
    class Root rootStyle
"""

# Create the diagram using the helper function
create_mermaid_diagram(diagram_code, "esp32_variants.png", "esp32_variants.svg")
