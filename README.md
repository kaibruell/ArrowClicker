# Arrow Clicker

A Python-based keyboard-to-mouse control application that allows you to control your mouse cursor and perform clicks using keyboard inputs. The application features dual-mode operation: mouse control mode and normal input mode.

## Features

- **Dual Mode Operation**: Switch between mouse control mode and normal keyboard input mode
- **WASD Mouse Movement**: Use WASD keys for intuitive mouse cursor movement
- **Acceleration System**: Mouse movement accelerates with continuous key presses
- **Precision Mode**: Hold Shift for slower, more precise mouse movements
- **Mouse Clicks**: Perform left and right mouse clicks using keyboard keys
- **Smooth Movement**: Multi-threaded design for fluid mouse cursor movement
- **Safety Features**: Easy toggle between modes and emergency exit

## Controls

### Global Controls
- **Pause**: Switch between MOUSE mode and INPUT mode
- **ESC**: Exit the program

### Mouse Mode Controls
- **W/A/S/D**: Move mouse cursor (up/left/down/right)
- **Shift**: Hold for precision mode (slower movement)
- **Comma (,)**: Left mouse click
- **Period (.)**: Right mouse click

### Input Mode
- All keyboard keys function normally

## Installation

1. Create a virtual environment:
```bash
python -m venv env
```

2. Activate the virtual environment:
```bash
source env/bin/activate
```

3. Install required dependencies:
```bash
pip install keyboard pyautogui
```

## Usage

Run the application with elevated privileges (required for keyboard hooks):

```bash
sudo $(which python) arrow-clicker.py
```

**Note**: Root privileges are required for the keyboard library to capture global key events.

## Configuration

The following parameters can be modified at the top of the script:

- `STEP_SIZE`: Initial movement speed (default: 10 pixels)
- `ACCEL_FACTOR`: Acceleration multiplier (default: 1.05)
- `MAX_SPEED`: Maximum movement speed (default: 30 pixels)
- `MIN_SPEED`: Precision mode speed (default: 1 pixel)
- `DEFAULT_DELAY`: Update rate in seconds (default: 0.005)

## Key Mappings

You can customize the key mappings by modifying these variables:

- `MOVE_UP`: Default 'w'
- `MOVE_DOWN`: Default 's'
- `MOVE_LEFT`: Default 'a' 
- `MOVE_RIGHT`: Default 'd'
- `PRECISION`: Default 'shift'
- `LEFT_CLICK`: Default ','
- `RIGHT_CLICK`: Default '.'
- `TOGGLE_MODE`: Default 'pause'
- `EXIT_KEY`: Default 'esc'

## Safety Notes

- The application disables PyAutoGUI's fail-safe feature for better functionality
- Use ESC key to safely exit the program at any time
- The Pause key allows quick switching between mouse control and normal input
- Mouse buttons are automatically released when switching modes

## Requirements

- Python 3.x
- `keyboard` library
- `pyautogui` library
- Linux/Unix system (for elevated privileges)

## Troubleshooting

- If keyboard input isn't captured, ensure the script is run with `sudo`
- If mouse movement feels too fast/slow, adjust `STEP_SIZE` and `MAX_SPEED` values
- For precision work, use Shift key to enable slow movement mode

## License

This project is provided as-is for educational and personal use purposes.
