# quickshell (stable release) - Reference Only

This spec is kept for reference. The stable `quickshell` package (v0.2.1) is **no longer built on COPR** (`mecattaf/harnessRPM`). Only the git-tracking variants are actively built:

- **quickshell-git** — tracks upstream `quickshell-mirror/quickshell` master
- **quickshellX-git** — tracks `mecattaf/quickshellX` fork with additional functionality

## Why it was removed

The v0.2.1 tagged release still referenced `breakpad` as a dependency in its build system, but upstream has since fully replaced breakpad with `cpptrace`. The git-tracking specs already pick up this change automatically. Rather than maintain a stable spec that drifts from upstream's current build requirements, we only ship the git variants.

## Original spec (quickshell.spec)

```spec
%bcond_with         asan

%global commit      a1a150fab00a93ea983aaca5df55304bc837f51b

Name:               quickshell
Version:            0.2.1
Release:            1%{?dist}
Summary:            Flexible QtQuick based desktop shell toolkit

License:            LGPL-3.0-only AND GPL-3.0-only
URL:                https://github.com/quickshell-mirror/quickshell
Source0:            %{url}/archive/v%{version}/%{name}-%{version}.tar.gz

Conflicts:          quickshell-git
Conflicts:          quickshellX-git

BuildRequires:      cmake
BuildRequires:      cmake(Qt6Core)
BuildRequires:      cmake(Qt6Qml)
BuildRequires:      cmake(Qt6ShaderTools)
BuildRequires:      cmake(Qt6WaylandClient)
BuildRequires:      cpptrace-devel
BuildRequires:      gcc-c++
BuildRequires:      ninja-build
BuildRequires:      pkgconfig(CLI11)
BuildRequires:      pkgconfig(gbm)
BuildRequires:      pkgconfig(jemalloc)
BuildRequires:      pkgconfig(libdrm)
BuildRequires:      pkgconfig(libpipewire-0.3)
BuildRequires:      pkgconfig(pam)
BuildRequires:      pkgconfig(wayland-client)
BuildRequires:      pkgconfig(wayland-protocols)
BuildRequires:      qt6-qtbase-private-devel
BuildRequires:      spirv-tools

%if %{with asan}
BuildRequires:      libasan
%endif

Provides:           desktop-notification-daemon

%description
Flexible toolkit for making desktop shells with QtQuick, targeting
Wayland and X11.

%prep
%autosetup -p1

%build
%cmake  -GNinja \
%if %{with asan}
        -DASAN=ON \
%endif
        -DBUILD_SHARED_LIBS=OFF \
        -DCMAKE_BUILD_TYPE=Release \
        -DDISTRIBUTOR="Fedora COPR (mecattaf/harnessRPM)" \
        -DGIT_REVISION=%{commit} \
        -DINSTALL_QML_PREFIX=%{_lib}/qt6/qml
%cmake_build

%install
%cmake_install

%files
%license LICENSE
%license LICENSE-GPL
%doc BUILD.md
%doc CONTRIBUTING.md
%doc README.md
%doc changelog/v%{version}.md
%{_bindir}/qs
%{_bindir}/quickshell
%{_datadir}/applications/org.quickshell.desktop
%{_datadir}/icons/hicolor/scalable/apps/org.quickshell.svg
%{_libdir}/qt6/qml/Quickshell

%changelog
%autochangelog
```
