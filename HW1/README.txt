Name: Mawaba Pascal Dao

Source code is in /src folder.

Files to run are
* testTeacher.py
* testNoTeacher.py (Be patient when running this. It will train on 30k games)

Run them using python3 with the expressivity argument (compact or full)

For example:

- python3 testNoTeacher.py compact

Please use compact expressivity for grading, I implemented full expressivity simply for testing purposes.

Description of Files:
- experiment_generator.py: Module that generates new board state for system to train on (Only used in testNoTeacher)
- board_utils.py: Contains all the code for operations that pertain to the board (i.e getStateFetures, invertBoard, isFinalState)
- perf_system.py: Module that actually plays the game. Chooses the move that maximizes v_hat.
- critic.py: Module that assigns value to final state and generates training examples
- play_utils.py: Contains all the code for playing against a human opponent (test mode)
- dojo.txt: Training input file used in testTeacher.py. Every game played against the system by a human are stored here.