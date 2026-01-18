# ROSE - Workspace Manager

A Python-based voice-controlled workspace manager that enables hands-free application and workspace management through voice commands and hotkey integration.

## Features

- **Voice Control**: Control workspaces and applications using voice commands
- **Hotkey Integration**: Customizable hotkeys for quick workspace switching
- **Session Management**: Manage and persist workspace sessions
- **Application Control**: Programmatic control of applications
- **Cross-platform Support**: Works across different platforms with keyboard automation

## Project Structure

```
├── main.py                 # Main entry point for the application
├── app_controller.py       # Application control and management
├── voice_engine.py         # Voice recognition and processing engine
├── session_manager.py      # Workspace session management
├── hotkeys.py              # Hotkey configuration and handling
├── requirements.txt        # Python dependencies
└── sessions/               # Stored session data
```

## Installation

### Requirements
- Python 3.8+
- pip (Python package manager)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/Roshmita-viswa/ROSE---workspace-manager.git
cd ROSE---workspace-manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the application:
```bash
python main.py
```

## Configuration

- **Hotkeys**: Configure custom hotkeys in `hotkeys.py`
- **Sessions**: Workspace sessions are automatically saved in the `sessions/` directory
- **Voice Engine**: Adjust voice recognition settings in `voice_engine.py`

## Dependencies

See `requirements.txt` for a complete list of required packages.

## Contributing

Contributions are welcome! Feel free to submit issues or pull requests.

## License

This project is part of the PlutoAI workspace management suite.

## Author

Roshmita Viswa

## Support

For issues or questions, please open an issue on the GitHub repository.
