Lab #5
Team Members: Frank Cabada(fc2452), Stephanie Burgos(sb3539), Daniel Rojas(dhr2119)

Files
------------------------------------------------------------------------------
path.py
coordinates.txt
roborace.txt

path.py:
Contains the control flow of the program.

coordinates.txt:
Sample coordinates given from lab instructions.

roborace.txt:
Coordinates given from the professor for roborace.

Robot Dimensions 
------------------------------------------------------------------------------
Size: 26cm x 16cm 
Virtual Size: R_LENGTH = 26, R_WIDTH = 16 (rectangle)
Reflection Reference Point: front, left corner (front begins pointing towards 0 degrees and is adjusted to point in the direction of the goal)

Invoking program details
------------------------------------------------------------------------------
Invoke program: python path.py [coordinate file]
Example: python path.py coordinates.txt

A coordinates file is needed to supply object and world information. The format is as specified in the lab instructions.


Outcome
------------------------------------------------------------------------------
The program works as intended and follows all lab instructions.
The extra credit is not implemented so the robot movement may not be as precise in the real world due to lobsided wheels and tractions problems.