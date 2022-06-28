The Math Behind the Magic
===========================
One of the core differences when operating in autonomous mode is that the robot can't receive
information about where it is from the driver, in the form of controls. Early on, we established that
we want to accurately and repeatably control our movements and actions. To do this, the robot
needs to know where it is at all times - or at least have a good guess. This is known as `odometry <https://en.wikipedia.org/wiki/Odometry>`_
within the field of robotics. Without accurate odometry, we're forced to use `dead reckoning <https://en.wikipedia.org/wiki/Dead_reckoning>`_ , or
worse, time-based movements at approximate speeds.

In order to perform our odometry, we decided to use our wheel encoders combined with a
gyroscope. By performing the reverse of what we do in teleop, which is taking an intended output
pose and figuring out what each individual actuator should be doing to achieve that pose. Again, a
pose is simply a set of unique characteristics describing the robot's position or motion at an instant
in time. By taking information about the velocity and direction of each wheel and combining it using
the kinematics we described in section 2.1, we can obtain an overall velocity of the robot in two
directions; this is referred to as Forward Kinematics, or FK. By integrating this over time (just
multiplying the velocity at this time with the time step of the controller), we can get our position.

Forward Kinematics (FK)
------------------------
Of course, going from wheel encoders to overall velocity is not entirely straightforward. The
problem comes when we look at our information and desired results: we have eight variables, four
wheel speeds and four directions, and we want three outputs: the robot's forward, sideways, and
rotational velocity. If you're familiar with algebra, especially linear algebra, you might recognize that
this makes our system overdefined. We have more information than we need, and can't obtain an
exact analytic solution. There's a couple ways to solve this. By `setting up the exact equations and putting them into a computer algebra system <https://www.chiefdelphi.com/t/paper-4-wheel-independent-drive-independent-steering-swerve/107383>`_
, or by assembling the equations in a matrix-vector
format and using a linear equation solver, we can obtain a “best-fit” to the system.

However, this sort of inexact fitting can be difficult to implement, often requiring inclusion of extra
libraries. Due to the time sensitivity of the season, we chose to take a simplified approach. `Courtesy of Kyle Lanman of team 2841, we adapted an algorithm <https://www.chiefdelphi.com/t/calculating-odometry-of-a-swerve-drive/160043/6>`_
that averages variables until we get from
eight down to the three we need. While we expect this to be less accurate than more advanced
methods, we found it to be remarkably accurate after calibration. As long as wheel speeds and
acceleration are kept below the point where they'd slip under normal conditions, this proves to be a
suitable odometry method for the limitations of the 15 second autonomous period, especially when
combined with other sensors to “close the loop” on navigation.

In this formulation of forward kinematics, we start from a position where we assume we know our
wheel speeds and wheel angles; call them with :math:`ws_{FR}`, :math:`ws_{FL}`, :math:`wa_{RL}`,and so on, with F/R and L/R again
representing front/rear and left/right. Using motors that have a built in encoder, such as CTRE
Falcon 500s or REV Neos, is advantageous for determining wheel speed.

We do need to make sure we've consistent, physically meaningful values for our wheel speeds.
Whether we're using encoders built into the motor or ones installed manually, they're likely putting
out some counter of ticks, or count of revolutions, or some speed of ticks/second or
revolutions/second. We'll need to use this in combination with our drivetrain reduction and wheel
diameter to get some conversion rate, and thus be able to get our wheel speeds in units of distance
per time, like in/sec, ft/sec, or m/sec.

We can first calculate A, B, C, and D values from our wheelspeeds and angles, but this time, we're
going to calculate them for each wheel. These will be in units of velocity (distance per me), as we're
simply multiplying our wheel speed (which has those units) by an angle component.

.. math:: B_{FL} = sin(wa_{FL}) * ws_{FL}
.. math:: D_{FL} = cos(wa_{FL}) * ws_{FL}
.. math:: B_{FR} = sin(wa_{FR}) * ws_{FR}
.. math:: C_{FR} = cos(wa_{FR}) * ws_{FR}
.. math:: A_{RL} = sin(wa_{RL}) * ws_{RL}
.. math:: D_{RL} = cos(wa_{RL}) * ws_{RL}
.. math:: A_{RR} = sin(wa_{RR}) * ws_{RR}
.. math:: C_{RR} = cos(wa_{RR}) * ws_{RR}

Well that wasn't much help with simplifying our variables! In order to make this more reasonable,
we're going to do some averaging. For each value of A, B, C, and D, we're going to take the two
values we have, and average them. These averaged values will still have units of velocity, as they're
just averaging two other velocity values.

.. math:: A = (A_{RR} + A_{RL})/2
.. math:: B = (B_{FL} + A_{FR})/2
.. math:: C = (C_{FR} + C_{RR})/2
.. math:: D = (D_{FL} + D_{RL})/2

Excellent, that's brought our complexity down some. Now we need to find our rotational velocity, or
ROT. For this, we need physically accurate measurements of what we earlier defined as the length
and width of our wheelbase, L and W. Then, we'll calculate the possible rotational velocity from our
knowledge about the front/back (A/B) and left/right (C/D) velocities, and average those again to get
a single value. Note that it's also possible to get this ROT value (which should be in radians/second)
from a gyroscope, which we should already have on our robot so we can drive field-centric.

.. math:: ROT_{1} = (B − A)/L
.. math:: ROT_{2} = (C − D)/W
.. math:: ROT = (ROT_{1} + ROT_{2})/2

From here, we're simply going to incorporate this with our geometry and A, B, C, D values to obtain
(again) two values each for forward and strafe velocities, and average them to get our final
estimates of forward and strafe speed.

.. math:: FWD_{1} = ROT * (L/2) + A
.. math:: FWD_{2} = − ROT * (L/2) + B
.. math:: FWD = (FWD_{1} + FWD_{2})/2

.. math:: STR_{1} = ROT * (W/2) + C
.. math:: STR_{2} = − ROT * (W/2) + D
.. math:: STR = (STR_{1} + STR_{2})/2

Great! Now we've got something to work with. If we want our distance values to be usefu l, though,
these velocities should be transformed so they're field-centric. Back to our trusty field centric
transformation, we'll again need our angle relative to the field, usually provided by a gyroscope.

.. math:: FWD_{new} = FWD * cos(θ) + STR * sin(θ)
.. math:: STR_{new} = STR * cos(θ) − FWD * sin(θ)

Odometry
-----------
From there, we can now figure out how fast we're actually going along the field - pretty nifty! To get
to a position, we just need to integrate these over time. This is as simple as initializing a timer and
comparing its value at the current loop run to its value in the previous run to determine our
timestep . For most robot code, this timestep is somewhere around 0.020 seconds, or 20
milliseconds; however, this is only a nominal value, and it can vary up and down (mostly up)
depending on the behavior of the robot's code. In any case, we can take this timestep and our speed
and integrate it into an accumulator value to get our position relative to where we started counting.

::

    timeStep = LoopTimer.Get() − lastTime
    positionAlongField = positionAlongField + FWD * timeStep
    positionAcrossField = positionAcrossField + STR * timeStep

We're calling our axis associated with strafing along and our axis associated with moving forward or
back across. This turned out to facilitate communication within our team more easily than axis
conventions like x/y/z.

We now have our odometry. When using it in autonomous routines, we reset this value to zero at the
start, and consider our coordinates relative to where the robot starts. This means robot positioning
is very important, as any error will be carried through the odometry.

When you add the change every cycle, you always know where that wheel is. The same is done for
the other 3 wheels. We use that information to find the center of the robot. The direction that the
robot is facing could also be determined in the same manner, but we chose to use our gyros for
that. We only store the current position of the center of the robot. We do , however, send that
position to the dashboard and record the data there. We are able to graph out the position that the
robot reported and impose it over a map of the field to allow us to make improvements to our
autons even without having access to the robot.

The next part of the puzzle is to tell the robot where to go next. We reverse the tracking process to
instruct each wheel on where to go next. We input the desired x,y coordinate into the subroutine.
The angle that each wheel needs to face is calculated. The angle will be the same for all wheels
unless the robot is going to spin while moving. If the robot will be changing heading while moving,
the amount of turn correction will be factored in causing the wheels to face different directions and
have different relative speeds until the spin portion is achieved. We use a positioning loop to
assign the wheel speed. We are only using kP * error. We can change states by several different
criteria. We might use an achieved distance, an intake sensor, or a targeting feedback to tell the
robot that it is done with that task. The robot then moves on to the next task.

Calibration
-------------
If we used our nominal wheel diameters and gear ratios, these values should be pretty close to
real-world values, but they probably won't be perfect. We'll want to calibrate our overall speeds by
applying a multiplier. This calibration can be as simple as marking off a set distance (the longer the
better) and driving the robot across this distance, keeping it as straight as possible. Once the
distance is reached, the reported distance value can be compared with the actual distance value
and ratioed to produce a correction factor - actual distance over reported distance. This can also
be used to account for wheel wear, which changes the effective wheel diameter and can cause
inaccurate distance measurements when not accounted for.