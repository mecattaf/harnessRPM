%global debug_package %{nil}

Name:           mactahoe-oled
Version:        1.0.0
Release:        1%{?dist}
Summary:        MacTahoe GTK theme (OLED black, grey accent) and icon set
BuildArch:      noarch

License:        GPL-3.0
URL:            https://github.com/mecattaf/harnessRPM
Source0:        %{url}/releases/download/v%{version}/%{name}-%{version}.tar.gz

%description
MacTahoe GTK theme with OLED black surfaces (grey accent) and MacTahoe grey
icon set for Wayland/niri environments. Includes standard, solid, HiDPI and
extra-HiDPI theme variants plus grey, grey-dark and grey-light icon sets.

Activate with:
  gsettings set org.gnome.desktop.interface gtk-theme 'MacTahoe-Dark-grey'
  gsettings set org.gnome.desktop.interface icon-theme 'MacTahoe-grey-dark'

%prep
%setup -q

%install
# Install GTK themes
install -d %{buildroot}%{_datadir}/themes
cp -r themes/* %{buildroot}%{_datadir}/themes/

# Install icons
install -d %{buildroot}%{_datadir}/icons
cp -r icons/* %{buildroot}%{_datadir}/icons/

# Fix permissions (directories 755, files 644)
find %{buildroot}%{_datadir}/themes -type d -exec chmod 755 {} \;
find %{buildroot}%{_datadir}/themes -type f -exec chmod 644 {} \;
find %{buildroot}%{_datadir}/icons -type d -exec chmod 755 {} \;
find %{buildroot}%{_datadir}/icons -type f -exec chmod 644 {} \;

%files
%{_datadir}/themes/MacTahoe-Dark-grey/
%{_datadir}/themes/MacTahoe-Dark-grey-hdpi/
%{_datadir}/themes/MacTahoe-Dark-grey-xhdpi/
%{_datadir}/themes/MacTahoe-Dark-solid-grey/
%{_datadir}/themes/MacTahoe-Dark-solid-grey-hdpi/
%{_datadir}/themes/MacTahoe-Dark-solid-grey-xhdpi/
%{_datadir}/icons/MacTahoe-grey/
%{_datadir}/icons/MacTahoe-grey-dark/
%{_datadir}/icons/MacTahoe-grey-light/

%changelog
* Tue Mar 10 2026 Mecattaf <thomas@mecattaf.dev> - 1.0.0-1
- Initial package with OLED black GTK themes and grey icon set
