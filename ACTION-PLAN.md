# Adding a New Package to harnessRPM

## 1. Create the package directory

```
mkdir <package-name>
```

Add at minimum:
- `<package-name>.spec` — RPM spec file
- `update.sh` — script to track upstream releases and auto-update the spec

For Go packages that need vendoring, also add `bundle_go_deps_for_rpm.sh`.

## 2. Update the build system

### `.copr/Makefile`

- If the package needs a new build type, add a `<type>prep` target with the right `dnf install` deps.
- Add the package name to the `prebuild` detection (`grep -q "Name:.*<package-name>"`).
- If the package needs dependency vendoring (Rust cargo vendor, Go mod vendor), add a vendoring block in the `srpm` target after `spectool -g`.

### `.github/workflows/build.yml`

- Add the `[build-<type>]` tag to the job-level `if` condition (if using a new tag).
- Add a build step that calls `copr-cli build-package`.

Existing build tags: `[build-rust]`, `[build-go]`, `[build-gcc]`, `[build-themes]`, `[build-prebuilt]`, `[build-kitty]`, `[build-all]`.

## 3. Create the package on COPR

Run through the authenticated toolbox:

```
distrobox enter toolbox -- copr-cli add-package-scm mecattaf/harnessRPM \
  --name <package-name> \
  --clone-url https://github.com/mecattaf/harnessRPM \
  --subdir <package-name> \
  --spec <package-name>.spec \
  --method make_srpm \
  --type git
```

## 4. Commit and push

```
git add <package-name>/ .copr/Makefile .github/workflows/build.yml
git commit -m "Add <package-name> <version> [build-<type>]"
git push
```

The `[build-<type>]` tag in the commit message triggers the GitHub Actions workflow, which calls `copr-cli build-package` to kick off the COPR build.

## Updating an existing package

Either run the package's `update.sh` (from its directory), or manually bump `Version:` in the spec and push with the right `[build-<type>]` tag.
