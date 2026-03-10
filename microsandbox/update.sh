#!/bin/bash
set -euo pipefail

SPEC="microsandbox.spec"
REPO="zerocore-ai/microsandbox"

# microsandbox uses tags like "microsandbox-v0.2.6"
LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^microsandbox-v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$LATEST" != "$CURRENT" ]; then
    SOURCE_URL="https://github.com/${REPO}/archive/microsandbox-v${LATEST}/microsandbox-${LATEST}.tar.gz"
    if curl --output /dev/null --silent --head --fail "$SOURCE_URL"; then
        sed -i "s/Version:.*/Version:        ${LATEST}/" "$SPEC"
        git add "$SPEC"
        git commit -m "Update microsandbox to $LATEST [build-rust]"
        git push
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Source files for version ${LATEST} not available yet"
        exit 0
    fi
else
    echo "microsandbox spec file is already at the latest version: $CURRENT"
fi
