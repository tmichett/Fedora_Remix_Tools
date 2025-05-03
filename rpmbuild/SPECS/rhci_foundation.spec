%define name fedora_remix_tools
%define version 1.0
%define release 0
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
mkdir -p $RPM_BUILD_ROOT/home/liveuser/Desktop/
mkdir -p $RPM_BUILD_ROOT/usr/share/gnome/autostart

# Copy application files to the buildroot
cp -p %{_sourcedir}/config.yml $RPM_BUILD_ROOT/opt/FedoraRemixTools/
cp -p %{_sourcedir}/menu.py $RPM_BUILD_ROOT/opt/FedoraRemixTools/
cp -p %{_sourcedir}/logo.png $RPM_BUILD_ROOT/opt/FedoraRemixTools/
cp -p %{_sourcedir}/smallicon.png $RPM_BUILD_ROOT/opt/FedoraRemixTools/
cp -p  %{_sourcedir}/start_fedora_remix_tools.sh $RPM_BUILD_ROOT/opt/FedoraRemixTools/


# Copy desktop file
cp -p %{_sourcedir}/Fedora_Remix_Tools.desktop $RPM_BUILD_ROOT/usr/share/applications/
cp -p %{_sourcedir}/Fedora_Remix_Tools.desktop $RPM_BUILD_ROOT/home/liveuser/Desktop/
cp -p %{_sourcedir}/Fedora_Remix_Tools.desktop $RPM_BUILD_ROOT/usr/share/gnome/autostart

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
/opt/FedoraRemixTools/
/opt/FedoraRemixTools/config.yml
/opt/FedoraRemixTools/menu.py
/opt/FedoraRemixTools/logo.png
/opt/FedoraRemixTools/smallicon.png
%attr(0755,root,root) /opt/FedoraRemixTools/start_rhci_tools.sh
%attr(0755,root,root) /usr/share/applications/Fedora_Remix_Tools.desktop
%attr(0755,root,root) /usr/share/gnome/autostart/Fedora_Remix_Tools.desktop
%attr(0755,liveuser,liveuser)/home/liveuser/Desktop/Fedora_Remix_Tools.desktop

%changelog
* Sat May 3 2025 Fedora Remix Tools Build <tmichett@redhat.com> - 1.0-0
- Initial package build
