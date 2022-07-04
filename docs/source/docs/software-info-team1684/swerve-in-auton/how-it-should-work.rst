How It Should Work
====================
We want to tell the robot to go to a coordinate on the field and face a specific direction when it gets
there. Sometimes we want the rotation to happen at different places along the route. Sometimes
we want it to rotate first or last. Sometimes we even want the robot to travel around an obstacle.
The robot should switch modes as desired along the overall route to achieve the game objectives.
We used a case generator to give us each motion in the desired order and change states primarily
by sensors. The end result should be a robot that travels at the maximum controllable speed while
achieving the desired positions with maximum accuracy.