# harnessRPM

COPR spec repository for the [harness](https://github.com/mecattaf) custom Fedora Atomic image.

```
sudo dnf copr enable mecattaf/harnessRPM
```

## Packages

| Package | Description | Type |
|---------|-------------|------|
| asr-rs | Streaming speech-to-text daemon for Wayland | Rust, build from source |
| mactahoe-oled | MacTahoe GTK theme (OLED black) + icon set | noarch, prebuilt tarball |
| shpool | Terminal session multiplexer | Rust, build from source |
| microsandbox | Lightweight microVM sandbox manager (libkrun) | Rust, build from source |
| pi | Terminal-based coding agent | Prebuilt binary |
| atuin | Magical shell history | Prebuilt binary |
| bibata-cursor-themes | Material design cursor theme set | noarch, build from source |
| cliphist | Wayland clipboard manager | Go, build from source |
| eza | Modern ls replacement | Prebuilt binary |
| lisgd | Libinput gesture daemon for touchscreens | C, build from source |
| nwg-look | GTK3 settings editor for wlroots | Go, build from source |
| starship | Cross-shell prompt | Prebuilt binary |
| wl-gammarelay-rs | Wayland display temperature/brightness control | Rust, build from source |
| xcur2png | X cursor to PNG converter (nwg-look dep) | C, build from source |

## Targets

- Fedora 43+ (x86_64, aarch64)
- Fedora rawhide
- Follow-fedora-branching enabled
