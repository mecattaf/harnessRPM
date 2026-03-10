%global forgeurl https://git.sr.ht/~mil/lisgd
Version:        0.4.0
%forgemeta

Name:           lisgd
Release:        %autorelease
Summary:        Libinput synthetic gesture daemon for touchscreens

License:        MIT
URL:            %{forgeurl}
Source0:        %{forgeurl}/archive/%{version}.tar.gz
Source1:        90-lisgd.rules

BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  libinput-devel
BuildRequires:  systemd-devel
BuildRequires:  libX11-devel
BuildRequires:  wayland-devel
BuildRequires:  checkpolicy
BuildRequires:  selinux-policy-devel
BuildRequires:  udev

Requires:       libinput
Requires:       libwayland-client
Requires:       libX11

%description
Lisgd (libinput synthetic gesture daemon) lets you bind gestures based on
libinput touch events to run specific commands to execute. For example, dragging
left to right with one finger could execute a particular command like launching
a terminal. Directional L-R, R-L, U-D, and D-U gestures and diagonal LD-RU,
RD-LU, UR-DL, UL-DR gestures are supported with 1 through n fingers.

%package selinux
Summary:        SELinux policy module for lisgd
Requires:       %{name} = %{version}-%{release}
Requires:       selinux-policy
Requires:       policycoreutils
Requires(post): policycoreutils

%description selinux
This package provides the SELinux policy module to ensure lisgd
can access input devices and execute commands properly.

%prep
%autosetup
# Create SELinux policy file
cat > lisgd.te << 'EOF'
module lisgd 1.0;

require {
    type user_t;
    type input_device_t;
    type xserver_t;
    class chr_file { open read write ioctl };
    class process { execmem };
}

#============= user_t ==============
allow user_t input_device_t:chr_file { open read write ioctl };
allow user_t self:process execmem;
EOF

%build
%make_build
# Build SELinux policy
checkmodule -M -m -o lisgd.mod lisgd.te
semodule_package -o lisgd.pp -m lisgd.mod

# Create a README.Fedora file
cat > README.Fedora << 'EOF'
lisgd - libinput synthetic gesture daemon
========================================

Using lisgd with your touchscreen
---------------------------------

To find your touchscreen devices, use this command:
```
swaymsg -t get_inputs | grep -A 20 touch
```

Once you identify your touchscreen device names, you need to find their input device paths.
You can do this with evtest:
```
sudo evtest
```
Select your touchscreen from the list and note the device path (like /dev/input/event5).

In your Sway config, add lisgd commands like:
```
exec lisgd -d /dev/input/eventX \
  -g "1,LR,*,*,R,swaymsg workspace next" \
  -g "1,RL,*,*,R,swaymsg workspace prev" 
```

Permissions
----------
lisgd requires access to input devices. The package installs udev rules that 
grant access to members of the 'seat' group, which users are automatically
part of in Fedora Workstation environments.

For Fedora Atomic or other immutable environments, these udev rules should
work without any system modifications.

Troubleshooting
--------------
If lisgd isn't working:
1. Verify you can access the touchscreen device: `ls -l /dev/input/eventX`
   (It should show permissions that include your group)
2. Check SELinux denials: `sudo ausearch -m avc -ts recent | grep denied`
3. Run lisgd with the -v flag for verbose output
4. On Fedora Atomic: Make sure the udev rules were applied with `sudo udevadm control --reload-rules`
   and `sudo udevadm trigger`
5. As a last resort, you can run lisgd with sudo for testing: `sudo lisgd -d /dev/input/eventX -v`
EOF

%install
install -m 755 -D lisgd "%{buildroot}%{_bindir}/lisgd"
install -m 644 -D lisgd.1 "%{buildroot}%{_mandir}/man1/lisgd.1"
install -m 644 -D lisgd.pp "%{buildroot}%{_datadir}/selinux/packages/%{name}.pp"
install -m 644 -D %{SOURCE1} "%{buildroot}%{_udevrulesdir}/90-lisgd.rules"
install -m 644 -D README.Fedora "%{buildroot}%{_docdir}/%{name}/README.Fedora"

%post selinux
%selinux_modules_install %{_datadir}/selinux/packages/%{name}.pp

%postun selinux
if [ $1 -eq 0 ]; then
    %selinux_modules_uninstall %{name}
fi

%files
%{_bindir}/lisgd
%{_mandir}/man1/lisgd.1.*
%{_udevrulesdir}/90-lisgd.rules
%license LICENSE
%doc README.md
%doc %{_docdir}/%{name}/README.Fedora

%files selinux
%{_datadir}/selinux/packages/%{name}.pp

%changelog
%autochangelog
