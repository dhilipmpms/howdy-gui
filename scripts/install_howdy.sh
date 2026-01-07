#!/bin/bash
set -e

DISTRO="$1"
VERSION="$2"
FAMILY="$3"
UBUNTU_24_PLUS="$4"

echo "Installing Howdy on $DISTRO $VERSION ($FAMILY family)..."

# Handle Debian/Ubuntu-based distributions
if [[ "$FAMILY" == "debian" ]]; then
    
    # Check if Ubuntu 24.04 or later
    if [[ "$UBUNTU_24_PLUS" == "true" ]]; then
        echo "Ubuntu 24.04+ detected - using unofficial PPA..."
        echo "Adding unofficial Howdy PPA (ppa:ubuntuhandbook1/howdy)..."
        sudo add-apt-repository -y ppa:ubuntuhandbook1/howdy
        
        echo "Updating package list..."
        sudo apt update
        
        echo "Installing Howdy..."
        sudo apt install -y howdy
        
        echo "Installing additional dependencies for Ubuntu 24.04+..."
        sudo apt install -y python3-numpy python3-opencv python3-dlib libpam-python dlib-models libinireader0
        
        echo "Howdy installation complete for Ubuntu 24.04+!"
    else
        echo "Adding official Howdy PPA (ppa:boltgolt/howdy)..."
        sudo add-apt-repository -y ppa:boltgolt/howdy
        
        echo "Updating package list..."
        sudo apt update
        
        echo "Installing Howdy..."
        sudo apt install -y howdy
        
        echo "Howdy installation complete!"
    fi

# Handle Fedora/RHEL-based distributions
elif [[ "$FAMILY" == "fedora" ]]; then
    echo "Installing Howdy via DNF..."
    
    # Check if Howdy is available in repos
    if sudo dnf info howdy &>/dev/null; then
        sudo dnf install -y howdy
        echo "Howdy installation complete!"
    else
        echo "ERROR: Howdy package not found in repositories."
        echo "You may need to add the appropriate repository for your distribution."
        exit 1
    fi

# Handle Arch-based distributions (should not reach here, but just in case)
elif [[ "$FAMILY" == "arch" ]]; then
    echo "ERROR: Please install Howdy from AUR:"
    echo "  yay -S howdy"
    echo "or"
    echo "  paru -S howdy"
    exit 1

else
    echo "ERROR: Unsupported distribution family: $FAMILY"
    exit 1
fi
