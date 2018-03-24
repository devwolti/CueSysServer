# CueSysServer
Cue System for Stage purposes. Written in Python

# Why?
A lot of small drama/theater clubs do not have the money to go for big stage systems, but the projects are mostly not getting smaller or easier. This is an approach to solve this problem in a cheap and easy way. The system is far from perfect and does not intend to be, but you are welcome to contribute. Maybe we can build something great. We are using it at the moment with a server on X86 and Raspberry PIs with a touchscreen as clients. Why Pyton? Good question, i know, it was made in hell (and i hate frameworks, because they always have more bugs than features). But there is not a fast and easy cross platform language (and no, java was not an option, because of the jvm and the RPi). Feel free to write clients/servers for it in any language you want, i'll publish all protocols. This project tries to be as open as it can be.

# Milestones

Alpha
Build a running alpha which can display cues and the clients can be controlled by the master

Improvements:
- a "real" non just text protocol (works as a first sketch though)
- mobile version (even though mobile devices and wifi do not really belong in a failsafe scenario where the wifi quality changes with the amount of people in the room)
- usability improvements
- connection to the main project (complete show system for cues/light/automation and so on)


# Install instructions Linux (Ubuntu)

You need the dev version of kivy, because else it won't work with twisted (whyever someone would build frameworks like that (both of them))

apt-get install  git python3-pip python-setuptools python-pygame python-opengl   python-gst0.10 python-enchant gstreamer0.10-plugins-good python-dev   build-essential python-pip libgl1-mesa-dev libgles2-mesa-dev zlib1g-dev
apt-get install python3-kivy
sudo apt-get install -y \
    python-pip \
    build-essential \
    git \
    python \
    python-dev \
    ffmpeg \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    zlib1g-dev
sudo apt-get install -y \
    libgstreamer1.0 \
    gstreamer1.0-plugins-base \
    gstreamer1.0-plugins-good
pip3 install --upgrade pip
pip3 install --upgrade Cython==0.27.3
pip3 install twisted
pip3 install pygame
pip3 install git+https://github.com/kivy/kivy.git@master

# Install instructions Windows


python -m pip install --upgrade pip wheel setuptools
python -m pip install docutils pygments pypiwin32 kivy.deps.sdl2 kivy.deps.glew
python -m pip install kivy.deps.gstreamer (If you encounter a MemoryError while installing, add after pip install an option –no-cache-dir)
python -m pip install https://kivy.org/downloads/appveyor/kivy/Kivy-1.10.1.dev0-cp36-cp36m-win32.whl

python -m pip install twisted (Maybe you have to install C++ build tools)

