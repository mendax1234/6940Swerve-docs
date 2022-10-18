Game Piece Centric (Starring the Pixy)
========================================

Introduction
----------------

In game piece centric, the rotate input from the joystick is overridden by the Pixy. The driver is free
to move the robot in any direction while the Pixy keeps the robot pointed at a ball. This makes
picking up balls on the far side of the field a little easier. Since we have a Pixy on the front intake
and the rear intake, the driver has to select which one to use for this mode.

Here is a `video <https://youtu.be/VP4emc-K57k?t=42>`_ of our 2020 robot demonstrating game piece centric control.

How It's Done
----------------

There are two signals that we receive from the Pixy. There is a digital signal that tells us if a target
is within range. In this case a target is a yellow ball (Power Cell). There is an analog signal that gives
us the location of the ball on one axis of the camera's view. In this case the x or left to right axis.

The Pixy's analog signal is from 0 to 3.3 volts with 0 being the leftmost view of the camera. We
determined the center of the camera's view to be what we wanted to lock in on. We created a
positioning loop that took over the rotational control and calculated the error between the target
and the center of the camera. The error was used to calculate our desired yaw until the digital
signal showed no more target.

.. code-block:: text

    double pixyVoltageRange = 3.3; //volts
        double pixyHFOV = 60; //degrees
        bool pixyFrontSeesBall(){
        return pixyFrontDigitalInput.Get();
    }
    double pixyFrontAngle(){
        return (((pixyFrontAnalogInput.GetAverageVoltage())/pixyVoltageRange) − 0.5) * pixyHFOV;
    }
    double pixyFrontCorrection (){
        double pixyXkP = 0.004;
        return pixyFrontAngle() * pixyXkP;
    }

    //In teleop
    if(pixyFrontSeesBall()) {
        yawCorrection = pixyFrontCorrection();
        rot = 0;
    }else{
        storedYaw = yaw;
    }

    move(fwd, rot + yawCorrection , str);

We use the Pixy in a different manner in auton. We use it to determine our position relative to the
target ball to allow for automatic adjustment in the case of minor set up variances.

.. code-block:: text

    if(pixyFrontSeesBall() && (abs(pixyFrontAngle() + goalY aw) > 3.0)) {
        move(0, yc, − copysignf(0.1, pixyFrontAngle()), true);
    }else{
        move(0, 0, 0, true);
    }

In this case, we'll use the Pixy to center ourselves on the game piece if we're more than 3 degrees
off from it in either direction.