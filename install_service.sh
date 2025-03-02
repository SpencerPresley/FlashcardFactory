#!/bin/bash

# Get the absolute path of the current directory
CURRENT_DIR=$(pwd)

# Update the service file with the correct path
sed -i "s|/path/to/HenHacks2025|$CURRENT_DIR|g" flashcard-factory.service

# Copy the service file to systemd directory
sudo cp flashcard-factory.service /etc/systemd/system/

# Reload systemd to recognize the new service
sudo systemctl daemon-reload

# Enable the service to start on boot
sudo systemctl enable flashcard-factory.service

# Start the service
sudo systemctl start flashcard-factory.service

echo "FlashcardFactory service has been installed and started."
echo "You can check its status with: sudo systemctl status flashcard-factory.service" 