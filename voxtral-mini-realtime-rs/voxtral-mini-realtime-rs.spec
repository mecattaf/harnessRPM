%global commit0 ffad466b6729acbe1a1d2e1b815f0275693b6f5d
%global shortcommit0 %(c=%{commit0}; echo ${c:0:7})
%global date0 20260211

Name:           voxtral-mini-realtime-rs
Version:        0.2.0
Release:        1.%{date0}git%{shortcommit0}%{?dist}
Summary:        Streaming speech-to-text using Voxtral Mini 4B with Burn ML framework

License:        Apache-2.0
URL:            https://github.com/TrevorS/voxtral-mini-realtime-rs
Source0:        %{url}/archive/%{commit0}.tar.gz#/%{name}-%{version}.tar.gz
# Vendor tarball created during SRPM build (COPR chroots lack network)
Source1:        %{name}-%{version}-vendor.tar.gz

BuildRequires:  rust-packaging
BuildRequires:  cargo
BuildRequires:  gcc
BuildRequires:  gcc-c++
BuildRequires:  pkg-config

# GPU runtime via wgpu/Vulkan
Requires:       vulkan-loader
Recommends:     mesa-vulkan-drivers

# Model download from HuggingFace Hub
Recommends:     python3-huggingface-hub

%description
Pure Rust implementation of Mistral's Voxtral Mini 4B Realtime automatic speech
recognition model using the Burn ML framework. Supports full-precision (f32)
SafeTensors and quantized (Q4 GGUF) inference via Vulkan GPU backend.

The voxtral-transcribe CLI transcribes WAV audio files using either f32 or Q4
models, with automatic chunking for long audio and HuggingFace Hub integration
for model downloads.

%prep
%autosetup -n %{name}-%{commit0}
tar xf %{SOURCE1}
mkdir -p .cargo
cp cargo-config.toml .cargo/config.toml

%build
cargo build --release --offline --features cli,hub --bin voxtral-transcribe

%install
install -Dpm 0755 target/release/voxtral-transcribe %{buildroot}%{_bindir}/voxtral-transcribe

%files
%license LICENSE
%doc README.md
%{_bindir}/voxtral-transcribe

%changelog
* Thu Mar 13 2026 Mecattaf <thomas@mecattaf.dev> - 0.2.0-1.20260211gitffad466
- Initial package (git snapshot, no upstream releases yet)
