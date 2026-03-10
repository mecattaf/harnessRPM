#!/bin/bash
# Script to check for updates to eza and update the spec file accordingly

set -euo pipefail

SPEC="eza.spec"
REPO="eza-community/eza"
VERSION_FIELD="Version:"

# Get the latest version from GitHub
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Check if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
    # Verify that all required source files are available before updating
    BINARY_URL="https://github.com/${REPO}/releases/download/v${LATEST}/${REPO##*/}_x86_64-unknown-linux-gnu.tar.gz"
    COMPLETIONS_URL="https://github.com/${REPO}/releases/download/v${LATEST}/completions-${LATEST}.tar.gz"
    MAN_URL="https://github.com/${REPO}/releases/download/v${LATEST}/man-${LATEST}.tar.gz"
    
    # Check if all source files exist
    if curl --output /dev/null --silent --head --fail "$BINARY_URL" && \
       curl --output /dev/null --silent --head --fail "$COMPLETIONS_URL" && \
       curl --output /dev/null --silent --head --fail "$MAN_URL"; then
        
        # Update the spec file version
        sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}        ${LATEST}/" "$SPEC"
        
        # Commit and push the changes with the build tag
        git add "$SPEC"
        git commit -m "Update eza to $LATEST [build-prebuilt]"
        git push
        
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Source files for version ${LATEST} not available yet"
        exit 0
    fi
else
    echo "eza spec file is already at the latest version: $CURRENT"
fi
