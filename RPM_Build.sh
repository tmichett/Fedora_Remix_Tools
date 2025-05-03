#!/bin/bash

cp -avR rpmbuild ~
rpmbuild -ba ~/rpmbuild/SPECS/rhci_foundation.spec
