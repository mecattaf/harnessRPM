#!/bin/bash
set -euo pipefail

SPEC="pi.spec"
REPO="badlogic/pi-mono"

LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$LATEST" != "$CURRENT" ]; then
    X64_URL="https://github.com/${REPO}/releases/download/v${LATEST}/pi-linux-x64.tar.gz"
    ARM64_URL="https://github.com/${REPO}/releases/download/v${LATEST}/pi-linux-arm64.tar.gz"

    if curl --output /dev/null --silent --head --fail "$X64_URL" && \
       curl --output /dev/null --silent --head --fail "$ARM64_URL"; then
        sed -i "s/Version:.*/Version:        ${LATEST}/" "$SPEC"
        git add "$SPEC"
        git commit -m "Update pi to $LATEST [build-prebuilt]"
        git push
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Source files for version ${LATEST} not available yet"
        exit 0
    fi
else
    echo "pi spec file is already at the latest version: $CURRENT"
fi
