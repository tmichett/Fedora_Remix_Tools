#!/bin/bash
# Script to create source tarball for COPR builds

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VERSION="1.0"
NAME="fedora_remix_tools"
TARBALL_DIR="${NAME}-${VERSION}"

echo "Creating source tarball for ${NAME}-${VERSION}..."

# Create temporary directory structure
rm -rf /tmp/${TARBALL_DIR}
mkdir -p /tmp/${TARBALL_DIR}

# Copy all source files
cp rpmbuild/SOURCES/config.yml /tmp/${TARBALL_DIR}/
cp rpmbuild/SOURCES/menu.py /tmp/${TARBALL_DIR}/
cp rpmbuild/SOURCES/logo.png /tmp/${TARBALL_DIR}/
cp rpmbuild/SOURCES/smallicon.png /tmp/${TARBALL_DIR}/
cp rpmbuild/SOURCES/fedora_remix_tools.sh /tmp/${TARBALL_DIR}/
cp rpmbuild/SOURCES/trust-desktop-icons.sh /tmp/${TARBALL_DIR}/
cp rpmbuild/SOURCES/Fedora_Remix_Tools.desktop /tmp/${TARBALL_DIR}/
cp rpmbuild/SOURCES/fedora-remix-tools-trust.desktop /tmp/${TARBALL_DIR}/

# Create tarball
cd /tmp
tar -czvf ${NAME}-${VERSION}.tar.gz ${TARBALL_DIR}

# Move tarball to SOURCES directory
mv ${NAME}-${VERSION}.tar.gz "${SCRIPT_DIR}/rpmbuild/SOURCES/"

# Cleanup
rm -rf /tmp/${TARBALL_DIR}

echo ""
echo "Tarball created: rpmbuild/SOURCES/${NAME}-${VERSION}.tar.gz"
echo ""
echo "To build locally:"
echo "  ./RPM_Build.sh"
echo ""
echo "To upload to COPR:"
echo "  1. Upload the tarball to your COPR project's lookaside cache"
echo "  2. Or use COPR's 'upload srpm' feature after building locally"

