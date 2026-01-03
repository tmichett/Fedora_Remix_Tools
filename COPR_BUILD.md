# COPR Build Guide for Fedora Remix Tools

This guide explains how to build and publish the Fedora Remix Tools RPM package to [COPR](https://copr.fedorainfracloud.org/) (Cool Other Package Repo).

## Table of Contents

- [Prerequisites](#prerequisites)
- [Setting Up copr-cli Authentication](#setting-up-copr-cli-authentication)
- [Building the RPM Locally](#building-the-rpm-locally)
- [Uploading to COPR](#uploading-to-copr)
- [COPR Project Configuration](#copr-project-configuration)
- [Troubleshooting](#troubleshooting)

## Prerequisites

### Install Required Packages

```bash
sudo dnf install copr-cli rpm-build
```

### Clone the Repository

```bash
git clone https://github.com/tmichett/Fedora_Remix_Tools.git
cd Fedora_Remix_Tools
```

## Setting Up copr-cli Authentication

`copr-cli` requires authentication to upload packages. You have two options:

### Option 1: API Token (Recommended)

1. **Get your API token:**
   - Go to: https://copr.fedorainfracloud.org/api/
   - Log in with your Fedora Account (FAS)
   - The page will display your API configuration

2. **Create the configuration file:**

   ```bash
   mkdir -p ~/.config
   nano ~/.config/copr
   ```

3. **Paste the configuration** (example format):

   ```ini
   [copr-cli]
   login = your-fas-username
   username = your-fas-username
   token = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
   copr_url = https://copr.fedorainfracloud.org
   ```

4. **Secure the file:**

   ```bash
   chmod 600 ~/.config/copr
   ```

### Option 2: Kerberos Authentication

If you have a Fedora Account with Kerberos configured:

```bash
# Get a Kerberos ticket
kinit your-fas-username@FEDORAPROJECT.ORG

# Verify the ticket
klist

# Now copr-cli will use Kerberos automatically
copr-cli whoami
```

## Building the RPM Locally

### Step 1: Create the Source Tarball and Build

```bash
cd Fedora_Remix_Tools
./RPM_Build.sh
```

This script:
1. Creates a source tarball from the SOURCES directory
2. Copies the rpmbuild structure to `~/rpmbuild/`
3. Builds both the SRPM and binary RPM

### Step 2: Verify the Build

```bash
# Check the SRPM was created
ls -la ~/rpmbuild/SRPMS/

# Check the binary RPM was created
ls -la ~/rpmbuild/RPMS/noarch/
```

Expected output:
- `~/rpmbuild/SRPMS/fedora_remix_tools-1.0-9.src.rpm`
- `~/rpmbuild/RPMS/noarch/fedora_remix_tools-1.0-9.noarch.rpm`

## Uploading to COPR

### Method 1: Using copr-cli (Command Line)

```bash
# Upload and build the SRPM
copr-cli build tmichett/FedoraRemix ~/rpmbuild/SRPMS/fedora_remix_tools-1.0-9.src.rpm

# Watch the build progress
copr-cli watch-build <build-id>
```

### Method 2: Web Upload

1. Go to: https://copr.fedorainfracloud.org/coprs/tmichett/FedoraRemix/add_build_upload/
2. Click **"Choose File"** and select `~/rpmbuild/SRPMS/fedora_remix_tools-1.0-9.src.rpm`
3. Select the target chroots (e.g., `fedora-43-x86_64`, `fedora-42-x86_64`)
4. Click **"Build"**

### Method 3: SCM Build from GitHub

If you want COPR to build directly from the GitHub repository:

1. Go to: https://copr.fedorainfracloud.org/coprs/tmichett/FedoraRemix/package/fedora_remix_tools/edit
2. Configure:
   - **Source Type**: `SCM`
   - **Clone URL**: `https://github.com/tmichett/Fedora_Remix_Tools.git`
   - **Subdirectory**: *(leave empty)*
   - **Spec file**: `rpmbuild/SPECS/FedoraRemixTools.spec`
   - **SRPM build method**: `make_srpm`
3. Save and click **"Rebuild"**

## COPR Project Configuration

### Creating a New COPR Project

```bash
# Create a new project
copr-cli create --chroot fedora-43-x86_64 \
                --chroot fedora-42-x86_64 \
                --chroot fedora-41-x86_64 \
                --description "Fedora Remix Tools and Customization" \
                FedoraRemix
```

### Adding a Package to the Project

```bash
# Add package configuration for SCM builds
copr-cli add-package-scm tmichett/FedoraRemix \
    --name fedora_remix_tools \
    --clone-url https://github.com/tmichett/Fedora_Remix_Tools.git \
    --spec rpmbuild/SPECS/FedoraRemixTools.spec \
    --method make_srpm
```

## Installing from COPR

Once the package is built and available:

```bash
# Enable the COPR repository
sudo dnf copr enable tmichett/FedoraRemix

# Install the package
sudo dnf install fedora_remix_tools
```

## Troubleshooting

### Authentication Errors

**Error:** `401 Unauthorized` or `No credentials were supplied`

**Solution:** Your API token may be expired or not configured:
1. Go to https://copr.fedorainfracloud.org/api/
2. Copy the new configuration
3. Update `~/.config/copr`

### Build Fails with "No such file or directory"

**Error:** `cp: cannot stat '/builddir/build/SOURCES/config.yml': No such file or directory`

**Solution:** The spec file expects a source tarball. Make sure to:
1. Run `./create_tarball.sh` first
2. Or use `./RPM_Build.sh` which does this automatically
3. Upload the SRPM (not trigger a rebuild from dist-git)

### SRPM Build Method Issues

If COPR's SCM build fails, try:
1. Change the SRPM build method to `make_srpm`
2. Ensure the `.copr/Makefile` exists in the repository
3. Or upload the SRPM directly instead of using SCM

### Checking Build Logs

```bash
# List recent builds
copr-cli list-builds tmichett/FedoraRemix

# Get build details
copr-cli get-build <build-id>
```

Or view logs at: `https://download.copr.fedorainfracloud.org/results/tmichett/FedoraRemix/`

## File Structure

```
Fedora_Remix_Tools/
├── .copr/
│   └── Makefile              # COPR make_srpm build instructions
├── rpmbuild/
│   ├── SOURCES/
│   │   ├── config.yml
│   │   ├── menu.py
│   │   ├── fedora_remix_tools.sh
│   │   ├── trust-desktop-icons.sh
│   │   ├── Fedora_Remix_Tools.desktop
│   │   ├── fedora-remix-tools-trust.desktop
│   │   └── *.png
│   └── SPECS/
│       └── FedoraRemixTools.spec
├── create_tarball.sh         # Creates source tarball
├── RPM_Build.sh              # Builds RPM locally
└── COPR_BUILD.md             # This file
```

## Useful Commands

```bash
# Check your COPR authentication
copr-cli whoami

# List your projects
copr-cli list

# List packages in a project
copr-cli list-packages tmichett/FedoraRemix

# Trigger a rebuild of existing package
copr-cli build-package tmichett/FedoraRemix --name fedora_remix_tools

# Delete a build
copr-cli delete-build <build-id>
```

## References

- [COPR Documentation](https://docs.pagure.org/copr.copr/)
- [copr-cli Manual](https://docs.pagure.org/copr.copr/user_documentation.html#client)
- [COPR API](https://copr.fedorainfracloud.org/api/)
- [Fedora Account System](https://accounts.fedoraproject.org/)



