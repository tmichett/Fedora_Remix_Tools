#!/bin/bash
set -e

# Create the source tarball first
echo "Creating source tarball..."
./create_tarball.sh

# Copy rpmbuild directory to home
cp -avR rpmbuild ~

# Build the RPM
rpmbuild -ba ~/rpmbuild/SPECS/FedoraRemixTools.spec

echo ""
echo "Build complete!"
echo "RPM location: ~/rpmbuild/RPMS/noarch/"
echo "SRPM location: ~/rpmbuild/SRPMS/"
