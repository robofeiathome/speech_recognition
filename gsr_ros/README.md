## gsr_ros ##

**PYTHON**
    - Python 2.7

**General Speech Recognition**
    - Ros package for Speech Recognition
    - Online and Offline Speech Recognition APIs

**APIs**
    - Sphinx (PocketSphinx)
    - Google Speech Recognition
    - WIT.ai
    - Houndify
    - DeepSpeech

## Install ##

**_To install this pkg you must git clone the repo:_**

    $ git clone https://gitlab.com/robofei/at-home/gsr_ros.git

**_Then you will need to run the install shell script which can be found in the gsr_ros folder:_**
    
    $ cd gsr_ros
    $ ./install.sh

That's it, you installed the gsr_ros pkg!

**Changing the API**

If you want to change the API you'll use, just go to the launch file,    
just change the param named API, the options are:

- Google (Online);
- Wit.ai (Online);
- Sphinx (Offline);
- DeepSpeech (Offline);
- Houndify (Online).

**API Register**

You will notice that some APIs, like WIT.ai and Houndify, require an ID.

You'll need to go their site and create an account. After that, just change
the value of the KEY1 and KEY2 in the launch file.

*_KEY1 is the Client ID and KEY2 is the Client Key for the Houndify API._*

*_KEY1 is the App ID and KEY2 is the Client Access Token for Wit.ai._*
    
DONE, now you can use those APIs for speech recognition.

Thanks for downloading!
