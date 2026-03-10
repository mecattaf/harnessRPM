#!/bin/bash
# Script to check for updates to starship and update the spec file accordingly

set -euo pipefail

SPEC="starship.spec"
REPO="starship/starship"
VERSION_FIELD="Version:"

# Get the latest version from GitHub
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Check if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
    # Verify that the source is available before updating
    SOURCE_URL="https://github.com/${REPO}/releases/download/v${LATEST}/${REPO##*/}-x86_64-unknown-linux-gnu.tar.gz"
    CONFIG_URL="https://raw.githubusercontent.com/starship/starship/v${LATEST}/docs/config/README.md"
    
    # Check if source files exist
    if curl --output /dev/null --silent --head --fail "$SOURCE_URL" && \
       curl --output /dev/null --silent --head --fail "$CONFIG_URL"; then
        
        # Update the spec file version
        sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}        ${LATEST}/" "$SPEC"
        
        # Commit and push the changes with the build tag
        git add "$SPEC"
        git commit -m "Update starship to $LATEST [build-prebuilt]"
        git push
        
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Source files for version ${LATEST} not available yet"
        exit 0
    fi
else
    echo "starship spec file is already at the latest version: $CURRENT"
fi
