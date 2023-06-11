Swerve Control in Teleoperated Period
######################################

Preparations
**************
 我们需要创建两个subsystem，一个用来存放SwerveModule的相关信息和控制Swerve模块的具体方法（此处命名为SwerveModule），另一个用来具体实现Swerve开车函数（此处命名为SwerveDriveTrain）。
   
.. note:: 当然你也可以把这些都存在一个subsystem里，只不过存在两个subsystem里更加清晰，能够体现出你具备良好的编程素养。

SwerveModule
==============

.. tabs:: 

    .. code-tab:: java

        public SwerveModule(int driveDeviceNumber, int pivotDeviceNumber,
                        boolean driveMotorInvert, boolean pivotMotorInvert,
                        int pivotEncoderOffset, boolean pivotEncoderPhase,
                        boolean pivotEncoderInvert) {
            drive_motor_ = new WPI_TalonFX(driveDeviceNumber);
            pivot_motor_ = new WPI_TalonSRX(pivotDeviceNumber); 

            //These two may let the swerve rotate itself many times when startup
            //drive_motor_.configFactoryDefault();
            //pivot_motor_.configFactoryDefault();
            
            drive_motor_.setNeutralMode(NeutralMode.Brake);
            pivot_motor_.setNeutralMode(NeutralMode.Coast);
            drive_motor_.configPeakOutputForward( SwerveConstants.kDriveMotorMaxOutput);
            drive_motor_.configPeakOutputReverse(-SwerveConstants.kDriveMotorMaxOutput);
            pivot_motor_.configPeakOutputForward( SwerveConstants.kPivotMotorMaxOutput);
            pivot_motor_.configPeakOutputReverse(-SwerveConstants.kPivotMotorMaxOutput);

            drive_motor_.configSelectedFeedbackSensor(FeedbackDevice.IntegratedSensor);
            pivot_motor_.configSelectedFeedbackSensor(FeedbackDevice.CTRE_MagEncoder_Absolute);

            drive_motor_.config_kP(0, SwerveConstants.kDriveMotorkP);
            drive_motor_.config_kI(0, SwerveConstants.kDriveMotorkI);
            drive_motor_.config_kD(0, SwerveConstants.kDriveMotorkD);
            drive_motor_.config_kF(0, SwerveConstants.kDriveMotorkF);
            drive_motor_.config_IntegralZone(0, SwerveConstants.kDriveMotorIZone);
        
            pivot_motor_.config_kP(0, SwerveConstants.kPivotMotorkP);
            pivot_motor_.config_kI(0, SwerveConstants.kPivotMotorkI);
            pivot_motor_.config_kD(0, SwerveConstants.kPivotMotorkD);
            pivot_motor_.config_kF(0, SwerveConstants.kPivotMotorF);
            pivot_motor_.config_IntegralZone(0, SwerveConstants.kPivotMotorkIZone);
            pivot_motor_.configMotionCruiseVelocity(SwerveConstants.motionCruiseVelocity);
            pivot_motor_.configMotionAcceleration(SwerveConstants.motionAcceleration);

            drive_motor_.configOpenloopRamp(SwerveConstants.kLoopSeconds);
            drive_motor_.configClosedloopRamp(SwerveConstants.kLoopSeconds);

            pivot_motor_.configOpenloopRamp(SwerveConstants.kLoopSeconds);
            pivot_motor_.configClosedloopRamp(SwerveConstants.kLoopSeconds);

            pivot_encoder_inverted = pivotEncoderInvert ? -1.0 : 1.0;

            drive_motor_.configVoltageCompSaturation(12);
            drive_motor_.enableVoltageCompensation(true);

            pivot_motor_.configVoltageCompSaturation(12);
            pivot_motor_.enableVoltageCompensation(true);

            drive_motor_.configVelocityMeasurementPeriod(SensorVelocityMeasPeriod.Period_25Ms);
            drive_motor_.configVelocityMeasurementWindow(1);

    .. code-tab:: c++

        Wait for you to write!


SwerveDriveTrain
=================

