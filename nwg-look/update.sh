#!/bin/bash
# This script checks for new versions of nwg-look and updates the spec file accordingly

set -euo pipefail

# Define key variables for version checking
SPEC="nwg-look.spec"
REPO="nwg-piotr/nwg-look"
VERSION_FIELD="Version:"

# Get the latest version from GitHub
# Note: nwg-look uses 'v' prefix in its tags
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

# Only update if versions differ
if [ "$LATEST" != "$CURRENT" ]; then
    # Update the spec file version
    # Note the specific formatting used in the nwg-look spec file
    sed -i "s/^${VERSION_FIELD}.*/${VERSION_FIELD}        ${LATEST}/" "$SPEC"
    
    # Commit and push the changes
    git add "$SPEC"
    git commit -m "Update nwg-look to $LATEST [build-go]"
    git push
fi
