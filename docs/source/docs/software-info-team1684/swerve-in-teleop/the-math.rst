The Maths
===========

Controls and Inputs
--------------------

The driver has some intended output that they'd like the robot to do. In order to communicate this,
we define three command inputs - Forward, Strafe, and Rotation, or :math:`FWD`, :math:`STR`, and ROT. Let's
define these as variables, each going from -1 to 1, with 0 indicating no control input. There are many
ways to map driver inputs to these commands via joysticks, but we chose to use a method where
one stick controls translation rate (FWD and :math:`STR`) and the other's left-right axis controls rotation
rate (ROT), as shown on the controller. These joysticks are implemented using standard libraries in
WPILib, and input is filtered and transformed to provide a better experience to the drivers.
In addition to the driver's inputs, we can have inputs incorporated.

.. figure:: https://pic.imgdb.cn/item/626dfbe0239250f7c590c457.png
   :width: 100%
   :align: center

In addition to the driver's inputs, we can have inputs incorporated.

Field Centric Transformation
-----------------------------

Once we know the intended movement that the robot should be making, we should apply our
field-centric math. This is what's known as a transformation . In simple terms, we take what we
know about the robot's orientation relative to the field - in this case, its angle (as measured by a
gyroscope) and our known desired forward/back and strafe commands, and adjust them so that the
robot moves relative to the field.

We define :math:`FWD` and :math:`STR` as the desired forward/back and strafe commands from the joystick,
relative to the field. These can both range from -1 to 1 from the joystick, assuming things are filtered
correctly, and the magnitude of the input vector (:math:`FWD`, :math:`STR`) shouldn't ever be greater than 1. We'll
find that this doesn't matter later.

We'll call the angle of the chassis relative to the field θ, and assume that it's 0 when the front of
the robot is aligned with the field, away from the driver. This angle can be either defined from -180°
to 180°, or from 0 to 360 degrees - the math in this case works the same. With these in mind, we can
transform our :math:`FWD` and :math:`STR` commands as follows:

.. math:: FWDnew = FWD * cosθ + STR * sinθ
.. math:: STRnew = STR * cosθ − FWD * sinθ

First, we calculate our new :math:`FWD`, which can be thought of as simply figuring out how much of each
original command (:math:`FWD` and :math:`STR`) are in the actual direction of the robot's “:math:`FWD`”. Likewise, we can
do the same for our :math:`STR` command. This effectively transforms our commands, considered relative
to the field , into commands that are relative to the robot , using information about the robot's
orientation to the field to align everything. If you know a bit of linear algebra, you might recognize
this as the result of a `rotation matrix <https://en.wikipedia.org/wiki/Rotation_matrix>`_` , applied to the vector (:math:`FWD`, STR).

Our ROT (rotation) command actually doesn't come into play at all in this transformation. To
understand why this is, consider that

To explain this further, let's look at the results of the the following three situations:

**Example 1: Robot is aligned with field**

The key here is to think about what the value of θ is, and how the value of our sines and cosines
changes as a result. Here, since we're aligned with the field, :math:`θ=0°`. Let's check our sine and cosine
plots to see where that puts us at, in terms of values:

.. figure:: https://pic.imgdb.cn/item/626dfd69239250f7c5944f63.jpg
   :width: 100%
   :align: center

:math:`cos0°` is 1, and :math:`sin0°` is 0. If we think about a right triangle, with one of its angles being 0° and a
hypotenuse of 1, the opposing side of that triangle would have no height - and the adjacent side
would have the length of the hypotenuse, or 1. Let's see what our math does with this.

.. math:: FWD_{new} = FWD * cos(0°) + STR * sin(0°) = FWD * 1 + STR * 0 = FWD
.. math:: STR_{new} = STR * cos(0°) − FWD * sin(0°) = STR * 1 − FWD * 0 = STR

Our math tells us that we haven't changed anything by doing this! Physically, this makes sense; if
the robot is aligned with the field, what it considers to be forward is the same as the field's forward;
we don't need to modify our commands at all.

**Example 2: Robot is at 90 degrees to field**

Let's say that we're now at a right angle to the field; our robot is sideways, so our angle :math:`θ=90°`.
Again, let's check our trigonometry. :math:`cos90°` = 0, and :math:`sin90°` = 1. What does our math do with
these?

.. math:: FWD_{new} = FWD * cos(90°) + STR * sin(90°) = FWD * 0 + STR * 1 = STR
.. math:: STR_{new} = STR * cos(90°) − FWD * sin(90°) = STR * 0 − FWD * 1 = −FWD

Our commands have switched (with a small change of sign)! Again, physically, this makes some
sense. The robot is sideways; in order to go forward, it has to do what it considers a strafe, and in
order to strafe, it has to go what it considers forward.

**Example 3: Robot is at 30 degrees to field**

We're now at some angle that doesn't produce as nice a result. The robot is aligned differently from
the field, so to go straight forward or straight sideways, the robot is going to need to do some combination of what it considers going forward and going sideways. With our angle θ=30°,
:math:`cos30°` = 0.866, and :math:`sin30°` = 0.5. Following through the equations, then, 

.. math:: FWD_{new} = FWD * cos(30°) + STR * sin(30°) = FWD * 0.866 + STR * 0.5
.. math:: STR_{new} = STR * cos(30°) − FWD * sin(30°) = STR * 0.866 − FWD * 0.5

Both :math:`FWD` and :math:`STR` contribute to each of the transformed values. This pattern will carry through for
any non-right angle, and as long as we consider our angle properly (with clockwise as positive) we're
good to go!

Inverse Kinematics (Wheel Speeds and Azimuths)
------------------------------------------------

Now that we have our :math:`FWD` and :math:`STR` commands transformed, we need to figure out what each wheel
should be doing to execute them. What we're doing here is commonly referred to as `inverse
kinematics <https://en.wikipedia.org/wiki/Inverse_kinematics>`_ , or IK. We have some goal output we want to get to, and we have some actuator
parameters (or joints) we can adjust, those being our wheel speeds and azimuth angles. Inverse
kinematics is the calculation of a unique set of output settings that will give us our overall output.
Forward kinematics (which we'll cover elsewhere) is the opposite - determining the state (or pose)
we're in based on what our actuators have been doing.

First, we should account for the wheel layout. We're going to assume our wheel pods are on the
vertices of a rectangle. To put it another way, all four wheel axles are able to lie on some circle. This
represents the majority of swerve drive setups (ours was square). If the swerve modules are not on
a square (e.g. if the robot is not square), we'll account for that as we make our calculations.

First, let's define the length and width of our wheelbase
as L and W, and let's define an additional value :math:`R`, as
:math:`R = \sqrt{L^2 + W^2}` , or the diameter of the circle that contacts all
four wheel axles. The units of these values don't matter, as we're
only going to be taking their ratios in our wheel calculations.

.. figure:: https://pic.imgdb.cn/item/626dfe54239250f7c5964d5d.jpg
   :width: 50%
   :align: center

Intuition
+++++++++++++
To understand how we can turn our overall commands (what we
want the robot as a whole to do) into what each wheel needs to do,
we should build some intuition. It's perfectly possible to borrow the math and program it into place
without this, but it really helps to understand how things work under the hood.

As we derive our inverse kinematics, we make some underlying assumptions, including that the
robot's chassis acts as a rigid body - within its own reference frame, one point cannot move closer
or further away to another point. Imagine a metal cube on a desk. You can move it forward, back,
and spin it, but it's solid and unchanging relative to itself. From a kinematics standpoint, there's an
important fact we can draw from this. If we look at one side of the robot, all points along it have to 
have the same velocity forward or backward. If they had different speeds, the side would be
changing in length. Hopefully that's not actually happening, and if our robot is built sufficiently
rigidly, it shouldn't be.

.. figure:: https://pic.imgdb.cn/item/626f5b68239250f7c56f4711.jpg
   :width: 100%
   :align: center

We can back this assumption out by doing some vector math . ChiefDelphi user Ether's `Derivation of
Inverse Kinematics for Swerve <https://www.chiefdelphi.com/t/paper-4-wheel-independent-drive-independent-steering-swerve/107383>`_ 
document explains this in detail. To do this, we can combine our
desired strafe and speed commands into a translation vector , and our rotation command can be
combined with our robot geometry to form a rotational component. By adding these vectors, we get
our required wheel movement vector, in the form of a direction and a magnitude.

From here, we'll define some variables to save us some work. Standard convention has them as A, B,
C, and D.

.. math:: A = STR - ROT * L/R
.. math:: B = STR + ROT * L/R
.. math:: C = FWD - ROT * W/R
.. math:: D = FWD - ROT * W/R

We'll use these to calculate our resultant wheel speeds and wheel angles (or azimuth angles), or ws
and wa respectively.

.. math:: ws_{FR} = \sqrt{B^2 + C^2}    
.. math:: wa_{FR} = atan2(B,C)
.. math:: ws_{FL} = \sqrt{B^2 + D^2}    
.. math:: wa_{FL} = atan2(B,D)
.. math:: ws_{RR} = \sqrt{A^2 + C^2}    
.. math:: wa_{RR} = atan2(A,C)
.. math:: ws_{RL} = \sqrt{A^2 + D^2}    
.. math:: wa_{RL} = atan2(A,D)

.. note:: The atan2 function is defined in many programming languages, and provides quadrant-aware calculations for the arctangent function, meaning the angle output will range from -π to π, instead of 0 to π/2.

What we see here is that we have common factors between our wheels. For both front wheels, we
have a common horizontal factor B, and for both rear wheels, a different common factor A. For both
right wheels, and left, we see the same thing, with common forward/backward components C and
D. This is the mathematical realization of the fact that our robot's chassis can't change in size or
shape. Bonus: if you know a bit of vector math, you'll notice that we're doing a transformation from
cartesian to polar coordinates.

Where FR, FL, RR, and RL refer to front right, front left, rear right, and rear left wheels. Our azimuth
angles should range from -π to π, with positive as clockwise and zero being straight π π ahead. These
can be converted to degrees as necessary - just multiply by 180/π . Our wheel speeds should range
from 0 to 1, absolute, but we'll need to check if they need to be normalized. To do this, we just check
if the maximum of our ws values is greater than 1, and if it is, scale the values such that it's 1.

::

   ws_{max} = max(ws_{FR}, ws_{FL}, ws_{RR}, ws_{RL})
   if ws_{max} > 1.0 :
   ws_{FR} = ws_{FR}/ws_{max}
   ws_{FL} = ws_{FL}/ws_{max}
   ws_{RR} = ws_{RR}/ws_{max}
   ws_{RL} = ws_{RL}/ws_{max}

Now we have all ws values ranging from 0 to 1. The wheel speed assumed to be in the direction the
wheel is facing ( wa ), and thus does not go negative, as that would imply the wheel has turned 180°.

Our algorithm to this point brings up a problem. If our control input quickly changes from, for
example, moving entirely forward to moving backward, our wheel pods need to turn all the way
around in order to execute the new command. Given that we're working with motors that can go full
power forward or backward, that's an inefficient thing to do. Ideally, we'd just flip the motor into
reverse and move on.

In order to solve this problem, we implement what we call inversion awareness . If we assume we
know the wheel's current azimuth angle, and we've calculated the azimuth we need, we can check if
we'd need to “flip” our module or not. If we would, we can just invert the speed output, readjust
where our azimuth is headed, and continue on our way. We'll implement this in a bit.

Power to the ground (Speed and Azimuth drivers)
-------------------------------------------------
Finally, we're at the point where we can get things moving. We have the parameters we want, a set
of wheel speeds and angles, generated from our desired output, transformed to be oriented relative
to the field. Now we want to get our swerve modules to execute those commands. These next bits
of code can be considered analogous to drivers in a computer system - layers of code that handle
the nitty-gritty low-level communication and control while providing an abstracted interface for
control. In our case, we grouped azimuth and wheel speed into one module that we can use to set a
wheel's target state.

Azimuth
+++++++++
Azimuth control is accomplished using a proportional feedback controller sensing the angle of the
wheel with an absolute encoder. Depending on the specific encoder used, this may come in the
form of a degree value, a voltage, or an integer number of ticks. For our US Digital MA3 encoders,
the output is in the form of a 0-5V signal, with the full range representing 360° of rotation. In many
cases, the encoder housing cannot repeatably and precisely be oriented to the “correct” physical
position. This means that the reading of our encoder when our azimuth is straight forward (0°, the
wheel is straight) can be any value. As such, we're going to have some offset value on a per-module
basis, and we'll factor it into our calculations.

For our feedback controller, we need to calculate the error between our setpoint and position.
Because we're working with angles and have a range of 0-360°, we need to use the remainder
function to make sure our error is calculated properly. We'll also use this for incorporating our
offset. Assuming we have the angle we want for this wheel (wa), we can calculate our error:

.. code-block:: text

   encoder = Encoder.GetValue()
   azimuthAngle = remainder(Encoder.GetValue() − wheelAngleOffset)
   azimuthError = remainder(azimuthAngle − wa)

Inversion Awareness
_____________________
Using the Talon FX's SetInverted method makes implementing inversion control very
straightforward. We simply “flip” our azimuth error to the other side.

.. code-block:: text

    azimuthError = azimuthPosition − wa ;
    if abs(azimuthError) > 90 : //assuming our angles are in degrees
      azimuthError = azimuthError − 180 * sgn(azimuthError)
      SpeedMotorController.SetInverted(true)
    else :
      SpeedMotorController.SetInverted(false)
