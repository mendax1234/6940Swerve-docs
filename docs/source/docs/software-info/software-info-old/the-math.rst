The Maths
===========

Controls and Inputs
--------------------

The driver has some intended output that they’d like the robot to do. In order to communicate this,
we define three command inputs - Forward, Strafe, and Rotation, or FWD, STR, and ROT. Let’s
define these as variables, each going from -1 to 1, with 0 indicating no control input. There are many
ways to map driver inputs to these commands via joysticks, but we chose to use a method where
one stick controls translation rate (FWD and STR) and the other’s left-right axis controls rotation
rate (ROT), as shown on the controller. These joysticks are implemented using standard libraries in
WPILib, and input is filtered and transformed to provide a better experience to the drivers.
In addition to the driver’s inputs, we can have inputs incorporated.
