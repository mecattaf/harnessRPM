.PHONY: prepare rustprep goprep gccprep prebuiltprep themesprep kittyprep prebuild srpm

# Define variables
BUILDDIR := $(shell pwd)
SPECFILE := $(spec)

prepare:
	dnf install --nodocs -y rpm-build rpmdevtools

rustprep: prepare
	dnf install --nodocs -y rust cargo git-core pkg-config alsa-lib-devel

goprep: prepare
	dnf install --nodocs -y \
		--repofrompath 'golang-rawhide,https://download.copr.fedorainfracloud.org/results/@go-sig/golang-rawhide/fedora-$$releasever-$$basearch/' \
		--setopt='golang-rawhide.gpgkey=https://download.copr.fedorainfracloud.org/results/@go-sig/golang-rawhide/pubkey.gpg' \
		golang git-core
	go env -w GOPROXY=https://proxy.golang.org,direct
	go env -w GOSUMDB=sum.golang.org
	test -f bundle_go_deps_for_rpm.sh && bash bundle_go_deps_for_rpm.sh $(SPECFILE) || true

gccprep: prepare
	dnf install --nodocs -y gcc gcc-c++ make cmake ninja-build

prebuiltprep: prepare
	dnf install --nodocs -y tar gzip xz

themesprep: prepare
	dnf install --nodocs -y python3-devel python3-pip python3-wheel

kittyprep: prepare
	dnf install --nodocs -y \
		--repofrompath 'golang-rawhide,https://download.copr.fedorainfracloud.org/results/@go-sig/golang-rawhide/fedora-$$releasever-$$basearch/' \
		--setopt='golang-rawhide.gpgkey=https://download.copr.fedorainfracloud.org/results/@go-sig/golang-rawhide/pubkey.gpg' \
		golang git-core
	go env -w GOPROXY=https://proxy.golang.org,direct
	go env -w GOSUMDB=sum.golang.org

prebuild:
	@buildtype="unknown"; \
	if grep -q "Name:.*asr-rs\|Name:.*shpool\|Name:.*microsandbox\|Name:.*wl-gammarelay-rs\|Name:.*gws\|Name:.*fgp-browser\|Name:.*voxtral-mini-realtime-rs" "$(SPECFILE)"; then \
		buildtype="rust"; \
	elif grep -q "Name:.*cliphist\|Name:.*nwg-look\|Name:.*xcur2png" "$(SPECFILE)"; then \
		buildtype="go"; \
	elif grep -q "Name:.*cpptrace\|Name:.*lisgd\|Name:.*quickshell-git\|Name:.*quickshellX-git" "$(SPECFILE)"; then \
		buildtype="gcc"; \
	elif grep -q "Name:.*bibata-cursor-themes" "$(SPECFILE)"; then \
		buildtype="theme"; \
	elif grep -q "Name:.*kitty" "$(SPECFILE)"; then \
		buildtype="kitty"; \
	elif grep -q "Name:.*mactahoe-oled\|Name:.*atuin\|Name:.*eza\|Name:.*starship\|Name:.*pi" "$(SPECFILE)"; then \
		buildtype="prebuilt"; \
	fi; \
	case $$buildtype in \
		"rust") $(MAKE) -f $(lastword $(MAKEFILE_LIST)) rustprep;; \
		"go") $(MAKE) -f $(lastword $(MAKEFILE_LIST)) goprep;; \
		"gcc") $(MAKE) -f $(lastword $(MAKEFILE_LIST)) gccprep;; \
		"theme") $(MAKE) -f $(lastword $(MAKEFILE_LIST)) themesprep;; \
		"kitty") $(MAKE) -f $(lastword $(MAKEFILE_LIST)) kittyprep;; \
		"prebuilt") $(MAKE) -f $(lastword $(MAKEFILE_LIST)) prebuiltprep;; \
		*) echo "Unknown package type in $(SPECFILE)"; exit 1;; \
	esac

srpm: prepare prebuild
	cd $(dir $(SPECFILE)) && spectool -g $(notdir $(SPECFILE))
	@# For Rust packages, vendor dependencies (COPR chroots lack network during rpmbuild)
	@if grep -q "Name:.*asr-rs\|Name:.*shpool\|Name:.*microsandbox\|Name:.*wl-gammarelay-rs\|Name:.*gws\|Name:.*voxtral-mini-realtime-rs" "$(SPECFILE)"; then \
		specdir=$$(cd "$(dir $(SPECFILE))" && pwd); \
		pkg_name=$$(grep '^Name:' "$(SPECFILE)" | awk '{print $$2}'); \
		pkg_ver=$$(grep '^Version:' "$(SPECFILE)" | awk '{print $$2}'); \
		echo "==> Vendoring Rust dependencies for $${pkg_name}-$${pkg_ver}..."; \
		tmpdir=$$(mktemp -d); \
		tar xf "$${specdir}/$${pkg_name}-$${pkg_ver}.tar.gz" -C "$$tmpdir"; \
		srcdir=$$(find "$$tmpdir" -mindepth 1 -maxdepth 1 -type d | head -1); \
		cd "$$srcdir" && cargo vendor > cargo-config.toml && \
		tar czf "$${specdir}/$${pkg_name}-$${pkg_ver}-vendor.tar.gz" -C "$$srcdir" vendor cargo-config.toml; \
		rm -rf "$$tmpdir"; \
		echo "==> Created $${pkg_name}-$${pkg_ver}-vendor.tar.gz"; \
	fi
	@# For kitty, vendor Go dependencies (COPR chroots lack network during rpmbuild)
	@if grep -q "Name:.*kitty" "$(SPECFILE)"; then \
		specdir=$$(cd "$(dir $(SPECFILE))" && pwd); \
		pkg_ver=$$(grep '^Version:' "$(SPECFILE)" | awk '{print $$2}'); \
		echo "==> Vendoring Go dependencies for kitty-$${pkg_ver}..."; \
		tmpdir=$$(mktemp -d); \
		tar xf "$${specdir}/kitty-$${pkg_ver}.tar.xz" -C "$$tmpdir"; \
		srcdir=$$(find "$$tmpdir" -mindepth 1 -maxdepth 1 -type d | head -1); \
		cd "$$srcdir" && go mod vendor && \
		tar czf "$${specdir}/vendor-$${pkg_ver}.tar.gz" vendor; \
		rm -rf "$$tmpdir"; \
		echo "==> Created vendor-$${pkg_ver}.tar.gz"; \
	fi
	@# fgp-browser needs special handling: bundled fgp-daemon + Cargo.lock generation
	@if grep -q "Name:.*fgp-browser" "$(SPECFILE)"; then \
		specdir=$$(cd "$(dir $(SPECFILE))" && pwd); \
		pkg_ver=$$(grep '^Version:' "$(SPECFILE)" | awk '{print $$2}'); \
		echo "==> Vendoring Rust dependencies for fgp-browser-$${pkg_ver} (with bundled fgp-daemon)..."; \
		tmpdir=$$(mktemp -d); \
		tar xf "$${specdir}/fgp-browser-$${pkg_ver}.tar.gz" -C "$$tmpdir"; \
		tar xf "$${specdir}/fgp-daemon-a16b0df.tar.gz" -C "$$tmpdir"; \
		srcdir=$$(find "$$tmpdir" -maxdepth 1 -name "browser-*" -type d | head -1); \
		daemondir=$$(find "$$tmpdir" -maxdepth 1 -name "daemon-*" -type d | head -1); \
		sed -i "s|fgp-daemon = { git = \"https://github.com/fast-gateway-protocol/daemon\" }|fgp-daemon = { path = \"$$daemondir\" }|" "$$srcdir/Cargo.toml"; \
		cd "$$srcdir" && cargo generate-lockfile && \
		cargo vendor > cargo-config.toml && \
		tar czf "$${specdir}/fgp-browser-$${pkg_ver}-vendor.tar.gz" -C "$$srcdir" vendor cargo-config.toml Cargo.lock; \
		rm -rf "$$tmpdir"; \
		echo "==> Created fgp-browser-$${pkg_ver}-vendor.tar.gz"; \
	fi
	rpmbuild -bs \
		--define "_sourcedir $(dir $(SPECFILE))" \
		--define "_specdir $(dir $(SPECFILE))" \
		--define "_builddir $(BUILDDIR)" \
		--define "_srcrpmdir $(outdir)" \
		--define "_rpmdir $(BUILDDIR)" \
		--define "_buildrootdir $(BUILDDIR)/.build" \
		$(SPECFILE)
