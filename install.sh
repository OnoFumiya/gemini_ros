#!/bin/bash

echo "╔══╣ Install: Gemini ROS (STARTING) ╠══╗"

# Keep track of the current directory
DIR=`pwd`

# Clone required packages
cd ..
git clone -b ${ROS_DISTRO}-devel https://github.com/OnoFumiya/ai_interfaces.git
cd ai_interfaces/
bash install.sh

# Install common dependencies
python3 -m pip install --break-system-packages -U pip
python3 -m pip install --break-system-packages \
    google-genai \
    "numpy<2.0"

# Install ROS dependencies
sudo apt update
sudo apt install -y \
    ros-${ROS_DISTRO}-rclpy \
    ros-${ROS_DISTRO}-sensor-msgs \
    ros-${ROS_DISTRO}-cv-bridge \
    ros-${ROS_DISTRO}-image-transport \
    ros-${ROS_DISTRO}-geometry-msgs

# Go back to previous directory
cd ${DIR}


echo "╚══╣ Install: Gemini ROS (FINISHED) ╠══╝"
