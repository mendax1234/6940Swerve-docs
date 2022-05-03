The Math Behind the Magic
===========================
One of the core differences when operating in autonomous mode is that the robot can’t receive
information about where it is from the driver, in the form of controls. Early on, we established that
we want to accurately and repeatably control our movements and actions. To do this, the robot
needs to know where it is at all times - or at least have a good guess. This is known as `odometry <https://en.wikipedia.org/wiki/Odometry>`_
within the field of robotics. Without accurate odometry, we’re forced to use `dead reckoning <https://en.wikipedia.org/wiki/Dead_reckoning>`_ , or
worse, time-based movements at approximate speeds.

In order to perform our odometry, we decided to use our wheel encoders combined with a
gyroscope. By performing the reverse of what we do in teleop, which is taking an intended output
pose and figuring out what each individual actuator should be doing to achieve that pose. Again, a
pose is simply a set of unique characteristics describing the robot’s position or motion at an instant
in time. By taking information about the velocity and direction of each wheel and combining it using
the kinematics we described in section 2.1, we can obtain an overall velocity of the robot in two
directions; this is referred to as Forward Kinematics, or FK. By integrating this over time (just
multiplying the velocity at this time with the time step of the controller), we can get our position.

Forward Kinematics (FK)
------------------------
Of course, going from wheel encoders to overall velocity is not entirely straightforward. The
problem comes when we look at our information and desired results: we have eight variables, four
wheel speeds and four directions, and we want three outputs: the robot’s forward, sideways, and
rotational velocity. If you’re familiar with algebra, especially linear algebra, you might recognize that
this makes our system overdefined. We have more information than we need, and can’t obtain an
exact analytic solution. There’s a couple ways to solve this. By `setting up the exact equations and putting them into a computer algebra system <https://www.chiefdelphi.com/t/paper-4-wheel-independent-drive-independent-steering-swerve/107383>`_
, or by assembling the equations in a matrix-vector
format and using a linear equation solver, we can obtain a “best-fit” to the system.

However, this sort of inexact fitting can be difficult to implement, often requiring inclusion of extra
libraries. Due to the time sensitivity of the season, we chose to take a simplified approach. `Courtesy of Kyle Lanman of team 2841, we adapted an algorithm <https://www.chiefdelphi.com/t/calculating-odometry-of-a-swerve-drive/160043/6>`_
that averages variables until we get from
eight down to the three we need. While we expect this to be less accurate than more advanced
methods, we found it to be remarkably accurate after calibration. As long as wheel speeds and
acceleration are kept below the point where they’d slip under normal conditions, this proves to be a
suitable odometry method for the limitations of the 15 second autonomous period, especially when
combined with other sensors to “close the loop” on navigation.

In this formulation of forward kinematics, we start from a position where we assume we know our
wheel speeds and wheel angles; call them with :math:`ws_{FR}`,:math:`ws_{FL}`,:math:`wa_{RL}`,and so on, with F/R and L/R again
representing front/rear and left/right. Using motors that have a built in encoder, such as CTRE
Falcon 500s or REV Neos, is advantageous for determining wheel speed.

We do need to make sure we’ve consistent, physically meaningful values for our wheel speeds.
Whether we’re using encoders built into the motor or ones installed manually, they’re likely putting
out some counter of ticks, or count of revolutions, or some speed of ticks/second or
revolutions/second. We’ll need to use this in combination with our drivetrain reduction and wheel
diameter to get some conversion rate, and thus be able to get our wheel speeds in units of distance
per time, like in/sec, ft/sec, or m/sec.

We can first calculate A, B, C, and D values from our wheelspeeds and angles, but this time, we’re
going to calculate them for each wheel. These will be in units of velocity (distance per me), as we’re
simply multiplying our wheel speed (which has those units) by an angle component.