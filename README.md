# im-camera
Python code based on OpenCV to add vision to IM

#  Activate Camera on RPI

```shell
#!/bin/bash
grep "start_x=1" /boot/config.txt
if grep "start_x=1" /boot/config.txt
then
        exit
else
        sed -i "s/start_x=0/start_x=1/g" /boot/config.txt
        reboot
fi
exit
```

# L'installation de base

1. Python-opencv

```shell
$ sudo apt-get install python-opencv
```

2. Et piCamera
 
```shell
$ sudo pip install picamera
```

# Hot compile Installation

(for RPI3 with Raspbian Jessie)

## prepare 

1. Expand FileSystem if needed

```shell
$ sudo raspi-config
```

2. Select "Expand FileSystem"

3. Reboot

4. Check

```shell
df -
```

5. update and upgrade OS

```shell
$ sudo apt-get update
$ sudo apt-get upgrade
```

6. install dependencies

```shell
$ sudo apt-get install build-essential cmake pkg-config
$ sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
$ sudo apt-get install libxvidcore-dev libx264-dev
$ sudo apt-get install libgtk2.0-dev
$ sudo apt-get install libatlas-base-dev gfortran
$ sudo apt-get install python2.7-dev python3-dev
```

7. Download OpenCV3.0 sources

```shell
$ cd ~
$ wget -O opencv.zip https://github.com/opencv/opencv/archive/3.3.0.zip
$ unzip opencv.zip
$ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/3.3.0.zip
$ unzip opencv_contrib.zip
```

8. Install pip

```shell
$ wget https://bootstrap.pypa.io/get-pip.py
$ sudo python get-pip.py
```

9. Install numpy

```shell
$ pip install numpy
```

10. Compile OpenCV

```shell
$ cd ~/opencv-3.3.0/
$ mkdir build
$ cd build
$ cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
    -DBUILD_PYTHON2=ON \
    ..
# Mac example
cmake -D CMAKE_BUILD_TYPE=RELEASE \
    -D CMAKE_INSTALL_PREFIX=/usr/local \
    -D OPENCV_EXTRA_MODULES_PATH=/Users/rguillome/Documents/code/opencv_contrib/modules \
    -D PYTHON2_LIBRARY=/usr/local/Cellar/python@2/2.7.14_1/Frameworks/Python.framework/Versions/2.7/lib/libpython2.7.dylib \
    -D PYTHON2_INCLUDE_DIR=/usr/local/Cellar/python@2/2.7.14_1/Frameworks/Python.framework/Versions/2.7/include/python2.7 \
    -D BUILD_opencv_python2=ON \
    -D BUILD_opencv_python3=OFF \
    -D INSTALL_PYTHON_EXAMPLES=ON \
    -D INSTALL_C_EXAMPLES=OFF \
    -D BUILD_EXAMPLES=OFF ..

$ make -j4
$ sudo make install
$ sudo ldconfig
```

11. Test

```shell
$ python
>>> import cv2
>>> cv2.__version__
'3.3.0'
>>>
```


