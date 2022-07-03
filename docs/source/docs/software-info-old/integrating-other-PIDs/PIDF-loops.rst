PIDs (PIDFs) Loops: A Primer
===============================

Why Do We Even Need Fancy Control Loops?
------------------------------------------
Control. We are completely serious. Loops enable us to finely control practically any part of the
robot. Yes, you can just set power to a motor with a joystick. That is fine for some mechanisms. If
you haven't even tried doing this yet, STOP RIGHT NOW! Go and make your robot move! Start simple,
then build your way up to complex controls.

Other mechanisms are very difficult to manage. Anything from battery voltage, to wheel wear can
impact how effectively the mechanism is operated. No matter what, there will always be physical
variance affecting robots. Never ever assume you will be driving your robot under certain, specific
conditions. Nothing is ever perfect, even in auton!

We are able to compensate for these differences using control loops. Yes, we also use some
awesome sensors to help us. However, control loops are the heart of reliable systems. Using a well
implemented PID or PIDF system will produce smooth, repeatable movements.

It is important to also note that there are other types of control loops. Compared to the others, PID
and PIDF are arguably the simplest and universal. That is why we use them wherever we can.

What Do These Letters Even Mean!?
-----------------------------------
These values are technically called gains . They help scale the error (the difference between our
target state , “where we want to be”, and our current state , “where we are right now”) in different
ways. This ends up being the correction we apply to the motor(s). For a more detailed explanation,
please see this article . Below we will talk about each gain .

.. note:: These gains can be used together in different combinations.
.. note:: These sample calculations are not tuned PID loops. These are simply examples to show how the numbers work.

P - Proportion
+++++++++++++++++
We multiply the error by P .
.. code-block:: text

    error = targetState − currentState;
    correction = error * kP;

All we are doing is converting the error into a useful number (e.g. a motor controller input).

Here is a simple numerical example:
.. code-block:: text

    error = targetState − currentState;
        = 2000 − 1000;
    correction = error * kP;
                = 1000 * 0.0001;
                = 0.1;

.. note:: In this scenario, our correction is 10% motor output.

I - Integral
+++++++++++++++
We continuously accumulate the error when we are very close to our target (within an
IZone ). Then, we scale the integral by the responseTime . Finally, we multiply this number by
I and add it into the correction calculation.

.. code-block:: text

    if((abs(error) < IZone) integral += error;
    if(abs(integral) > ILimit) integral *= responseTime;
    correction = error * kP + integral * kI;

All we are doing is allowing a little more power to be applied at the end.

The integral cannot be stored as a local variable . It must be external to your PID function. We
need to have a record of all previous tiny error values, otherwise the integral will not be
large enough to do anything. Because of this, you have to reset the integral before using
your PID again .

Additionally, it is very important that you use an ILimit to restrict how strong the integral can
get . Without this, the integra l can cause overrun and/or oscillation .

We can creep right to our target at an adjustable rate using responseTime . Slower systems
have smaller values, while faster systems have large values.

Depending on your system, you might not need to incorporate the integral.

Here is a simple numerical example:

.. code-block:: text

    error = targetState − currentState;
           = 2000 -1991
    if((abs(error) < IZone) integral += error;
        if((abs(9 < 10) integral += 9;
    if(abs(integral) > ILimit) integral *= responseTime;
        if(abs(9) > 100) integral *= 0.02;
    correction = error * kP + integral * kI;
               = 9 * 0.0001 + 9 * 0.002;
               = 0.0009 + 0.018 ;
               = 0.0189 ;

.. note:: In this scenario, our correction is 1.89% motor output. Yes, this is a very small number. However, after a few more cycles the integral will make correction grow strong enough to creep the system right to the target state .

D - Derivative
++++++++++++++++++
We take the difference between our current error and our previous error divided by our
responseTime . Then, we add the derivative into the correction equation.

.. code-block:: text

    derivative = (error – prevError) / responseTime;
    correction = error * kP + derivative * kD;

Think of this like we're slowly using the brakes instead of stomping on them. The derivative
helps us smooth out our movements.

We can also think about this in graphical terms. We are finding the slope of the correction
line. The slope tells us what the correction should look like in the near future. This helps to
smooth out the correction . As a result, derivatives can eliminate both overrun and
oscillation .

Unfortunately, control loops using derivatives are highly susceptible to noise issues.
Sudden jumps in values will cause unexpected behaviors.

Depending on your system, you might not need to incorporate the derivative .

Here is a simple numerical example:

.. code-block:: text

    error = targetState − currentState;
          = 2000 − 1000;
    derivative = (error – prevError) / responseTime;
               = (1000 – 1010) / 0.02 = − 500;
    correction = error * kP + derivative * kD;
               = 1000 * 0.0001 +− 500 * 0.001;
               = 0.1 − 0.5;
               = − 0.4;
               
.. note:: In this scenario, our correction is 40% reverse motor output.

F - Feed Forward
+++++++++++++++++++++
We multiply the target by feed forward . Then, we add that into the existing correction
equation. All we are doing is providing the system an initial boost in power based on our
existing knowledge of the system.

.. code-block:: text

    correction = error * kP + feedForward * kF;

Here is another way of thinking about it. We are supplying a known starting value to get us
into our operating range. Think about a shooter wheel. If we want the wheel to run at a
constant velocity, we already know how fast we want it to go. The feed forward gives our
system a boost, so the rest of the PID doesn't need to work as hard.

Other Control Loop Terms
--------------------------
Open Loops
++++++++++++++
Dead reckoning : controlling the system based on time . There is no feedback from sensors ,
so the system is not able to correct for changing conditions. This method should be used as
a starting point for building closed loops .

Closed Loops
++++++++++++++++++
PID(F) loops. Based on feedback we get from sensors, our system is able to automatically
correct for changing conditions.

Internal Loops (our version)
+++++++++++++++++++++++++++++++
PID(F) loops that are built into the motor controller. The feedback sensor is directly
communicating with the motor controller. Use this whenever possible. They react quicker
than external loops because the motor controller has a faster running clock than the
RoboRIO (typically 1 ms vs. 50 ms).

External Loops (our version)
++++++++++++++++++++++++++++++++
PID(F) loops that run on the RoboRIO. The feedback sensor is directly communicating with
the RoboRIO. Use this when you have to. They react slower than internal loops because the
RoboRIO has a slower running clock than the motor controller (50 ms vs. typically 1 ms).
Also, you are responsible for writing the control loop yourself.

Positioning Loops
+++++++++++++++++++
PID(F) loops that have a target positio n in mind. Using an encoder (or other distance
measurement device), they allow you to achieve a certain distance in a timely, consistent
manner.

Velocity Loops
++++++++++++++++++
PID(F) loops that have a target velocity in mind. Using an encoder (or other velocity
measurement device), they allow you to achieve a certain speed in a timely, consistent
manner.

“Inside Outside” Loops (our definition)
+++++++++++++++++++++++++++++++++++++++++++
Using an external position loop to set an internal velocity loop . The encoder (or other
distance sensor) communicates with the RoboRIO, while another encoder (or other velocity
sensor) communicates with the motor controller. Use this for ultimate control IF you are
experienced. It can negate variations in battery levels.

General Tips for Tuning Control Loops
----------------------------------------
Good ole “trial and error”. The cool kids call it “The WAG Method”: Wild ______ Guess. (Use your
imagination.)

Tuning control loops can be a very time-intensive process. It is a necessary step though. You have
to customize the PID or PIDF to fit your robot. Each robot is different, so no two PIDs are alike. Even
practice and competition robots might need to have slightly different gains . This is primarily due to
weight differences between them.

See this article by CTRE for more information about tuning control loops.

Start with kP
+++++++++++++++++
.. note:: If the control loop for your system is going to maintain a certain setpoint , then it is a good idea to start with kF , and come back to this step.

Make a logical guess based on the units of measurement you are using and your output
units. Let's think about a simple positioning loop . Let's say our encoder reads 100 ticks/inch
and we are using percent output. Approximately how much power do we want applied to at
a certain distance? We already have an idea of how far we want to move: we know the field
measurements. So, let's say we want this positioning loop to give 100% output when we are
10 ft away. This is what the math would look like:

.. code-block:: text

    correction = error * kP;
    1 = 120000 * kP;
    kP = 1/12000 = 0.000833;

Using that kP , we can do some quick math to see how this behaves when we are 3 ft from
our target distance.

.. code-block:: text

    correction = error * kP;
    correction = 3600 * 0.0000833;
    correction = 0.299 = 30%;

Based on this, it seems we are within our operating range. Onward to tuning time!

It is recommended you double your kP value until you see oscillation , or what we call
“wagging” . If your robot starts shimmying and shaking, that means your gain is too high. Try
going 75% of the previous value. If that looks good, continue increasing the gain slightly
until you see more oscillation . Once you see more oscillation , lower the gain a tiny bit.

Now that we are content with our gain , we need to make sure it works throughout our
entire operating range.We have to test the control loop under different conditions. In our
earlier example, we would need to physically test our positioning loop at different
distances. We want the robot to always achieve its distance, no matter the distance (within
reason). To perform this test, we set up a range target distances, both traveling forwards
and backwards. DO NOT OVERLOOK THIS STEP! Please don't ever assume your loop will work
correctly in both directions.

If a system is traveling too quickly in certain scenarios, it may be a good idea to apply a
correction cap . This allows us to keep our tuned gain without sacrificing control due to
momentum.

We want to maximize the responsiveness of our system. When it is on the edge of
oscillation , the gain is just right. That is why we go through this process. Just calculating a
value alone is not enough. You have to test and tweak the gain to fit your system.

Next is kD
++++++++++++
Now that we are happy with our kP , we can start tuning kD .
.. note:: Depending on how your mechanism is designed and the type of control loop , you might not need to use kD . Brushless motors themselves behave much differently from brushed motors. We have found that control loops using brushless motors and kD are much harder to tune. They have a lot more torque, making the derivative difficult to control.

It is recommended that you start the kD at 10 times kP . In our previous example, that would mean:

.. code-block:: text

    kD = 10 * kP = 10 * 0.0000833 k = 0.000833;
    derivative = (error – prevError) / responseTime;
               = (3600 – 3620) / 0.02 = − 100;
    correction = error * kP + derivative * kD;
               = 3600 * 0.0000833 + − 100 * 0.000833;
               = 0.299 − 0.0833 = 0.217 = 22%;

Based on this, it seems we are within our operating range. Onward to tuning time!

It is recommended you double your kD value until you see you come short of your target . If
your mechanism overshoots (or travels past your target ), that means your gain is too low. If
it stops abruptly, that means your gain is too high. Try going 75% of the previous value. If
that looks good, continue increasing the gain slightly until you see it come short again.
Once you see more of this, lower the gain a tiny bit.

You may want to increase your kP slightly to maximize the speed of your system. Ideally,
you want to find the balance between speed and accuracy with any control loop .

.. note:: The derivative is not intended to get you exactly to your target ; that's what the integral is for. Instead, we use kD to help eliminate overshooting the target.

Now that we are content with our gain , we need to make sure it works throughout our
entire operating range.We have to test the control loop under different conditions. In our
earlier example, we would need to physically test our positioning loop at different
distances. We want the robot to always achieve its distance, no matter the distance (within
reason). To perform this test, we set up a range target distances, both traveling forwards
and backwards. DO NOT OVERLOOK THIS STEP! Please don't ever assume your loop will work
correctly in both directions.

We want to maximize the responsiveness of our system. When it is just shy of the target ,
the gain is just right. That is why we go through this process. Just calculating a value alone
is not enough. You have to test and tweak the gain to fit your system.

Then kI
++++++++++
Now that we are happy with our kD , we can start tuning kI .
.. note:: Depending on how your mechanism is designed and the type of control loop , you
might not need to use kI.

It is recommended that you start the kI with a fairly small value. We only want the integral
to be active when we are extremely close to our target. So, let's look at an example without
the integra l, then with it:

.. code-block:: text

    derivative = (error - prevError) / responseTime;
               = (9 – 10) / 0.02 = − 50;
    correction = error * kP + derivative * kD;
               = 9 * 0.000833 + − 50 * 0.000833;
               = 0.0075 − 0.0417 = − 0.0342 = − 3%;

.. code-block:: text

    derivative = (error – prevError) / responseTime;
               = (9 – 10) / 0.02 = − 50;
    if((abs(error) < IZone) integral += error;
        if((abs(9 < 10) integral += 9;
    if(abs(integral) > ILimit) integral *= responseTime;
        if(abs(9) > 100) integral *= 0.02;
    correction = error * kP + integral * kI + derivative * kD;
               = 9 * 0.000833 + 9 * 0.005 + − 50 * 0.000833;
               = 0.0075 + 0.045 − 0.0417 = 0.09415 = 9%;

See the difference? Without kI , we are stuck just short of our target . With kI , we will
accumulate enough correction to get right to our target .
Based on this, it seems we are within our operating range. Onward to tuning time!

It is recommended you double your kI value until you see oscillation , or what we call
“wagging” . If your robot starts shimmying and shaking, that means your gain is too high. Try
going 75% of the previous value. If that looks good, continue increasing the gain slightly
until you see more oscillation . Once you see more oscillation , lower the gain a tiny bit.

Don't forget that you can also play with IZone and ILimit . These values can help create a
strong, yet controlled correction right to the target .

Now that we are content with our gain , we need to make sure it works throughout our
entire operating range.We have to test the control loop under different conditions. In our
earlier example, we would need to physically test our positioning loop at different
distances. We want the robot to always achieve its distance, no matter the distance (within
reason). To perform this test, we set up a range target distances, both traveling forwards
and backwards. DO NOT OVERLOOK THIS STEP! Please don't ever assume your loop will work
correctly in both directions.

We want to maximize the responsiveness of our system. When it is on the edge of
oscillation , the gain is just right. That is why we go through this process. Just calculating a
value alone is not enough. You have to test and tweak the gain to fit your system.

What about kF?
+++++++++++++++
.. note:: To use feedforward effectively you have to have a good idea of how your system will behave ahead of time.

kF is the simplest gain to tune. You just need to find a value that gets you right into your
operating range. Feedforward doesn't perform any corrections , rather it moves your
starting point from 0 to “whatever you want”. This makes it much easier to tune the rest of
the PID . Having a tighter range to correct results in faster reactions and finer control.

Once your feedforward has your system off to a good start, then you can return to tuning
kP .
