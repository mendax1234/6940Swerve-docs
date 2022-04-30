Hardware/Electrical Info
============================

About Our Swerve Modules
-------------------------

We are using the MK5 swerve modules from SJTU.

About Our Gyros
----------------

We use one gyro on our robot. The `Gadgeteer Pigeon IMU <https://store.ctr-electronics.com/gadgeteer-pigeon-imu/>`_ from Cross the Road Electronics (CTRE)
We have also test `NavX-MXP <https://pdocs.kauailabs.com/navx-mxp/>`_ on our robot and it works well.

About Our Motor Controllers
----------------------------

Our choice for motor controllers for the swerve modules was the `Falcon 500 <https://www.vexrobotics.com/217-6515.html>`_ with the integrated
brushless motor by VEX Robotics and the Talon FX controller by CTRE. The reason for using this as
the drive motor was simple, power and control. The integrated encoder is adequate for counting the
distance travelled using the velocity mode to get the most consistent results regardless of voltage
differences (within reason.)

The turning motor is `775 pro <https://www.vexrobotics.com/775pro.html>`_ by VEX Robotics
and the `Talon SRX <https://www.vexrobotics.com/217-8080.html>`_ controller by CTRE.
The reason for using this is that the swerve is designed to use a 775 pro as its turning motor.
Another reason is that we don't have enough Falcon 500 and we want to make full use of them. 
For example, use them on our shooter and intaker.

Other Sensors
--------------
We use several other sensors that weave into our swerve code. The most obvious is the `Limelight2+ <https://limelightvision.io/>`_ .
We also use two `Pixy2 <https://pixycam.com/pixy2/>`_ , two `IR Sensors <https://www.amazon.com/HiLetgo-E18-D80NK-Infrared-Photoelectric-Avoidance/dp/B07VKR1GBJ/ref=sr_1_2?keywords=E18-D80NK&qid=1651325946&sr=8-2>`_ 
and one `REV color sensor <https://www.revrobotics.com/rev-31-1557/>`_.
We will address the exact usage of these sensors in later sections.

The Limelight is used to visually target the goal. We use the x and y offsets that are in the Limelight
to turn the shooter to the goal and gauge the distance from the goal. The Limelight has excellent
range and is able to target the goal from anywhere on the field that has a shooting solution. The
Limelight is mounted in front of our shooter. With the interpoltion table, we can achieve shooting at
every place in the field with the help of Limelight2+.

The Pixy2 is also a visual targeting camera and processor, but due to the color ofthis season's 
(2022 Season Rapid React) cargo (blue and red), Pixy2 may not be able tell the difference between
team's bumper and the cargo, so l am sorry to say that Pixy2 may not be able to be used as a camera 
to do game-piece centric. But we will also introduce the game-piece centric in the later chapters with
Pixy2.

The IR Sensors are used to detect whether we have a ball intaked into our robot. And the REV color sensor
is used to shoot away the wrong color ball. The exact usage of these two sensors will be introduced in the
later chapters.



