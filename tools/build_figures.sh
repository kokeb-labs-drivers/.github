#!/bin/sh
# Rebuild the profile figures. Models live in tools/figures/docs/model; the SVGs the README shows are copied to
# profile/img. Needs the theme package: pip install ./packages/kokeb-mkdocs-theme from kokeb-labs/ci-tools.
set -eu
here=$(cd "$(dirname "$0")" && pwd)
cd "$here/figures"
kokeb-docs figures "$@"
mkdir -p "$here/../profile/img"
for id in driver-layers driver-pipeline hardware-levels; do
  cp "docs/diagrams/$id.svg" "docs/diagrams/$id.dark.svg" "$here/../profile/img/"
done
