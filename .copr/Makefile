# Makefile for COPR builds
# This file tells COPR how to build the SRPM

srpm:
	# Create the source tarball
	mkdir -p fedora_remix_tools-1.0
	cp rpmbuild/SOURCES/config.yml fedora_remix_tools-1.0/
	cp rpmbuild/SOURCES/menu.py fedora_remix_tools-1.0/
	cp rpmbuild/SOURCES/logo.png fedora_remix_tools-1.0/
	cp rpmbuild/SOURCES/smallicon.png fedora_remix_tools-1.0/
	cp rpmbuild/SOURCES/fedora_remix_tools.sh fedora_remix_tools-1.0/
	cp rpmbuild/SOURCES/trust-desktop-icons.sh fedora_remix_tools-1.0/
	cp rpmbuild/SOURCES/Fedora_Remix_Tools.desktop fedora_remix_tools-1.0/
	cp rpmbuild/SOURCES/fedora-remix-tools-trust.desktop fedora_remix_tools-1.0/
	tar -czvf fedora_remix_tools-1.0.tar.gz fedora_remix_tools-1.0
	rm -rf fedora_remix_tools-1.0
	
	# Build the SRPM
	rpmbuild -bs rpmbuild/SPECS/FedoraRemixTools.spec \
		--define "_sourcedir $(CURDIR)" \
		--define "_srcrpmdir $(outdir)"

