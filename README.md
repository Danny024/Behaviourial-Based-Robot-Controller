# Behaviourial Based Robot Controller
This project controls the navigation of an epuck robot  about a maze on Webot by checking if there is a black square on the maze.
The epuck robot makes use of a ground sensor to determine if there is a black square on the maze and uses the 8 proximity sensors of the epuck to control the robot navigation.
If there is a black square the robot end goal is at the right of the maze but if thers is no black square the robots end goal is to the left of the maze.

**Video Demonstration**

[![BBR robot](https://img.youtube.com/vi/0VuvZOtGc2o/0.jpg)](https://www.youtube.com/watch?v=0VuvZOtGc2o)
## Guide
```
The directory to the BBR Python Code is :

controllers / bbr_controller /bbr_controller.py

To launch the 2 Webot World go to:

worlds/e-puck_Robotics_TMaze_WithoutBlackSquare(1).wbt

worlds/e-puck_Robotics_TMaze_WithBlackSquare.wbt
```
