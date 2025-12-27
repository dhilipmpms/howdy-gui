Name:           howdy-gui-manager
Version:        1.0.0
Release:        1%{?dist}
Summary:        GUI Manager for Howdy Facial Authentication

License:        MIT
URL:            https://github.com/boltgolt/howdy
BuildArch:      noarch

Requires:       python3 >= 3.6
Requires:       python3-qt5
Requires:       python3-opencv
Requires:       howdy

%description
A graphical user interface for managing Howdy facial authentication system.
Features include:
 - Camera device selection and testing
 - Live camera preview
 - Face model management (add, remove, list)
 - Configuration editor for all Howdy settings
 - Real-time face recognition testing

This application provides an easy-to-use interface for configuring
and managing Howdy without using the command line.

%prep
# No prep needed - files are already in place

%build
# No build needed - Python scripts

%install
# Create directories
mkdir -p %{buildroot}/usr/bin
mkdir -p %{buildroot}/usr/share/howdy-gui
mkdir -p %{buildroot}/usr/share/applications
mkdir -p %{buildroot}/usr/share/icons/hicolor/256x256/apps

# Copy executable
install -m 755 %{_sourcedir}/usr/bin/howdy-gui-manager %{buildroot}/usr/bin/howdy-gui-manager

# Copy Python modules
cp -r %{_sourcedir}/usr/share/howdy-gui/* %{buildroot}/usr/share/howdy-gui/

# Copy desktop file
install -m 644 %{_sourcedir}/usr/share/applications/howdy-gui-manager.desktop \
    %{buildroot}/usr/share/applications/howdy-gui-manager.desktop

# Copy icon
install -m 644 %{_sourcedir}/usr/share/icons/hicolor/256x256/apps/howdy-gui-manager.png \
    %{buildroot}/usr/share/icons/hicolor/256x256/apps/howdy-gui-manager.png

%files
/usr/bin/howdy-gui-manager
/usr/share/howdy-gui/
/usr/share/applications/howdy-gui-manager.desktop
/usr/share/icons/hicolor/256x256/apps/howdy-gui-manager.png

%post
# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database -q /usr/share/applications || :
fi

# Update icon cache
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor || :
fi

%postun
# Update desktop database
if [ -x /usr/bin/update-desktop-database ]; then
    /usr/bin/update-desktop-database -q /usr/share/applications || :
fi

# Update icon cache
if [ -x /usr/bin/gtk-update-icon-cache ]; then
    /usr/bin/gtk-update-icon-cache -q -t -f /usr/share/icons/hicolor || :
fi

%changelog
* Fri Dec 27 2024 Howdy GUI Team <howdy@example.com> - 1.0.0-1
- Initial RPM release
- Multi-distribution support
- Modern UI with gradient header and improved styling
