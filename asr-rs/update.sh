#!/bin/bash
set -euo pipefail

SPEC="asr-rs.spec"
REPO="mecattaf/asr-rs"

LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$LATEST" != "$CURRENT" ]; then
    SOURCE_URL="https://github.com/${REPO}/archive/v${LATEST}/${REPO##*/}-${LATEST}.tar.gz"
    if curl --output /dev/null --silent --head --fail "$SOURCE_URL"; then
        sed -i "s/Version:.*/Version:        ${LATEST}/" "$SPEC"
        git add "$SPEC"
        git commit -m "Update asr-rs to $LATEST [build-rust]"
        git push
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Source files for version ${LATEST} not available yet"
        exit 0
    fi
else
    echo "asr-rs spec file is already at the latest version: $CURRENT"
fi
