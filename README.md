# Howdy GUI Manager

A comprehensive GUI application for managing Howdy face authentication on Linux systems.

## Features

### 🎯 Multi-Distribution Support
- **Debian/Ubuntu** family (Ubuntu, Pop!_OS, Linux Mint, Elementary, Zorin)
- **Fedora/RHEL** family (Fedora, RHEL, CentOS, Rocky, AlmaLinux)
- **Arch** family (Arch, Manjaro, EndeavourOS, Garuda)
- Automatic version detection and compatibility checking
- Ubuntu 24.04+ restriction enforcement

### 📸 Face Model Management
- **List** all registered face models
- **Add** new models with custom labels
- **Remove** individual models
- **Clear** all models at once
- Real-time status updates

### ⚙️ Configuration Interface
- Camera device selection (auto-detection)
- Certainty threshold adjustment
- Timeout configuration
- Dark threshold control
- Input validation and helpful tooltips

### 🧪 Face Recognition Testing
- Visual test interface
- Color-coded results (✅/❌)
- Detailed feedback messages
- Error handling and diagnostics

## Installation

### Prerequisites
- Python 3.6+
- PyQt6
- distro package

### Install Dependencies
```bash
pip install PyQt6 distro
```

### Install Howdy
The application will guide you through Howdy installation if it's not already installed.

## Usage

### Launch Application
```bash
python main.py
```

### First-Time Setup
1. If Howdy is not installed, the app will offer to install it
2. Navigate to the **Face Models** tab
3. Click **Add Model** to register your face
4. Enter a label (e.g., "default", "glasses", "no-glasses")
5. Follow the on-screen instructions
6. Test recognition in the **Test** tab

### Managing Face Models
- **Add Model**: Register a new face with a custom label
- **Remove Selected**: Delete a specific model
- **Clear All**: Remove all registered models
- **Refresh**: Update the model list

### Configuring Howdy
1. Go to **Configuration** tab
2. Select your IR camera device
3. Adjust settings:
   - **Certainty**: Lower = stricter (3.5 recommended)
   - **Timeout**: How long to wait for detection
   - **Dark Threshold**: Minimum brightness level
4. Click **Save Configuration** (requires sudo)

### Testing Face Recognition
1. Go to **Test** tab
2. Click **Test Face Recognition**
3. Look at the camera
4. View results with detailed feedback

## Project Structure

```
howdy-gui/
├── main.py                 # Application entry point
├── core/
│   ├── checks.py          # Distribution detection
│   ├── installer.py       # Howdy installation logic
│   ├── howdy.py           # Face model operations
│   └── config.py          # Configuration management
├── ui/
│   ├── main_window.py     # Main tabbed interface
│   ├── models_tab.py      # Face models management
│   ├── config_tab.py      # Configuration interface
│   ├── test_tab.py        # Testing interface
│   └── setup_dialog.py    # Installation wizard
└── scripts/
    └── install_howdy.sh   # Installation script
```

## Requirements

- **Operating System**: Linux (Debian, Ubuntu, Fedora, Arch variants)
- **Python**: 3.6 or higher
- **PyQt6**: For GUI
- **distro**: For distribution detection
- **Howdy**: Face authentication system (installed via app)

## Supported Distributions

### Debian Family
- Ubuntu (up to 22.04)
- Debian
- Pop!_OS
- Linux Mint
- Elementary OS
- Zorin OS

### Fedora Family
- Fedora
- RHEL
- CentOS
- Rocky Linux
- AlmaLinux

### Arch Family
- Arch Linux (via AUR)
- Manjaro
- EndeavourOS
- Garuda Linux

## Known Limitations

- Ubuntu 24.04 and later are not supported due to PAM changes
- Configuration changes require sudo privileges
- IR camera required for face authentication
- Some distributions may require manual Howdy installation

## Troubleshooting

### Application won't launch
- Ensure PyQt6 is installed: `pip install PyQt6`
- Check Python version: `python --version` (3.6+ required)

### Howdy installation fails
- Check your distribution is supported
- Ensure you have sudo privileges
- For Arch-based systems, install manually via AUR

### Face recognition not working
- Verify IR camera is connected
- Check camera device in Configuration tab
- Ensure at least one face model is added
- Adjust certainty threshold if needed

### Configuration changes not saving
- Ensure you have sudo privileges
- Check Howdy config file exists: `/lib/security/howdy/config.ini`

## License

This project is provided as-is for managing Howdy face authentication.

## Credits

- Built with PyQt6
- Uses Howdy for face authentication
- Distribution detection via distro package
