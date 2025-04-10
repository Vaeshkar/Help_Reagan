#!/bin/bash

# Move to script's directory
cd "$(dirname "$0")"

# Debug: print current directory
echo "Current directory: $(pwd)"

# Make sure the binary is executable
chmod +x help_reagan || { echo "Failed to make help_reagan executable"; read -p "Press [Enter] to close..."; exit 1; }

# Launch the game
./help_reagan || { echo "Failed to launch help_reagan"; read -p "Press [Enter] to close..."; exit 1; }

# Pause at the end
read -p "Game exited. Press [Enter] to close..."