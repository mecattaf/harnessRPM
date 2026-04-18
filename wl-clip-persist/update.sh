#!/bin/bash
set -euo pipefail

SPEC="wl-clip-persist.spec"
REPO="Linus789/wl-clip-persist"

# Get latest version from GitHub API
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
# Get current version from spec file
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Check if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
    # Update version in spec file
    sed -i "s/Version:.*/Version:        ${LATEST}/" "$SPEC"

    # Commit and push changes
    git add "$SPEC"
    git commit -m "Update wl-clip-persist to $LATEST [build-rust]"
    git push
fi
