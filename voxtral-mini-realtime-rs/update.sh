#!/bin/bash
set -euo pipefail

REPO="TrevorS/voxtral-mini-realtime-rs"
SPEC="voxtral-mini-realtime-rs.spec"

CURRENT_COMMIT=$(grep '%global commit0' "$SPEC" | awk '{print $3}')
LATEST_COMMIT=$(curl -sf "https://api.github.com/repos/$REPO/commits/main" | grep '"sha"' | head -1 | cut -d'"' -f4)

if [ -z "$LATEST_COMMIT" ]; then
    echo "Failed to fetch latest commit"
    exit 0
fi

if [ "$CURRENT_COMMIT" = "$LATEST_COMMIT" ]; then
    echo "voxtral-mini-realtime-rs is up to date ($CURRENT_COMMIT)"
    exit 0
fi

SHORTCOMMIT=${LATEST_COMMIT:0:7}

# Get commit date
LATEST_DATE=$(curl -sf "https://api.github.com/repos/$REPO/commits/$LATEST_COMMIT" | grep '"date"' | head -1 | cut -d'"' -f4 | cut -dT -f1 | tr -d '-')

# Check upstream version from Cargo.toml
UPSTREAM_VER=$(curl -sf "https://raw.githubusercontent.com/$REPO/$LATEST_COMMIT/Cargo.toml" | grep '^version' | head -1 | cut -d'"' -f2)

# Verify source tarball is accessible
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" -L "https://github.com/$REPO/archive/$LATEST_COMMIT.tar.gz")
if [ "$HTTP_CODE" != "200" ]; then
    echo "Source tarball not available (HTTP $HTTP_CODE)"
    exit 0
fi

sed -i "s/%global commit0 .*/%global commit0 $LATEST_COMMIT/" "$SPEC"
sed -i "s/%global date0 .*/%global date0 $LATEST_DATE/" "$SPEC"

if [ -n "$UPSTREAM_VER" ]; then
    sed -i "s/^Version:.*/Version:        $UPSTREAM_VER/" "$SPEC"
fi

echo "Updated voxtral-mini-realtime-rs to $SHORTCOMMIT ($UPSTREAM_VER)"
git add "$SPEC"
git commit -m "Update voxtral-mini-realtime-rs to $SHORTCOMMIT [build-rust]"
git push
