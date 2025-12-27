#!/bin/bash
#
# Howdy GUI Manager - Multi-Distribution Installer
# Supports: Debian/Ubuntu (apt), Fedora/RHEL (dnf), Arch/Manjaro (pacman)
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Print colored messages
print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_info() { echo -e "${BLUE}ℹ${NC} $1"; }
print_warning() { echo -e "${YELLOW}⚠${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }

echo "=============================================="
echo "  Howdy GUI Manager - Multi-Distro Installer"
echo "=============================================="
echo ""

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "This script must be run as root"
    echo "Please run: sudo $0"
    exit 1
fi

# Detect distribution
detect_distribution() {
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        DISTRO_ID=$ID
        DISTRO_NAME=$NAME
        DISTRO_VERSION=$VERSION_ID
    else
        print_error "Cannot detect OS version"
        exit 1
    fi
}

# Detect package manager
detect_package_manager() {
    if command -v apt-get &> /dev/null; then
        PKG_MANAGER="apt"
    elif command -v dnf &> /dev/null; then
        PKG_MANAGER="dnf"
    elif command -v yum &> /dev/null; then
        PKG_MANAGER="yum"
    elif command -v pacman &> /dev/null; then
        PKG_MANAGER="pacman"
    elif command -v zypper &> /dev/null; then
        PKG_MANAGER="zypper"
    else
        PKG_MANAGER="unknown"
    fi
}

# Show interactive menu
show_menu() {
    echo ""
    print_info "Detected Distribution: $DISTRO_NAME"
    print_info "Detected Package Manager: $PKG_MANAGER"
    echo ""
    echo "Which package manager would you like to use?"
    echo ""
    echo "  1) apt      (Debian/Ubuntu/Mint/Pop!_OS)"
    echo "  2) dnf/rpm  (Fedora/RHEL/CentOS)"
    echo "  3) pacman   (Arch/Manjaro/EndeavourOS)"
    echo "  4) Exit"
    echo ""
    
    while true; do
        read -p "Enter your choice [1-4]: " choice
        case $choice in
            1) SELECTED_PKG="apt"; break;;
            2) SELECTED_PKG="dnf"; break;;
            3) SELECTED_PKG="pacman"; break;;
            4) echo "Installation cancelled"; exit 0;;
            *) print_error "Invalid choice. Please enter 1-4.";;
        esac
    done
    
    echo ""
    print_info "Selected package manager: $SELECTED_PKG"
    echo ""
}

# Install Howdy - APT (Debian/Ubuntu)
install_howdy_apt() {
    print_info "Installing Howdy via APT..."
    
    if command -v howdy &> /dev/null; then
        print_success "Howdy is already installed"
        return 0
    fi
    
    # Add Howdy PPA
    if ! grep -q "boltgolt/howdy" /etc/apt/sources.list /etc/apt/sources.list.d/* 2>/dev/null; then
        print_info "Adding Howdy PPA repository..."
        add-apt-repository -y ppa:boltgolt/howdy
    fi
    
    # Update and install
    apt-get update -qq
    DEBIAN_FRONTEND=noninteractive apt-get install -y howdy
    
    print_success "Howdy installed successfully"
}

# Install Howdy - DNF (Fedora/RHEL)
install_howdy_dnf() {
    print_info "Installing Howdy via DNF..."
    
    if command -v howdy &> /dev/null; then
        print_success "Howdy is already installed"
        return 0
    fi
    
    # Enable COPR repository
    print_info "Enabling Howdy COPR repository..."
    dnf copr enable -y principis/howdy
    
    # Install Howdy
    dnf install -y howdy
    
    print_success "Howdy installed successfully"
}

# Install Howdy - Pacman (Arch)
install_howdy_pacman() {
    print_info "Installing Howdy via Pacman (AUR)..."
    
    if command -v howdy &> /dev/null; then
        print_success "Howdy is already installed"
        return 0
    fi
    
    # Check for AUR helper
    if command -v yay &> /dev/null; then
        print_info "Using yay to install from AUR..."
        sudo -u $SUDO_USER yay -S --noconfirm howdy
    elif command -v paru &> /dev/null; then
        print_info "Using paru to install from AUR..."
        sudo -u $SUDO_USER paru -S --noconfirm howdy
    else
        print_warning "No AUR helper found. Installing yay..."
        
        # Install dependencies for yay
        pacman -S --needed --noconfirm git base-devel
        
        # Install yay as the user (not root)
        cd /tmp
        sudo -u $SUDO_USER git clone https://aur.archlinux.org/yay.git
        cd yay
        sudo -u $SUDO_USER makepkg -si --noconfirm
        cd ..
        rm -rf yay
        
        # Now install howdy
        print_info "Installing Howdy with yay..."
        sudo -u $SUDO_USER yay -S --noconfirm howdy
    fi
    
    print_success "Howdy installed successfully"
}

# Install dependencies - APT
install_dependencies_apt() {
    print_info "Installing dependencies via APT..."
    
    apt-get update -qq
    DEBIAN_FRONTEND=noninteractive apt-get install -y \
        python3 \
        python3-pyqt5 \
        python3-opencv
    
    print_success "Dependencies installed"
}

# Install dependencies - DNF
install_dependencies_dnf() {
    print_info "Installing dependencies via DNF..."
    
    dnf install -y \
        python3 \
        python3-qt5 \
        python3-opencv
    
    print_success "Dependencies installed"
}

# Install dependencies - Pacman
install_dependencies_pacman() {
    print_info "Installing dependencies via Pacman..."
    
    pacman -S --needed --noconfirm \
        python \
        python-pyqt5 \
        python-opencv
    
    print_success "Dependencies installed"
}

# Install GUI Manager - Debian/Ubuntu (.deb)
install_gui_manager_deb() {
    print_info "Building and installing .deb package..."
    
    # Build the package if it doesn't exist
    if [ ! -f "howdy-gui-manager_1.0.0_all.deb" ]; then
        print_info "Building .deb package..."
        ./build-deb.sh
    fi
    
    # Install the package
    dpkg -i howdy-gui-manager_1.0.0_all.deb || apt-get install -f -y
    print_success "Howdy GUI Manager installed"
}

# Install GUI Manager - Fedora/RHEL (.rpm)
install_gui_manager_rpm() {
    print_info "Building and installing .rpm package..."
    
    # Check for build tools
    if ! command -v rpmbuild &> /dev/null; then
        print_info "Installing RPM build tools..."
        dnf install -y rpm-build rpmdevtools
    fi
    
    # Build the package
    print_info "Building .rpm package..."
    ./build-rpm.sh
    
    # Find and install the built package
    RPM_FILE=$(ls howdy-gui-manager-1.0.0-1.*.rpm 2>/dev/null | head -n 1)
    if [ -z "$RPM_FILE" ]; then
        print_error "RPM package not found after build"
        exit 1
    fi
    
    dnf install -y "$RPM_FILE"
    print_success "Howdy GUI Manager installed"
}

# Install GUI Manager - Arch/Manjaro (PKGBUILD)
install_gui_manager_arch() {
    print_info "Building and installing Arch package..."
    
    # Check for build tools
    if ! command -v makepkg &> /dev/null; then
        print_info "Installing build tools..."
        pacman -S --needed --noconfirm base-devel
    fi
    
    # Build the debian package structure first (needed as source)
    if [ ! -d "debian-package/usr" ]; then
        print_info "Preparing source files..."
        ./build-deb.sh > /dev/null 2>&1 || true
    fi
    
    # Build and install the package
    cd arch-package
    sudo -u $SUDO_USER makepkg -si --noconfirm
    cd ..
    
    print_success "Howdy GUI Manager installed"
}

# Main installation function
main_installation() {
    echo "This script will install:"
    echo "  1. Howdy (facial authentication)"
    echo "  2. Required dependencies (PyQt5, OpenCV)"
    echo "  3. Howdy GUI Manager"
    echo ""
    read -p "Continue with installation? (y/N) " -n 1 -r
    echo ""
    
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Installation cancelled"
        exit 0
    fi
    
    echo ""
    echo "Starting installation..."
    echo ""
    
    # Step 1: Install Howdy
    echo "Step 1/3: Installing Howdy..."
    echo "-------------------------------------------"
    case $SELECTED_PKG in
        apt)
            install_howdy_apt
            ;;
        dnf|yum)
            install_howdy_dnf
            ;;
        pacman)
            install_howdy_pacman
            ;;
        *)
            print_error "Unsupported package manager: $SELECTED_PKG"
            exit 1
            ;;
    esac
    echo ""
    
    # Step 2: Install dependencies
    echo "Step 2/3: Installing GUI Manager dependencies..."
    echo "-------------------------------------------"
    case $SELECTED_PKG in
        apt)
            install_dependencies_apt
            ;;
        dnf|yum)
            install_dependencies_dnf
            ;;
        pacman)
            install_dependencies_pacman
            ;;
    esac
    echo ""
    
    # Step 3: Install GUI Manager
    echo "Step 3/3: Installing Howdy GUI Manager..."
    echo "-------------------------------------------"
    case $SELECTED_PKG in
        apt)
            install_gui_manager_deb
            ;;
        dnf|yum)
            install_gui_manager_rpm
            ;;
        pacman)
            install_gui_manager_arch
            ;;
    esac
    echo ""
}

# Run the installer
detect_distribution
detect_package_manager
show_menu
main_installation

# Success message
echo "=============================================="
echo "  Installation Complete!"
echo "=============================================="
echo ""
print_success "You can now launch Howdy GUI Manager:"
echo "  • From terminal: sudo howdy-gui-manager"
echo "  • From application menu: Search for 'Howdy GUI Manager'"
echo ""
echo "Next steps:"
echo "  1. Launch the GUI Manager"
echo "  2. Go to Camera Settings and select your camera"
echo "  3. Go to Face Models and add your face"
echo "  4. Test recognition!"
echo ""
echo "For support, visit: https://github.com/boltgolt/howdy"
echo "=============================================="
