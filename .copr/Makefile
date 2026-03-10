.PHONY: prepare rustprep goprep gccprep prebuiltprep themesprep prebuild srpm

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

prebuild:
	@buildtype="unknown"; \
	if grep -q "Name:.*asr-rs\|Name:.*shpool\|Name:.*microsandbox\|Name:.*wl-gammarelay-rs" "$(SPECFILE)"; then \
		buildtype="rust"; \
	elif grep -q "Name:.*cliphist\|Name:.*nwg-look\|Name:.*xcur2png" "$(SPECFILE)"; then \
		buildtype="go"; \
	elif grep -q "Name:.*lisgd" "$(SPECFILE)"; then \
		buildtype="gcc"; \
	elif grep -q "Name:.*bibata-cursor-themes" "$(SPECFILE)"; then \
		buildtype="theme"; \
	elif grep -q "Name:.*mactahoe-oled\|Name:.*atuin\|Name:.*eza\|Name:.*starship\|Name:.*pi" "$(SPECFILE)"; then \
		buildtype="prebuilt"; \
	fi; \
	case $$buildtype in \
		"rust") $(MAKE) -f $(lastword $(MAKEFILE_LIST)) rustprep;; \
		"go") $(MAKE) -f $(lastword $(MAKEFILE_LIST)) goprep;; \
		"gcc") $(MAKE) -f $(lastword $(MAKEFILE_LIST)) gccprep;; \
		"theme") $(MAKE) -f $(lastword $(MAKEFILE_LIST)) themesprep;; \
		"prebuilt") $(MAKE) -f $(lastword $(MAKEFILE_LIST)) prebuiltprep;; \
		*) echo "Unknown package type in $(SPECFILE)"; exit 1;; \
	esac

srpm: prepare prebuild
	cd $(dir $(SPECFILE)) && spectool -g $(notdir $(SPECFILE))
	rpmbuild -bs \
		--define "_sourcedir $(dir $(SPECFILE))" \
		--define "_specdir $(dir $(SPECFILE))" \
		--define "_builddir $(BUILDDIR)" \
		--define "_srcrpmdir $(outdir)" \
		--define "_rpmdir $(BUILDDIR)" \
		--define "_buildrootdir $(BUILDDIR)/.build" \
		$(SPECFILE)
