# LSR: MIDI Clock to Infrared Synchroniser

## Description

LSR (MIDI Clock Synchroniser and Infrared Relay) is a Python utility that receives MIDI clock messages from a musical instrument or sequencer and uses them to synchronise infrared (IR) transmissions to a compatible device. The tool listens to MIDI timing clock signals, calculates the BPM (beats per minute), and sends coordinated IR commands via a Broadlink infrared transmitter.

This is particularly useful for synchronising external hardware or equipment that responds to infrared control with MIDI-based music systems, allowing tempo-synchronized control of IR-compatible devices.

## Usage

### Basic Invocation

```bash
python lsr.py [MIDI_INPUT_PORT]
```

### Examples

To use the default MIDI input port (typically the first available device):

```bash
python lsr.py
```

To specify a particular MIDI input port:

```bash
python lsr.py 1
```

This will open MIDI port 1 and begin listening for MIDI clock messages.

## CLI Arguments

### Positional Arguments

- `MIDI_INPUT_PORT` (optional, integer)
  - The MIDI input port number to listen on
  - Defaults to `0` (the first available MIDI input device) if not specified
  - Enumeration of available MIDI ports typically starts at 0

## Operation

Once started, the utility performs the following workflow:

1. **Device Discovery**: Searches for an available Broadlink infrared transmitter on the network. The discovery process may take several attempts and uses a 10-second timeout per attempt.

2. **Authentication**: Authenticates with the Broadlink device to establish communication.

3. **MIDI Listening**: Opens the specified MIDI input port and registers a callback function to receive MIDI messages.

4. **Clock Reception**: Listens for MIDI timing clock messages (status byte `0xF8`). These are sent at a rate of 24 pulses per quarter note by standard MIDI devices.

5. **BPM Calculation**: Calculates the tempo in BPM by measuring the interval between successive timing clock messages. A rolling window of the last 24 samples is maintained to smooth the calculation.

6. **Synchronised Transmission**: Transmits infrared commands at each musical beat (every 24 clock ticks) using one of three preprogrammed IR patterns, rotating through a cycle.

7. **Status Reporting**: Prints the current BPM every second, indicating whether synchronisation has been achieved.

## Dependencies

The utility requires the following Python packages:

- **python-broadlink** (`broadlink`)
  - Provides device discovery and IR transmission functionality
  - Repository: https://github.com/mjg59/python-broadlink
  - Used for locating and communicating with Broadlink IR transmitters

- **python-rtmidi** (`rtmidi`)
  - Provides MIDI input capabilities
  - Repository: https://github.com/SpotlightKid/python-rtmidi
  - Used for receiving MIDI clock and control messages

### Installation

```bash
pip install broadlink python-rtmidi
```

## Notable Implementation Details

### MIDI Clock Receiver Class

The `MIDIClockReceiver` class encapsulates the core synchronisation logic:

- **Embedded IR Patterns**: Contains three base64-encoded IR command packets stored as class attributes:
  - `pkt_ptrn`: The primary IR pattern sent on each beat
  - `pkt_30_pc`, `pkt_60_pc`, `pkt_100_pc`: Alternative IR patterns that cycle through (though the cycling may be commented out in the current implementation)

- **Callback Pattern**: The class implements `__call__()` to act as a callable callback function, enabling integration with the `python-rtmidi` callback system.

- **Tempo Tracking**: Uses a deque (double-ended queue) to maintain a rolling window of clock message intervals. The BPM is calculated as `2.5 / (average_interval)`, which is derived from the fact that MIDI clock messages occur at 24 pulses per quarter note.

- **MIDI Message Handling**:
  - `TIMING_CLOCK` (0xF8): Processes tempo and beat information
  - `SONG_START` and `SONG_CONTINUE`: Sets `running = True` to indicate playback has begun
  - `SONG_STOP`: Sets `running = False` to indicate playback has stopped

- **Beat Detection**: A counter tracks every 24th MIDI clock message, which corresponds to one musical beat. When a beat is reached, the `on_beat()` method transmits the primary IR pattern to the Broadlink device.

- **Synchronisation Flag**: The `sync` flag is set to `True` once at least two clock samples have been received, indicating that a reliable BPM reading is available.

### Timing and Synchronisation

- MIDI devices typically send timing clock messages at 24 pulses per quarter note
- The utility only transmits IR commands once every 24 clocks (i.e., once per beat), allowing coarse-grained synchronisation
- The rolling average of clock intervals ensures smooth tempo tracking even with minor timing jitter from the MIDI source

### Logging

The utility uses Python's built-in `logging` module with an INFO level logger named `"midiin_callback"`. Console output includes:

- Device discovery progress messages
- MIDI message status (START, CONTINUE, STOP)
- Real-time BPM updates, with "(no sync)" appended until at least two samples have been collected

### Error Handling

- If MIDI input port opening is interrupted or fails, the utility exits with status code 1
- If the program receives a `KeyboardInterrupt` (Ctrl+C) at any point, it gracefully closes the MIDI input port and exits cleanly
- Broadlink device discovery loops until a device is found, making it resilient to temporary network unavailability

## Troubleshooting

- **"Locating infrared transmitter" takes a long time**: Ensure the Broadlink device is powered on and connected to the network. Discovery may require multiple attempts.
- **No BPM output**: Confirm that the MIDI source is sending timing clock messages and that the correct MIDI port is specified.
- **"no sync" appears indefinitely**: Ensure the MIDI source is actively sending clock messages. At least two clock messages are needed before synchronisation is achieved.
- **MIDI port not found**: List available MIDI ports using your system's MIDI configuration tools or `python-rtmidi` utilities, then specify the correct port number.

## License and Attribution

This utility integrates with third-party libraries licensed under their respective terms. See the referenced repositories for licensing information.
