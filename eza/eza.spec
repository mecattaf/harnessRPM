%global debug_package %{nil}

Name:           eza
Version:        0.23.4
Release:        %autorelease
Summary:        A modern alternative to ls

License:        EUPL-1.2
URL:            https://github.com/eza-community/eza
Source0:        %{url}/releases/download/v%{version}/%{name}_x86_64-unknown-linux-gnu.tar.gz
Source1:        %{url}/releases/download/v%{version}/completions-%{version}.tar.gz
Source2:        %{url}/releases/download/v%{version}/man-%{version}.tar.gz
Source3:        https://raw.githubusercontent.com/eza-community/eza/v%{version}/LICENSE.txt

# This is a prebuilt binary package, only available for x86_64
ExclusiveArch:  x86_64
BuildRequires:  gzip

%description
eza is a modern, maintained replacement for the ls command.

- It uses colors to distinguish file types and metadata.
- It recognizes symlinks, extended attributes, and Git status.
- It's written in Rust, so it's small, fast, and portable.

%prep
%setup -q -c
# Extract additional tarballs manually to specific directories
mkdir -p completions
mkdir -p man
tar -xf %{SOURCE1} -C completions
tar -xf %{SOURCE2} -C man
cp %{SOURCE3} .

%build
# Find and compress man pages properly
find man -name "*.1" -exec gzip -9 {} \;
find man -name "*.5" -exec gzip -9 {} \;

%install
# Install binary
install -Dpm755 %{name} %{buildroot}%{_bindir}/%{name}

# Install shell completions
# Use find to locate the files regardless of directory structure
install -dm755 %{buildroot}%{_datadir}/bash-completion/completions/
install -dm755 %{buildroot}%{_datadir}/fish/vendor_completions.d/
install -dm755 %{buildroot}%{_datadir}/zsh/site-functions/

# Find completions files by type and install them
find completions -name "*.bash" -o -name "%{name}" | grep -v "\.fish$" | grep -v "_%{name}" | head -1 | xargs -r install -Dpm644 -t %{buildroot}%{_datadir}/bash-completion/completions/
mv -f %{buildroot}%{_datadir}/bash-completion/completions/*.bash %{buildroot}%{_datadir}/bash-completion/completions/%{name} 2>/dev/null || true
find completions -name "*.fish" -o -name "%{name}.fish" | head -1 | xargs -r install -Dpm644 -t %{buildroot}%{_datadir}/fish/vendor_completions.d/
find completions -name "_%{name}" -o -name "_*.zsh" | head -1 | xargs -r install -Dpm644 -t %{buildroot}%{_datadir}/zsh/site-functions/
# Rename if needed
if [ ! -f %{buildroot}%{_datadir}/zsh/site-functions/_%{name} ]; then
  find %{buildroot}%{_datadir}/zsh/site-functions/ -name "_*" | head -1 | xargs -r -I{} mv {} %{buildroot}%{_datadir}/zsh/site-functions/_%{name} 2>/dev/null || true
fi

# Install man pages - using find to locate them regardless of directory structure
for manpage in $(find man -name "%{name}.1.gz" -o -name "*.1.gz" | grep -v "colors" | head -1); do
    install -Dpm644 "$manpage" %{buildroot}%{_mandir}/man1/%{name}.1.gz
done

for manpage in $(find man -name "%{name}_colors.5.gz" -o -name "*_colors.5.gz" | head -1); do
    install -Dpm644 "$manpage" %{buildroot}%{_mandir}/man5/%{name}_colors.5.gz
done

for manpage in $(find man -name "%{name}_colors-explanation.5.gz" -o -name "*_colors-explanation.5.gz" | head -1); do
    install -Dpm644 "$manpage" %{buildroot}%{_mandir}/man5/%{name}_colors-explanation.5.gz
done

# Create ls symlink
ln -sf %{name} %{buildroot}%{_bindir}/exa

%files
%license LICENSE.txt
%{_bindir}/%{name}
%{_bindir}/exa
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}
%{_mandir}/man1/%{name}.1.gz
%{_mandir}/man5/%{name}_colors.5.gz
%{_mandir}/man5/%{name}_colors-explanation.5.gz

%changelog
* Thu May 08 2025 Package Maintainer <maintainer@example.com> - 0.21.3-1
- Update to version 0.21.3
%autochangelog
