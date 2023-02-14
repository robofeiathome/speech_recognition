#!/bin/bash

#distribution=${1:-noetic} 

apt-get install -y libasound-dev
apt-get install -y portaudio19-dev
apt-get install -y libportaudio2
apt-get install -y libportaudiocpp0

pip install gTTS
pip install speechrecognition
pip install jellyfish
pip install PyAudio

