# Super Summariser Ultra Pro Max

## Flow

```mermaid
---
id: d22fae4c-efa7-404f-b1df-2437f43e1477
config:
  theme: neo-dark
  look: neo
  layout: elk
---
flowchart TB
    entryPoint("fa:fa-play Entry Point")
    entryPoint --> detectInstructions["fa:fa-question-circle Are instructions being given?"]
    detectInstructions -->|Yes| instructionsMain["fa:fa-magnifying-glass Are instructions the main focus?"]
    instructionsMain -->|Yes| instructMode("fa:fa-chalkboard-teacher Instruction Mode")
    detectInstructions -->|No| converseMode("fa:fa-comments Conversation Mode")
    instructionsMain -->|No| converseMode
    instructMode --> endPoint("fa:fa-flag-checkered End Point")
    converseMode --> endPoint
```
