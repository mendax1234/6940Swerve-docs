Maintaining Your Heading (aka Not Spinning… aka Driving “Straight”) While in Field Centric
=============================================================================================

Introduction
---------------

Driving “straight” isn't as easy as you thought, is it? When we say “straight”, we mean moving without
unintentionally turning. We've all been there: “why is the robot steering left/right even though I'm
telling it to drive straight!?!” This is something we struggled with for a while too. Unfortunately,
there will always be physical variances between individual wheels or two sides of a drivetrain. There
will always be a need for a drive “straight” PID .

When it comes to swerve, driving “straight” is more complicated. Instead of the robot driving
forward/backward at a specific heading/angle , we want the robot to move in any direction without
spinning. The robot should always stay facing the same way, unless we tell it to rotate. When it
rotates, that angle will be our new heading to maintain.

Now things get even more interesting. How do we do this when we have other PID loops (i.e. goal
centric , game piece centric ) occurring simultaneously? The robot should switch between goal centric,
game piece centric, and field centric seamlessly.

Not spinning isn't as easy as you thought, is it? Don't worry, we're going to help as much as we can.

How It's Done
---------------

You need to have a variable that stores your target heading . Typically, we refer to ours as storedYaw .
This variable must be updated every time you have a new angle you want to face.

In addition, you need to have a variable that stores your current heading . Typically, we refer to ours
as yaw . This variable must be updated every cycle with data from your gyro .

Then, you have a simple rotation PID which might look like this:

.. code-block:: text

    double calcY awStraight(double targetAngle, double curentAngle, double kP){
        double errorAngle = remainderf((targetAngle − currentAngle), 360);
        double correction = tx * kP;
        return correction;
    }

You would call this function in Teleop like so:

.. code-block:: text

    if(rot ! = 0){
        storedY aw = yaw;
    }else{
    if( abs(speed) > 0 || abs(strafe) > 0 ){
        yawCorrection = calcY awStraight(storedY aw, yaw, 0.004);
        }
    }
    move(fwd, rot + yawCorrection , str);

Essentially, we want to keep facing the same angle whenever we aren't rotating. When we don't
want to spin, we want to maintain our heading while we move. However, we don't want to PID our
angle if we aren't trying to move (due to safety concerns).

To integrate this with other driving PID loops , make sure that maintaining your heading is your
“default” scenario. Goal centric and game piece centric will modify your yawCorrection and
storedYaw (or equivalent variables) as needed.