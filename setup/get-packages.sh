# Git
#preinstalled: sudo apt-get install git

#
#preinstalled: sudo apt-get install pigpio python-pigpio python3-pigpio
sudo apt-get install pigpiod
sudo systemctl enable pigpiod

# Prereqs for ApproxEng Redboard
sudo apt-get install libtiff5 libopenjp2-7-dev fonts-dejavu libpython3-dev libjpeg-dev

# Misc build
sudo apt-get install gtkmm-3.0

# for julius speech recognition
sudo apt-get install build-essential zlib1g-dev libsdl2-dev libasound2-dev

# for opencv demos etc.
sudo apt install libhdf5-dev
sudo apt install libatlas3-base libwebp6 libtiff5 libjasper1 libopenexr23 
# possibly should just use qt5 now?
sudo apt install libqtgui4 libqt4-test libqtcore4
# no longer available: libilmbase12 libgstreamer1.0-0 libavcodec57 libavformat57 libavutil55 libswscale4
sudo apt-get install libopenblas-dev liblapack-dev libatlas-base-dev
