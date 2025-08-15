#!/usr/bin/env bash
# Simple deployment script to run the Streamlit app on a Google Compute Engine VM.
#
# Prerequisites:
#   * The gcloud CLI must be installed and authenticated.
#   * Replace the PROJECT_ID and REPO_URL variables below with your values.
#
# The script performs the following actions:
#   1. Creates a firewall rule to allow inbound traffic to Streamlit's default port (8501).
#   2. Creates a VM instance and attaches the startup script that installs and launches the app.
#   3. After the instance starts, the application will be reachable via http://EXTERNAL_IP:8501.
#
# Usage:
#   bash deploy/gcp_deploy.sh

set -euo pipefail

# ---- Configuration --------------------------------------------------------
PROJECT_ID="your-gcp-project-id"   # ID of your GCP project
ZONE="us-central1-a"               # Compute Engine zone to deploy in
INSTANCE_NAME="dice-streamlit"     # Name for the VM instance
MACHINE_TYPE="e2-micro"            # VM machine type

# Optional: run gcloud in a specific project to avoid passing --project each time
#gcloud config set project "$PROJECT_ID"

# ---- Firewall -------------------------------------------------------------
# Open TCP port 8501 so the Streamlit server can receive external traffic.  If
# the firewall rule already exists, the command will fail.  "|| true" prevents
# the script from stopping in that case.
gcloud compute firewall-rules create allow-streamlit \
    --project="$PROJECT_ID" \
    --allow=tcp:8501 \
    --target-tags=streamlit-server \
    --description="Allow incoming HTTP traffic to Streamlit" || true

# ---- VM Creation ----------------------------------------------------------
# Create a Debian-based VM and attach our startup script.  The script performs
# package installation and launches the app automatically on boot.
gcloud compute instances create "$INSTANCE_NAME" \
    --project="$PROJECT_ID" \
    --zone="$ZONE" \
    --machine-type="$MACHINE_TYPE" \
    --tags=streamlit-server \
    --image-family=debian-11 \
    --image-project=debian-cloud \
    --metadata-from-file startup-script=deploy/startup.sh

# After a couple of minutes the app should be live.  Retrieve the external IP
# with:
#   gcloud compute instances describe "$INSTANCE_NAME" --zone "$ZONE" \
#       --format='get(networkInterfaces[0].accessConfigs[0].natIP)'
