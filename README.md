# CueSysServer
Cue System for Stage purposes. Written in Python


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

TBD (but it works, because i am developing under Windows)
