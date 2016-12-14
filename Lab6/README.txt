Lab #6
Team Members: Frank Cabada(fc2452), Stephanie Burgos(sb3539), Daniel Rojas(dhr2119)


Files
------------------------------------------------------------------------------
part1.py
part2.py
obstacles.txt
start_goal.txt

part1.py:
This is for the single tree

obstacles.txt:
Sample obstacle coordinates given from lab instructions.

start_goal.txt:
Sample goal coordinates give from lab instructions.


Invoking the programs
------------------------------------------------------------------------------
You can copy paste the following to run the programs.
Invoke part 1: python part1.py obstacles.txt start_goal.txt
Invoke part 2: python part2.py obstacles.txt start_goal.txt


Outcome
------------------------------------------------------------------------------
Both part 1 and part 2 work as described in the lab instructions.
However, there is a bug that sometimes occurs. Sometimes the tree will intersect with an obstacle. This always occurs on a horizontal line of an obstacle. We have spent a lot of time trying to fix this error but were unable to. This doesn't affect the program from finding a path to the goal which is the good part.
With more time, we would like to fix this bug.

Also, in part 2 each tree is drawn all at once even though the trees are taking turns as they grow like they should according to the algorithm. It is much easier to run the calculations for the trees to extend and then afterward give each tree to Turtle to draw it. So even through it will draw the blue tree first and then the red tree, we did follow the correct algorithm of swapping the trees as they extend.