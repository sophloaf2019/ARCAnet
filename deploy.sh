#!/bin/bash

# Configuration
REPO="sophloaf2019/ARCAnet" # Replace with your GitHub username/repo
BRANCH="main"                             # Replace with the branch you want to track (e.g., main)
APP_DIR="./"               # Replace with the path to your app on the droplet
VENV_DIR="./venv"             # Replace with the path to your virtual environment
APP_SCRIPT="run.py"                   # Replace with your app's main script

# Step 1: Check the latest commit hash on GitHub
echo "Checking for updates..."
LATEST_COMMIT=$(curl -s "https://api.github.com/repos/$REPO/commits/$BRANCH" | grep -oP '"sha": "\K[0-9a-fA-F]{40}')

# Step 2: Check the current commit hash on the droplet
cd $APP_DIR
CURRENT_COMMIT=$(git rev-parse HEAD)

# Step 3: Compare the commits
if [ "$LATEST_COMMIT" != "$CURRENT_COMMIT" ]; then
    echo "New version available. Deploying update..."

    # Step 4: Stop the server
    echo "Stopping the server..."
    pkill -f "$APP_SCRIPT" # Replace this if you use a different method to stop your server

    # Step 5: Pull the latest changes from GitHub
    echo "Pulling the latest changes from GitHub..."
    git fetch origin $BRANCH
    git reset --hard origin/$BRANCH

    # Step 6: Check if virtual environment exists, create if necessary
    if [ ! -d "$VENV_DIR" ]; then
        echo "Creating a new virtual environment..."
        python3 -m venv $VENV_DIR
    else
        echo "Virtual environment already exists. Reusing..."
    fi

    # Step 7: Activate the virtual environment
    echo "Activating the virtual environment..."
    source $VENV_DIR/bin/activate

    # Step 8: Install dependencies
    echo "Installing dependencies..."
    pip install --upgrade pip
    pip install -r requirements.txt

    # Step 9: Restart the server
    echo "Restarting the server..."
    nohup python $APP_SCRIPT &

    echo "Deployment complete!"
else
    echo "No new version available. The server is up-to-date."
fi
