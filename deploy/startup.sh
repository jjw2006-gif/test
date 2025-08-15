#!/usr/bin/env bash
# Startup script executed on the GCP VM.  It installs system and Python
# dependencies, clones this repository, and launches the Streamlit app so it is
# accessible from outside the instance.

set -euo pipefail

# ---- Configuration --------------------------------------------------------
APP_DIR="/opt/dice_app"                       # Where to place the application
REPO_URL="https://github.com/your-org/your-repo.git"  # Public Git repository URL

# ---- System Setup ---------------------------------------------------------
# Update package list and install Python, pip and Git.  These packages are
# sufficient for running the Streamlit application.
apt-get update
apt-get install -y python3-pip git

# ---- Application Code -----------------------------------------------------
# Fetch the application source code from the repository.
mkdir -p "$APP_DIR"
cd "$APP_DIR"
if [ ! -d repo ]; then
    git clone "$REPO_URL" repo
fi
cd repo

# ---- Python Dependencies --------------------------------------------------
# Install required Python packages.  ``pip3`` is used instead of ``pip`` to
# ensure the Python 3 version is invoked.
pip3 install --upgrade pip
pip3 install -r requirements.txt

# ---- Run the Streamlit App -----------------------------------------------
# Launch the Streamlit server.  ``--server.address 0.0.0.0`` makes the service
# listen on all interfaces so it can be reached from the internet.  ``nohup``
# keeps the process running after the startup script exits and redirects output
# to a log file for later inspection.
nohup streamlit run src/dice_agent/streamlit_app.py \
    --server.address 0.0.0.0 \
    --server.port 8501 \
    > /var/log/streamlit.log 2>&1 &
