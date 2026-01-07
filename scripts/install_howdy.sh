#!/bin/bash
set -e

DISTRO="$1"
VERSION="$2"
FAMILY="$3"

echo "Installing Howdy on $DISTRO $VERSION ($FAMILY family)..."

# Handle Debian/Ubuntu-based distributions
if [[ "$FAMILY" == "debian" ]]; then
    echo "Adding Howdy PPA..."
    sudo add-apt-repository -y ppa:boltgolt/howdy
    
    echo "Updating package list..."
    sudo apt update
    
    echo "Installing Howdy..."
    sudo apt install -y howdy
    
    echo "Howdy installation complete!"

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
