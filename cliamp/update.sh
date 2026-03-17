#!/bin/bash
set -euo pipefail

SPEC="cliamp.spec"
REPO="bjarneo/cliamp"

LATEST=$(curl -s "https://api.github.com/repos/$REPO/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(rpmspec -q --qf "%{version}\n" "$SPEC" | head -1)

if [ "$LATEST" != "$CURRENT" ]; then
    AMD64_URL="https://github.com/${REPO}/releases/download/v${LATEST}/cliamp-linux-amd64"
    ARM64_URL="https://github.com/${REPO}/releases/download/v${LATEST}/cliamp-linux-arm64"

    if curl --output /dev/null --silent --head --fail "$AMD64_URL" && \
       curl --output /dev/null --silent --head --fail "$ARM64_URL"; then
        sed -i "s/Version:.*/Version:        ${LATEST}/" "$SPEC"
        git add "$SPEC"
        git commit -m "Update cliamp to $LATEST [build-prebuilt]"
        git push
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Source files for version ${LATEST} not available yet"
        exit 0
    fi
else
    echo "cliamp spec file is already at the latest version: $CURRENT"
fi
