#!/bin/sh 

cd src
git clone http://github.com/festvox/flite
cd flite
./configure
make
make get_voices
sudo apt install pulseaudio
sudo apt install libpulse-dev
sudo apt install osspd
sudo apt install sox
