#!/bin/bash

# Deployment Script for Alhilal and Algable systems
# Targeted for Ubuntu 22.04 LTS

# 1. Update system
sudo apt update && sudo apt upgrade -y

# 2. Install dependencies
sudo apt install -y python3-pip python3-venv nginx postgresql postgresql-contrib libpq-dev curl git

# 3. Setup Project Directories
mkdir -p ~/projects
cd ~/projects

# 4. Instructions for User
echo "=========================================================="
echo "Basic server dependencies installed successfully."
echo "=========================================================="
echo "Next steps:"
echo "1. Clone your repository: git clone <your-repo-url> ."
echo "2. Create a virtual environment: python3 -m venv venv"
echo "3. Activate it: source venv/bin/activate"
echo "4. Install requirements: pip install -r requirements.txt"
echo "=========================================================="
