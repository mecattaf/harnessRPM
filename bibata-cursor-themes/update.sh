#!/bin/bash
set -euo pipefail

SPEC="bibata-cursor-themes.spec"
REPO="ful1e5/Bibata_Cursor"

# Get latest version from GitHub releases
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$LATEST" != "$CURRENT" ]; then
    # Verify that both source files are available before updating
    MAIN_SOURCE="https://github.com/${REPO}/archive/v${LATEST}/${LATEST}.tar.gz"
    BITMAPS_SOURCE="https://github.com/${REPO}/releases/download/v${LATEST}/bitmaps.zip"
    
    # Check if both source files exist
    if curl --output /dev/null --silent --head --fail "$MAIN_SOURCE" && \
       curl --output /dev/null --silent --head --fail "$BITMAPS_SOURCE"; then
        
        # Update version in spec file
        sed -i "s/Version:.*/Version:        ${LATEST}/" "$SPEC"
        
        # Update changelog
        TODAY=$(date "+%a %b %d %Y")
        sed -i "/%changelog/a* ${TODAY} GitHub Action <github-actions@github.com> - ${LATEST}-1\n- Update to version ${LATEST}\n" "$SPEC"
        
        # Commit and push changes
        git add "$SPEC"
        git commit -m "Update bibata-cursor-themes to ${LATEST} [build-themes]"
        git push
    else
        echo "Warning: Source files for version ${LATEST} not available yet"
        exit 0
    fi
fi
