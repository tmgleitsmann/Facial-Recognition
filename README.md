# Facial-Recognition
Python program that uses opencv and MongoDB to retrieve user specific data based off of facial recognition.
Be sure to install cascades w/ opencv and have an image folder with profile pictures. 
pip install numpy, opencv-contrib-python, opencv, pillow, and pymongo in your virtualenv.
Use the appropriate connection string.

Step1:
Execute faces-train.py (training program)
Step2:
execute OCVTest.py
This program will launch any capture device and start recording for faces & eyes.
Once a face is captured in a frame, if it meets the confidence criteria (40 to start with, my picture quality is very low)
then it appends the image label to a list and creates a dictionary slot for it if it isn't already present. The dictionary determines 
the frequency that the face appears. 
ie) if tom-gleitsmann appears 8 times then {tom-gleitsmann: 8}
Once a label is recorded 10 times then it sends that label to mongoConnect.py and searches the database for the corresponding person's data.
This is then returned to OCVTest.py and the program terminates. 
