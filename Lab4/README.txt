Lab #4
Team Members: Frank Cabada(fc2452), Stephanie Burgos(sb3539), Daniel Rojas(dhr2119)

Files
------------------------------------------------------------------------------
locate.py
particle.py
robot.py
coordinates.txt

locate.py:
The bulk of the code. Contains the control flow of the program.

particle.py:
Particle class. Functions specific to particles (moving, scanning for obstacles, etc.) is in here.

robot.py:
Robot class that inherits from the particle class.


Invoking program details
------------------------------------------------------------------------------
Invoke program: python locate.py [coordinate file] [particle count]
Example: python locate.py coordinates.txt 5000

A coordinates file is needed to supply world size and obstacle placement. The format is as specified in the lab. Example:
200 200
20 20
40 40
150 200


Program
------------------------------------------------------------------------------
Our program uses the coordinates file to draw the world, obstacles, and stamps the initial particles and robot at random locations.
The particles and robot cannot be chosen to reside on a coordinate that contains an obstacle.
The algorithm will run an amount depending on the value of the MOVES constant. This is how many times the robot and particles are moved and resampled.

Robot action:
The robot is moved a random distance with a max ditance of MAX_DIST and min ditance of MIN_DIST. This is checked to be a valid move.
A valid move means that the robot will not collide with the wall or obstacle.
If not valid, pick another random distance after rotating 45 degrees and this move will be checked again.
If valid, then the robot will be moved and scan the world.

Scanning:
The behavior of particle and robot scanning is the same. They scan 180 degrees in front of them to simulate the scanning range of the GoPiGo.
The scan is checked in 20 degree increments and calculates the distance to an obstacle or wall (or nothing) at each increment.

Particle action:
Particles will mirror the same move as the robot. If this move puts a particle outside of the world, the particle is considered to have stayed at the wall at the point it collides and these particles are given a probability of 0.
The particle will now scan the environment.

Probability measurement and resampling:
Using the data that the particles get from scanning, the distances are compared to the distances scanned by the robot. This is handed off to a Gaussian funciton to calculate the probability and a weight list is created.
This weight list is used to resample the particles to the more probable locations of where the robot may be.

Printing results:
The updated particle list and the robot is used to print the results of the program. This includes the mean error at start, total updates, mean location, mean error, the final coordinates for a specified number of particles, and the actual robot location.


Outcome
------------------------------------------------------------------------------
Currently our program is unable to accurately calculate the robot's position. There seems to be an error with the way probabilities of the particles are calculated.
During certain runs, the particles will converge pretty well but this doesn't happen all of the time.

With more time, we would hope to improve the accuracy of the program. This would involve further debugging of the probability assignment of the particles.