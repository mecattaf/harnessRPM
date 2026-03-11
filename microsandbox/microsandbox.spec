Name:           microsandbox
Version:        0.2.6
Release:        1%{?dist}
Summary:        Lightweight microVM sandbox manager using libkrun

License:        Apache-2.0
URL:            https://github.com/zerocore-ai/microsandbox
Source0:        %{url}/archive/%{name}-v%{version}/%{name}-%{version}.tar.gz
# Vendor tarball created during SRPM build (COPR chroots lack network)
Source1:        %{name}-%{version}-vendor.tar.gz

BuildRequires:  rust-packaging
BuildRequires:  cargo
BuildRequires:  git-core
BuildRequires:  systemd-rpm-macros
BuildRequires:  libkrun-devel
BuildRequires:  openssl-devel
BuildRequires:  pkg-config

Requires:       libkrun

%description
microsandbox is a lightweight microVM sandbox manager built on libkrun.
It provides isolated execution environments using KVM-based micro virtual
machines. Includes the msb CLI, msbrun launcher, and msbserver orchestrator.

NOTE: Requires /dev/kvm access. On SELinux-enforcing systems you may need
to allow KVM device access for your user. See README.SELinux for details.

%prep
%autosetup -n %{name}-%{name}-v%{version}
tar xf %{SOURCE1}
mkdir -p .cargo
cp cargo-config.toml .cargo/config.toml

%build
cargo build --release --offline --bin msb --bin msbrun --bin msbserver

%install
install -Dpm 0755 target/release/msb %{buildroot}%{_bindir}/msb
install -Dpm 0755 target/release/msbrun %{buildroot}%{_libexecdir}/%{name}/msbrun
install -Dpm 0755 target/release/msbserver %{buildroot}%{_libexecdir}/%{name}/msbserver

# Install systemd user service
install -d %{buildroot}%{_userunitdir}
cat > %{buildroot}%{_userunitdir}/%{name}.service << 'EOF'
[Unit]
Description=microsandbox server
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=%{_libexecdir}/%{name}/msbserver
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

# Install SELinux README
cat > README.SELinux << 'EOFSEL'
microsandbox SELinux Notes
==========================

microsandbox requires access to /dev/kvm for microVM execution.
On Fedora Atomic with SELinux enforcing, you may need to:

  1. Allow KVM access for your user:
     sudo setsebool -P virt_use_kvm 1

  2. If that is insufficient, create a custom policy module:
     sudo ausearch -m avc -ts recent | audit2allow -M microsandbox
     sudo semodule -i microsandbox.pp

  3. Verify access:
     ls -lZ /dev/kvm
EOFSEL

%files
%license LICENSE
%doc README.md
%doc README.SELinux
%{_bindir}/msb
%dir %{_libexecdir}/%{name}
%{_libexecdir}/%{name}/msbrun
%{_libexecdir}/%{name}/msbserver
%{_userunitdir}/%{name}.service

%post
%systemd_user_post %{name}.service

%preun
%systemd_user_preun %{name}.service

%postun
%systemd_user_postun_with_restart %{name}.service

%changelog
* Tue Mar 10 2026 Mecattaf <thomas@mecattaf.dev> - 0.2.6-1
- Initial package
