Robotics Lab 3

Team Members: 
Frank Cabada fc2452 
Daniel Rojas dhr2119 
Stephanie Burgos sb3539

The code for this homework is located in lab3.py.

The video can be viewed through this YouTube link:
https://youtu.be/qEcr31dWbm8

There are few code snippets for calculating image histogram found at:
http://docs.opencv.org/3.1.0/dc/df6/tutorial_py_histogram_backprojection.html


Program flow:

The robot takes an initial image in which the user can select a rectangular region. The
user will form this rectangular region starting from the top left to bottom right.
A binary mask is produced from the colors detected in the selected region and this is
the color that the robot will scan for and begin to track.

As the robot continues to take new images, the binary mask in calculated and the robot will
respond to the object's movements. If the object exceeds a certain center threshold the robot
will recenter the object in the camera's view by rotating. If the object moves closer
then the robot will move backward. If the object moves away then the robot will move forward.

Our rotations are set to one encoder count for gradual adjustment throughout multiple images.
This was chosen as it is difficult and can likely cause errors when attempting to rotate the
exact amount to recenter the object with only one a single image reference.

Similarly, forward and backward movements are eight encoder counts. During testing, we found eight
to be an optimal level that wasn't too slow but not a massive overextension which can
cause miscalculations.