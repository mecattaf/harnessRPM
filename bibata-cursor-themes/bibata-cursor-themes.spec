%global         source_name Bibata_Cursor
%global         debug_package %{nil}

Name:           bibata-cursor-themes
Version:        2.0.7
Release:        1%{?dist}
Summary:        OpenSource, Compact and Material Designed Cursor Set

License:        GPL-3.0-only
URL:            https://github.com/ful1e5/Bibata_Cursor
Source0:        %{url}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{url}/releases/download/v%{version}/bitmaps.zip

BuildArch:      noarch

BuildRequires:  python3
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
BuildRequires:  unzip

Requires:       gtk3

%description
Bibata is an open-source cursor theme collection with a material design aesthetic.
It comes in multiple variants including Modern and Original styles, each available
in Amber, Classic (Black), and Ice (White) colors, with both left and right-handed
versions.

%prep
%autosetup -c
%autosetup -T -D -a 1

mv bitmaps %{source_name}-%{version}

%build
# Ensure pip installs packages in the local directory
export PIP_TARGET="${PWD}/.local"
export PATH="${PIP_TARGET}/bin:$PATH"
export PYTHONPATH="${PIP_TARGET}:${PYTHONPATH:-}"

# Install required build dependencies
pip install --no-cache-dir clickgen

cd %{source_name}-%{version}

# Build normal variants
declare -A normal_names=(
    ["Bibata-Modern-Amber"]="Yellowish and rounded edge Bibata cursors"
    ["Bibata-Modern-Classic"]="Black and rounded edge Bibata cursors"
    ["Bibata-Modern-Ice"]="White and rounded edge Bibata cursors"
    ["Bibata-Original-Amber"]="Yellowish and sharp edge Bibata cursors"
    ["Bibata-Original-Classic"]="Black and sharp edge Bibata cursors"
    ["Bibata-Original-Ice"]="White and sharp edge Bibata cursors"
)

for key in "${!normal_names[@]}"; do
    ctgen configs/normal/x.build.toml -p x11 -d "bitmaps/$key" -n "$key" -c "${normal_names[$key]}"
done

# Build right-handed variants
declare -A right_names=(
    ["Bibata-Modern-Amber-Right"]="Yellowish and rounded edge right-hand Bibata cursors"
    ["Bibata-Modern-Classic-Right"]="Black and rounded edge right-hand Bibata cursors"
    ["Bibata-Modern-Ice-Right"]="White and rounded edge right-hand Bibata cursors"
    ["Bibata-Original-Amber-Right"]="Yellowish and sharp edge right-hand Bibata cursors"
    ["Bibata-Original-Classic-Right"]="Black and sharp edge right-hand Bibata cursors"
    ["Bibata-Original-Ice-Right"]="White and sharp edge right-hand Bibata cursors"
)

for key in "${!right_names[@]}"; do
    ctgen configs/right/x.build.toml -p x11 -d "bitmaps/$key" -n "$key" -c "${right_names[$key]}"
done

%install
%__rm -rf %{buildroot}
%__mkdir -p %{buildroot}%{_datadir}/icons

# Install all theme variants
cd %{source_name}-%{version}
for theme in themes/*; do
    %__cp -r "$theme" %{buildroot}%{_datadir}/icons/
    %__chmod 0755 %{buildroot}%{_datadir}/icons/"$(basename "$theme")"
done

%files
%license %{source_name}-%{version}/LICENSE
%doc %{source_name}-%{version}/README.md
%{_datadir}/icons/Bibata-*

%changelog
* Wed Dec 04 2024 Your Name <your.email@domain.com> - 2.0.7-1
- Update to version 2.0.7
- Add automated build support
- Improve spec file structure and documentation

* Tue Jun 18 2024 Original Packager <packager@email.com> - 1.0.0-1
- Initial package version
