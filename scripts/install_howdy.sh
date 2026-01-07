#!/bin/bash
set -e

DISTRO="$1"

echo "Detected distro: $DISTRO"

if [[ "$DISTRO" == "ubuntu" || "$DISTRO" == "debian" ]]; then
    echo "Installing Howdy via official PPA..."

    sudo apt update
    sudo apt install -y software-properties-common

    # Official Howdy PPA
    sudo add-apt-repository -y ppa:boltgolt/howdy
    sudo apt update
    sudo apt install -y howdy

elif [[ "$DISTRO" == "fedora" ]]; then
    echo "Installing Howdy on Fedora..."

    sudo dnf install -y howdy

elif [[ "$DISTRO" == "arch" ]]; then
    echo "Arch Linux detected."
    echo "Please install Howdy from AUR:"
    echo "  yay -S howdy"
    exit 1

else
    echo "Unsupported distro. Install Howdy manually."
    exit 1
fi

echo "Howdy installation completed."
