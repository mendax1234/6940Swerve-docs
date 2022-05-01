The Maths
===========

Controls and Inputs
--------------------

The driver has some intended output that they’d like the robot to do. In order to communicate this,
we define three command inputs - Forward, Strafe, and Rotation, or :math:`FWD`, :math:`STR`, and ROT. Let’s
define these as variables, each going from -1 to 1, with 0 indicating no control input. There are many
ways to map driver inputs to these commands via joysticks, but we chose to use a method where
one stick controls translation rate (FWD and :math:`STR`) and the other’s left-right axis controls rotation
rate (ROT), as shown on the controller. These joysticks are implemented using standard libraries in
WPILib, and input is filtered and transformed to provide a better experience to the drivers.
In addition to the driver’s inputs, we can have inputs incorporated.

.. figure:: https://pic.imgdb.cn/item/626dfbe0239250f7c590c457.png
   :width: 100%
   :align: center

In addition to the driver’s inputs, we can have inputs incorporated.

Field Centric Transformation
-----------------------------

Once we know the intended movement that the robot should be making, we should apply our
field-centric math. This is what’s known as a transformation . In simple terms, we take what we
know about the robot’s orientation relative to the field - in this case, its angle (as measured by a
gyroscope) and our known desired forward/back and strafe commands, and adjust them so that the
robot moves relative to the field.

We define :math:`FWD` and :math:`STR` as the desired forward/back and strafe commands from the joystick,
relative to the field. These can both range from -1 to 1 from the joystick, assuming things are filtered
correctly, and the magnitude of the input vector (:math:`FWD`, :math:`STR`) shouldn’t ever be greater than 1. We’ll
find that this doesn’t matter later.

We’ll call the angle of the chassis relative to the field θ, and assume that it’s 0 when the front of
the robot is aligned with the field, away from the driver. This angle can be either defined from -180°
to 180°, or from 0 to 360 degrees - the math in this case works the same. With these in mind, we can
transform our :math:`FWD` and :math:`STR` commands as follows:

.. math:: FWDnew = FWD * cosθ + STR * sinθ
.. math:: STRnew = STR * cosθ − FWD * sinθ

First, we calculate our new :math:`FWD`, which can be thought of as simply figuring out how much of each
original command (:math:`FWD` and :math:`STR`) are in the actual direction of the robot’s “:math:`FWD`”. Likewise, we can
do the same for our :math:`STR` command. This effectively transforms our commands, considered relative
to the field , into commands that are relative to the robot , using information about the robot’s
orientation to the field to align everything. If you know a bit of linear algebra, you might recognize
this as the result of a rotation matrix , applied to the vector (:math:`FWD`, STR).

Our ROT (rotation) command actually doesn’t come into play at all in this transformation. To
understand why this is, consider that

To explain this further, let’s look at the results of the the following three situations:

**Example 1: Robot is aligned with field**

The key here is to think about what the value of θ is, and how the value of our sines and cosines
changes as a result. Here, since we’re aligned with the field, :math:`θ=0°`. Let’s check our sine and cosine
plots to see where that puts us at, in terms of values:

.. figure:: https://pic.imgdb.cn/item/626dfd69239250f7c5944f63.jpg
   :width: 100%
   :align: center

:math:`cos0°` is 1, and :math:`sin0°` is 0. If we think about a right triangle, with one of its angles being 0° and a
hypotenuse of 1, the opposing side of that triangle would have no height - and the adjacent side
would have the length of the hypotenuse, or 1. Let’s see what our math does with this.

Our math tells us that we haven’t changed anything by doing this! Physically, this makes sense; if
the robot is aligned with the field, what it considers to be forward is the same as the field’s forward;
we don’t need to modify our commands at all.

**Example 2: Robot is at 90 degrees to field**

Let’s say that we’re now at a right angle to the field; our robot is sideways, so our angle :math:`θ=90°`.
Again, let’s check our trigonometry. :math:`cos90°` = 0, and :math:`sin90°` = 1. What does our math do with
these?

.. math:: 
   FWD_{\new} = FWD * cos(90°) + STR * sin(90°) = FWD * 0 + STR * 1 = STR
   STR_{\new} = STR * cos(90°) − FWD * sin(90°) = STR * 0 − FWD * 1 = −FWD

Our commands have switched (with a small change of sign)! Again, physically, this makes some
sense. The robot is sideways; in order to go forward, it has to do what it considers a strafe, and in
order to strafe, it has to go what it considers forward.

**Example 3: Robot is at 30 degrees to field**

We’re now at some angle that doesn’t produce as nice a result. The robot is aligned differently from
the field, so to go straight forward or straight sideways, the robot is going to need to do some combination of what it considers going forward and going sideways. With our angle θ=30°,
:math:`cos30°` = 0.866, and :math:`sin30°` = 0.5. Following through the equations, then,

.. math:: 
   FWD_{\new} = FWD * cos(30°) + STR * sin(30°) = FWD * 0.866 + STR * 0.5
   STR_{\new} = STR * cos(30°) − FWD * sin(30°) = STR * 0.866 − FWD * 0.5

Both :math:`FWD` and :math:`STR` contribute to each of the transformed values. This pattern will carry through for
any non-right angle, and as long as we consider our angle properly (with clockwise as positive) we’re
good to go!

Inverse Kinematics (Wheel Speeds and Azimuths)
------------------------------------------------

Now that we have our :math:`FWD` and :math:`STR` commands transformed, we need to figure out what each wheel
should be doing to execute them. What we’re doing here is commonly referred to as inverse
kinematics , or IK. We have some goal output we want to get to, and we have some actuator
parameters (or joints) we can adjust, those being our wheel speeds and azimuth angles. Inverse
kinematics is the calculation of a unique set of output settings that will give us our overall output.
Forward kinematics (which we’ll cover elsewhere) is the opposite - determining the state (or pose)
we’re in based on what our actuators have been doing.

First, we should account for the wheel layout. We’re going to assume our wheel pods are on the
vertices of a rectangle. To put it another way, all four wheel axles are able to lie on some circle. This
represents the majority of swerve drive setups (ours was square). If the swerve modules are not on
a square (e.g. if the robot is not square), we’ll account for that as we make our calculations.

First, let’s define the length and width of our wheelbase
as L and W, and let’s define an additional value :math:`R`, as
:math:`R = (L^2 + W^2)^0.5` , or the diameter of the circle that contacts all
four wheel axles. The units of these values don’t matter, as we’re
only going to be taking their ratios in our wheel calculations.

.. figure:: https://pic.imgdb.cn/item/626dfe54239250f7c5964d5d.jpg
   :width: 50%
   :align: center