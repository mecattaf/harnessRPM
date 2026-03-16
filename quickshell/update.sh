#!/bin/bash
set -euo pipefail

# Update all three quickshell spec files

REPO_STABLE="quickshell-mirror/quickshell"
REPO_FORK="mecattaf/quickshellX"

# --- quickshell.spec (stable release) ---
SPEC="quickshell.spec"
LATEST=$(curl -s "https://api.github.com/repos/$REPO_STABLE/releases/latest" | jq -r .tag_name | sed 's/^v//')
CURRENT=$(grep '^Version:' "$SPEC" | awk '{print $2}')

if [ "$LATEST" != "$CURRENT" ]; then
    TAG_COMMIT=$(curl -s "https://api.github.com/repos/$REPO_STABLE/git/refs/tags/v${LATEST}" | jq -r .object.sha)
    # Dereference annotated tags
    TAG_TYPE=$(curl -s "https://api.github.com/repos/$REPO_STABLE/git/tags/$TAG_COMMIT" 2>/dev/null | jq -r '.object.type // empty')
    if [ "$TAG_TYPE" = "commit" ]; then
        TAG_COMMIT=$(curl -s "https://api.github.com/repos/$REPO_STABLE/git/tags/$TAG_COMMIT" | jq -r .object.sha)
    fi

    SOURCE_URL="https://github.com/${REPO_STABLE}/archive/v${LATEST}/quickshell-${LATEST}.tar.gz"
    if curl --output /dev/null --silent --head --fail "$SOURCE_URL"; then
        sed -i "s/^Version:.*/Version:            ${LATEST}/" "$SPEC"
        sed -i "s/^%global commit.*/%global commit      ${TAG_COMMIT}/" "$SPEC"
        echo "Updated $SPEC to version $LATEST"
    else
        echo "Warning: Source for quickshell ${LATEST} not available yet"
    fi
else
    echo "$SPEC is already at latest version: $CURRENT"
fi

# --- quickshell-git.spec (upstream rolling) ---
SPEC="quickshell-git.spec"
LATEST_COMMIT=$(curl -s "https://api.github.com/repos/$REPO_STABLE/commits/master" | jq -r .sha)
CURRENT_COMMIT=$(grep '^%global commit' "$SPEC" | awk '{print $3}')

if [ "$LATEST_COMMIT" != "$CURRENT_COMMIT" ]; then
    COMMIT_COUNT=$(curl -s "https://api.github.com/repos/$REPO_STABLE/commits?sha=master&per_page=1" -I 2>/dev/null | grep -i '^link:' | sed 's/.*page=\([0-9]*\)>; rel="last".*/\1/')
    SNAPDATE=$(date +%Y%m%d)
    LATEST_TAG=$(curl -s "https://api.github.com/repos/$REPO_STABLE/releases/latest" | jq -r .tag_name | sed 's/^v//')

    sed -i "s/^%global commit.*/%global commit      ${LATEST_COMMIT}/" "$SPEC"
    sed -i "s/^%global commits.*/%global commits     ${COMMIT_COUNT}/" "$SPEC"
    sed -i "s/^%global snapdate.*/%global snapdate    ${SNAPDATE}/" "$SPEC"
    sed -i "s/^%global tag.*/%global tag         ${LATEST_TAG}/" "$SPEC"
    echo "Updated $SPEC to commit ${LATEST_COMMIT:0:7}"
else
    echo "$SPEC is already at latest commit: ${CURRENT_COMMIT:0:7}"
fi

# --- quickshellX-git.spec (fork rolling) ---
SPEC="quickshellX-git.spec"
LATEST_COMMIT=$(curl -s "https://api.github.com/repos/$REPO_FORK/commits/main" | jq -r .sha)
CURRENT_COMMIT=$(grep '^%global commit' "$SPEC" | awk '{print $3}')

if [ "$LATEST_COMMIT" != "$CURRENT_COMMIT" ]; then
    COMMIT_COUNT=$(curl -s "https://api.github.com/repos/$REPO_FORK/commits?sha=main&per_page=1" -I 2>/dev/null | grep -i '^link:' | sed 's/.*page=\([0-9]*\)>; rel="last".*/\1/')
    SNAPDATE=$(date +%Y%m%d)
    LATEST_TAG=$(curl -s "https://api.github.com/repos/$REPO_STABLE/releases/latest" | jq -r .tag_name | sed 's/^v//')

    sed -i "s/^%global commit.*/%global commit      ${LATEST_COMMIT}/" "$SPEC"
    sed -i "s/^%global commits.*/%global commits     ${COMMIT_COUNT}/" "$SPEC"
    sed -i "s/^%global snapdate.*/%global snapdate    ${SNAPDATE}/" "$SPEC"
    sed -i "s/^%global tag.*/%global tag         ${LATEST_TAG}/" "$SPEC"
    echo "Updated $SPEC to commit ${LATEST_COMMIT:0:7}"
else
    echo "$SPEC is already at latest commit: ${CURRENT_COMMIT:0:7}"
fi
