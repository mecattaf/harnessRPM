#!/bin/bash
# This script checks for new versions of cliphist and updates the spec file accordingly
# It works with the bundle_go_deps_for_rpm.sh script for handling Go dependencies

set -euo pipefail

# Define key variables for version checking
SPEC="cliphist.spec"
REPO="sentriz/cliphist"
VERSION_FIELD="Version:"

# Get the latest version from GitHub
# Note: cliphist uses 'v' prefix in its tags, so we remove it
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Only update if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
    # Update the spec file version
    sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}                ${LATEST}/" "$SPEC"
    
    # Since this is a Go package, we need to handle dependencies
    # The bundle_go_deps_for_rpm.sh script will be called during the build process
    
    # Commit and push the changes
    git add "$SPEC"
    git commit -m "Update cliphist to $LATEST [build-go]"
    git push
fi
