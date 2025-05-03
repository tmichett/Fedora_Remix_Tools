%define name rhci_instructor_tools
%define version 1.0
%define release 5
%define buildroot %{_tmppath}/%{name}-%{version}-%{release}-root

Summary: RHCI Foundation Instructor Tools Application
Name: %{name}
Version: %{version}
Release: %{release}
License: Proprietary
Group: Applications/System
BuildArch: noarch
BuildRoot: %{buildroot}
Requires: python3

%description
RHCI Foundation Instructor Tools Application

%prep
# No preparation needed for this simple package

%build
# No build process needed

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/opt/rhci_foundation
mkdir -p $RPM_BUILD_ROOT/usr/share/applications
mkdir -p $RPM_BUILD_ROOT/home/kiosk/Desktop/
mkdir -p $RPM_BUILD_ROOT/usr/share/gnome/autostart

# Copy application files to the buildroot
cp -p %{_sourcedir}/config.yml $RPM_BUILD_ROOT/opt/rhci_foundation/
cp -p %{_sourcedir}/menu.py $RPM_BUILD_ROOT/opt/rhci_foundation/
cp -p %{_sourcedir}/logo.png $RPM_BUILD_ROOT/opt/rhci_foundation/
cp -p %{_sourcedir}/smallicon.png $RPM_BUILD_ROOT/opt/rhci_foundation/
cp -p  %{_sourcedir}/start_rhci_tools.sh $RPM_BUILD_ROOT/opt/rhci_foundation/


# Copy desktop file
cp -p %{_sourcedir}/RHCI_Tools.desktop $RPM_BUILD_ROOT/usr/share/applications/
cp -p %{_sourcedir}/RHCI_Tools.desktop $RPM_BUILD_ROOT/home/kiosk/Desktop/
cp -p %{_sourcedir}/RHCI_Tools.desktop $RPM_BUILD_ROOT/usr/share/gnome/autostart

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/opt/rhci_foundation/
/opt/rhci_foundation/config.yml
/opt/rhci_foundation/menu.py
/opt/rhci_foundation/logo.png
/opt/rhci_foundation/smallicon.png
%attr(0755,root,root) /opt/rhci_foundation/start_rhci_tools.sh
%attr(0755,root,root) /usr/share/applications/RHCI_Tools.desktop
%attr(0755,root,root) /usr/share/gnome/autostart/RHCI_Tools.desktop
%attr(0755,kiosk,kiosk)/home/kiosk/Desktop/RHCI_Tools.desktop

%changelog
* Thu Apr 24 2025 Package Builder <builder@example.com> - 1.0-1
- Initial package build
