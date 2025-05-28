# cSpell:ignore cpufreq

# Turbo Boost Control

A simple GTK application to control Intel Turbo Boost technology on Linux systems.

## Features

- Simple and intuitive user interface
- Real-time Turbo Boost status monitoring
- Easy toggle between ON/OFF states
- System tray integration
- Automatic status updates

## Requirements

- Python 3.x
- GTK 3
- Intel CPU with Turbo Boost support
- Root privileges (for MSR access)

## Installation

1. Install required packages:
```bash
sudo dnf install python3-gobject python3-psutil msr-tools
```

2. Clone the repository:
```bash
git clone https://github.com/muhammedby/turboost.git
cd turbo-boost-control
```

3. Run the application:
```bash
python3 turbo_boost_control.py
```

## Usage

1. Launch the application
2. Use the slider to toggle Turbo Boost:
   - Slide left to disable Turbo Boost
   - Slide right to enable Turbo Boost
3. The status label shows the current state

## Building from Source

### Flatpak Build

1. Install Flatpak and GNOME SDK:
```bash
sudo dnf install flatpak
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo
flatpak install flathub org.gnome.Sdk//45
```

2. Build the application:
```bash
flatpak-builder build org.turboboost.control.json
```

3. Run the application:
```bash
flatpak-builder --run build org.turboboost.control.json turboboost-control
```

### AppImage Build

1. Install required tools:
```bash
sudo dnf install appimage-builder
```

2. Build the AppImage:
```bash
appimage-builder
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.

## Acknowledgments

- Intel for Turbo Boost technology
- GTK team for the amazing toolkit
- Linux community for the excellent tools and documentation 

<!-- cSpell:ignore gobject psutil flathub appimage --> 
