%global debug_package %{nil}

Name:           atuin
Version:        18.6.0
Release:        %autorelease
Summary:        Magical shell history

License:        MIT
URL:            https://github.com/atuinsh/atuin
Source0:        %{url}/releases/download/%{version}/%{name}-x86_64-unknown-linux-gnu.tar.gz
Source1:        https://raw.githubusercontent.com/atuinsh/atuin/%{version}/README.md
Source2:        https://raw.githubusercontent.com/atuinsh/atuin/%{version}/LICENSE

# This is a prebuilt binary package, only available for x86_64
ExclusiveArch:  x86_64
Requires:       glibc

%global         _missing_build_ids_terminate_build 0

%description
Atuin replaces your existing shell history with a SQLite database, and records additional context for your commands.
Additionally, it provides optional and fully encrypted synchronization of your history between machines, via an Atuin server.

%prep
%setup -q -c
cp %{SOURCE1} ./README.md
cp %{SOURCE2} ./LICENSE

# Debug: list files to examine tarball structure
ls -la
if [ -d %{name}-x86_64-unknown-linux-gnu ]; then
    ls -la %{name}-x86_64-unknown-linux-gnu
fi
if [ -d bin ]; then
    ls -la bin
fi

%build
# Binary release, nothing to build

%install
# Find and install the binary, handling different possible locations
if [ -f ./%{name} ]; then
    # Binary at root level
    install -Dpm755 ./%{name} %{buildroot}%{_bindir}/%{name}
elif [ -f ./bin/%{name} ]; then
    # Binary in bin directory
    install -Dpm755 ./bin/%{name} %{buildroot}%{_bindir}/%{name}
elif [ -f ./%{name}-x86_64-unknown-linux-gnu/%{name} ]; then
    # Binary in architecture-specific directory
    install -Dpm755 ./%{name}-x86_64-unknown-linux-gnu/%{name} %{buildroot}%{_bindir}/%{name}
elif [ -f ./%{name}-x86_64-unknown-linux-gnu/bin/%{name} ]; then
    # Binary in nested bin directory
    install -Dpm755 ./%{name}-x86_64-unknown-linux-gnu/bin/%{name} %{buildroot}%{_bindir}/%{name}
else
    # If we can't find the binary, search for it
    BINARY_PATH=$(find . -name "%{name}" -type f -executable | head -1)
    if [ -n "$BINARY_PATH" ]; then
        install -Dpm755 "$BINARY_PATH" %{buildroot}%{_bindir}/%{name}
    else
        echo "Could not find %{name} binary in the tarball"
        exit 1
    fi
fi

# Install shell completions - check supported commands first
mkdir -p %{buildroot}%{_datadir}/bash-completion/completions
mkdir -p %{buildroot}%{_datadir}/fish/vendor_completions.d
mkdir -p %{buildroot}%{_datadir}/zsh/site-functions

# Check if completions command exists by looking at help output
if %{buildroot}%{_bindir}/%{name} --help | grep -q "completions"; then
    # Modern syntax with a 'completions' subcommand
    %{buildroot}%{_bindir}/%{name} completions bash > %{buildroot}%{_datadir}/bash-completion/completions/%{name} || :
    %{buildroot}%{_bindir}/%{name} completions fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish || :
    %{buildroot}%{_bindir}/%{name} completions zsh > %{buildroot}%{_datadir}/zsh/site-functions/_%{name} || :
elif %{buildroot}%{_bindir}/%{name} --help | grep -q "generate-completions"; then
    # Alternative syntax with 'generate-completions'
    %{buildroot}%{_bindir}/%{name} generate-completions bash > %{buildroot}%{_datadir}/bash-completion/completions/%{name} || :
    %{buildroot}%{_bindir}/%{name} generate-completions fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish || :
    %{buildroot}%{_bindir}/%{name} generate-completions zsh > %{buildroot}%{_datadir}/zsh/site-functions/_%{name} || :
elif %{buildroot}%{_bindir}/%{name} --help | grep -q "completion"; then
    # Single 'completion' command variant
    %{buildroot}%{_bindir}/%{name} completion bash > %{buildroot}%{_datadir}/bash-completion/completions/%{name} || :
    %{buildroot}%{_bindir}/%{name} completion fish > %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish || :
    %{buildroot}%{_bindir}/%{name} completion zsh > %{buildroot}%{_datadir}/zsh/site-functions/_%{name} || :
else
    # If no completion command is found, create empty files
    echo "# Atuin auto-completion is not available for this version" > %{buildroot}%{_datadir}/bash-completion/completions/%{name}
    echo "# Atuin auto-completion is not available for this version" > %{buildroot}%{_datadir}/fish/vendor_completions.d/%{name}.fish
    echo "# Atuin auto-completion is not available for this version" > %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
    echo "WARNING: No completion command found in atuin. Skipping shell completions."
fi

%files
%license LICENSE
%doc README.md
%{_bindir}/%{name}
%{_datadir}/bash-completion/completions/%{name}
%{_datadir}/fish/vendor_completions.d/%{name}.fish
%{_datadir}/zsh/site-functions/_%{name}

%changelog
* Thu May 08 2025 Package Maintainer <maintainer@example.com> - 18.6.0-1
- Update to version 18.6.0
%autochangelog
