#cd src && wget https://github.com/mozilla/DeepSpeech/releases/download/v0.4.1/deepspeech-0.4.1-models.tar.gz && tar xvfz deepspeech-0.4.1-models.tar.gz
sudo apt-get update 
sudo apt-get install libportaudio-dev
sudo apt-get install python3-dev
sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 
sudo apt-get install portaudio19-dev
sudo apt-get install vorbis-tools
sudo apt-get install swig
pip3 install SpeechRecognition
python3 -m pip install --upgrade pip setuptools wheel
pip3 install --upgrade pocketsphinx
cd ~/Downloads && wget https://files.pythonhosted.org/packages/ab/42/b4f04721c5c5bfc196ce156b3c768998ef8c0ae3654ed29ea5020c749a6b/PyAudio-0.2.11.tar.gz
cd ~/Downloads &&  tar xvzf PyAudio-0.2.11.tar.gz
cd ~/Downloads/PyAudio-0.2.11 && sudo python setup.py install
python3 -m pip install jellyfish
python3 -m pip install deepspeech==0.4.1
#pip install deepspeech==0.4.1

sudo chmod +x ./src/recognition.py
