#!/bin/bash
#
# Build script for Howdy GUI Manager RPM package
#

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✓${NC} $1"; }
print_info() { echo -e "${BLUE}ℹ${NC} $1"; }
print_error() { echo -e "${RED}✗${NC} $1"; }

echo "======================================"
echo "Building Howdy GUI Manager RPM package"
echo "======================================"
echo ""

# Variables
PACKAGE_NAME="howdy-gui-manager"
VERSION="1.0.0"
RELEASE="1"

# Check if we're in the right directory
if [ ! -d "howdy-gui-manager" ]; then
    print_error "howdy-gui-manager directory not found!"
    echo "Please run this script from the howdy-gui project root."
    exit 1
fi

# Check for rpmbuild
if ! command -v rpmbuild &> /dev/null; then
    print_error "rpmbuild not found!"
    echo "Please install: sudo dnf install rpm-build rpmdevtools"
    exit 1
fi

# Setup RPM build environment
print_info "Setting up RPM build environment..."
mkdir -p ~/rpmbuild/{BUILD,RPMS,SOURCES,SPECS,SRPMS}

# First, build the debian package structure (we'll use it as source)
print_info "Preparing source files..."
if [ ! -d "debian-package/usr" ]; then
    print_info "Building debian package structure first..."
    ./build-deb.sh > /dev/null 2>&1 || true
fi

# Copy spec file
print_info "Copying spec file..."
cp rpm-package/howdy-gui-manager.spec ~/rpmbuild/SPECS/

# Copy source files to rpmbuild SOURCES
print_info "Copying source files..."
mkdir -p ~/rpmbuild/SOURCES/usr/{bin,share}
cp -r debian-package/usr/* ~/rpmbuild/SOURCES/usr/

# Build RPM
print_info "Building RPM package..."
rpmbuild -bb ~/rpmbuild/SPECS/howdy-gui-manager.spec

# Copy built package to current directory
print_info "Copying built package..."
cp ~/rpmbuild/RPMS/noarch/${PACKAGE_NAME}-${VERSION}-${RELEASE}.*.rpm .

# Get the actual filename
RPM_FILE=$(ls ${PACKAGE_NAME}-${VERSION}-${RELEASE}.*.rpm 2>/dev/null | head -n 1)

if [ -z "$RPM_FILE" ]; then
    print_error "RPM package not found!"
    exit 1
fi

echo ""
echo "======================================"
print_success "Package built successfully!"
echo "======================================"
echo ""
echo "Package info:"
rpm -qip "$RPM_FILE"
echo ""
echo "Package contents:"
rpm -qlp "$RPM_FILE"
echo ""
echo "======================================"
echo "To install the package, run:"
echo "  sudo dnf install $RPM_FILE"
echo "  # OR"
echo "  sudo rpm -ivh $RPM_FILE"
echo "======================================"
