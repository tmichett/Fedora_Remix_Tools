%define name fedora_remix_tools
%define version 1.0
%define release 8
%define buildroot %{_tmppath}/%{name}-%{version}-%{release}-root

Summary: Fedora Remix Tools Application
Name: %{name}
Version: %{version}
Release: %{release}
License: Proprietary
Group: Applications/System
BuildArch: noarch
BuildRoot: %{buildroot}
Requires: python3

%description
Fedora Remix Tools Application

%prep
# No preparation needed for this simple package

%build
# No build process needed

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/opt/FedoraRemixTools
mkdir -p $RPM_BUILD_ROOT/usr/share/applications
mkdir -p $RPM_BUILD_ROOT/usr/share/gnome/autostart

# Copy application files to the buildroot
cp -p %{_sourcedir}/config.yml $RPM_BUILD_ROOT/opt/FedoraRemixTools/
cp -p %{_sourcedir}/menu.py $RPM_BUILD_ROOT/opt/FedoraRemixTools/
cp -p %{_sourcedir}/logo.png $RPM_BUILD_ROOT/opt/FedoraRemixTools/
cp -p %{_sourcedir}/smallicon.png $RPM_BUILD_ROOT/opt/FedoraRemixTools/
cp -p %{_sourcedir}/fedora_remix_tools.sh $RPM_BUILD_ROOT/opt/FedoraRemixTools/
cp -p %{_sourcedir}/trust-desktop-icons.sh $RPM_BUILD_ROOT/opt/FedoraRemixTools/

# Copy desktop file to system locations only
# Desktop shortcut for liveuser is created in %post to avoid user/group dependency
cp -p %{_sourcedir}/Fedora_Remix_Tools.desktop $RPM_BUILD_ROOT/usr/share/applications/

# Autostart entry to trust desktop icons on first login (runs in user session)
cp -p %{_sourcedir}/fedora-remix-tools-trust.desktop $RPM_BUILD_ROOT/usr/share/gnome/autostart/

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Create desktop shortcut for liveuser if the user exists
# This avoids the user/group dependency issue in the RPM
DESKTOP_FILE="/home/liveuser/Desktop/Fedora_Remix_Tools.desktop"

if id liveuser &>/dev/null; then
    # Create Desktop directory if it doesn't exist
    mkdir -p /home/liveuser/Desktop
    
    # Copy desktop file to user's desktop
    cp /usr/share/applications/Fedora_Remix_Tools.desktop "$DESKTOP_FILE"
    
    # Set the executable bit
    chmod +x "$DESKTOP_FILE"
    
    # Ensure ownership is correct
    chown liveuser:liveuser "$DESKTOP_FILE"
    
    # Method 1: Use dbus-launch to create a session and set trusted metadata
    if command -v dbus-launch &>/dev/null && command -v gio &>/dev/null; then
        su - liveuser -c "dbus-launch gio set '$DESKTOP_FILE' metadata::trusted true" 2>/dev/null || true
    fi
    
    # Method 2: Use gio with dbus-run-session as fallback
    if command -v dbus-run-session &>/dev/null && command -v gio &>/dev/null; then
        su - liveuser -c "dbus-run-session gio set '$DESKTOP_FILE' metadata::trusted true" 2>/dev/null || true
    fi
fi

%files
%defattr(-,root,root,-)
/opt/FedoraRemixTools/
/opt/FedoraRemixTools/config.yml
/opt/FedoraRemixTools/menu.py
/opt/FedoraRemixTools/logo.png
/opt/FedoraRemixTools/smallicon.png
%attr(0755,root,root) /opt/FedoraRemixTools/fedora_remix_tools.sh
%attr(0755,root,root) /opt/FedoraRemixTools/trust-desktop-icons.sh
%attr(0755,root,root) /usr/share/applications/Fedora_Remix_Tools.desktop
%attr(0644,root,root) /usr/share/gnome/autostart/fedora-remix-tools-trust.desktop
# Desktop shortcut is created dynamically in %post to avoid liveuser dependency

%changelog
* Thu Jan 1 2026 Fedora Remix Tools Build <tmichett@redhat.com> - 1.0-8
- Fix RPM dependency on liveuser by creating desktop shortcut in %post  
- Use dbus-launch/dbus-run-session to set trusted metadata from CLI
- Fix desktop shortcut to be trusted/launchable without manual "Allow Launching"

* Sat May 3 2025 Fedora Remix Tools Build <tmichett@redhat.com> - 1.0-0
- Initial package build
