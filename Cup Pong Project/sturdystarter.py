import ev3dev.ev3 as ev3

class SturdyBot(object):
    """This provides a higher-level interface to the sturdy Lego robot we've been working
    with."""

    # ---------------------------------------------------------------------------
    # Constants for the configDict
    LEFT_MOTOR = 'left-motor'
    RIGHT_MOTOR = 'right-motor'
    SERVO_MOTOR = 'servo-motor'
    LEFT_TOUCH = 'left-touch'
    RIGHT_TOUCH = 'right-touch'
    ULTRA_SENSOR = 'ultra-sensor'
    COLOR_SENSOR = 'color-sensor'
    GYRO_SENSOR = 'gyro-sensor'

    # ---------------------------------------------------------------------------
    # Setup methods, including constructor

    def __init__(self, robotName, configDict=None):
        """Takes in a string, the name of the robot, and an optional dictionary
        giving motor and sensor ports for the robot."""
        self.name = robotName
        self.leftMotor = None
        self.rightMotor = None
        self.servoMotor = None
        self.leftTouch = None
        self.rightTouch = None
        self.ultraSensor = None
        self.colorSensor = None
        self.gyroSensor = None
        if configDict is not None:
            self.setupSensorsMotors(configDict)
        if self.leftMotor is None:
            self.leftMotor = ev3.LargeMotor('outC')
        if self.rightMotor is None:
            self.rightMotor = ev3.LargeMotor('outB')

    def forward(self,speed,time = None):
        self.leftMotor.speed_sp = self.leftMotor.max_speed*speed
        self.rightMotor.speed_sp = self.rightMotor.max_speed*speed
        self.leftMotor.run_timed(time_sp=time, speed_sp = self.leftMotor.speed_sp)
        self.rightMotor.run_timed(time_sp=time, speed_sp = self.rightMotor.speed_sp)
        self.leftMotor.wait_until_not_moving()

    def forward_forever(self, speed):
        self.leftMotor.speed_sp = self.leftMotor.max_speed*speed
        self.rightMotor.speed_sp = self.rightMotor.max_speed*speed
        self.leftMotor.run_forever()
        self.rightMotor.run_forever()

    def backward(self, speed,time = None):
        self.leftMotor.speed_sp = -(self.leftMotor.max_speed*speed)
        self.rightMotor.speed_sp = -(self.rightMotor.max_speed*speed)
        self.leftMotor.run_timed(time_sp=time, speed_sp = self.leftMotor.speed_sp)
        self.rightMotor.run_timed(time_sp=time, speed_sp = self.rightMotor.speed_sp)
        self.leftMotor.wait_until_not_moving()
    
    def turnLeft(self, speed, time= None):
        self.leftMotor.speed_sp = -self.leftMotor.max_speed*speed
        self.rightMotor.speed_sp = self.rightMotor.max_speed*speed
        self.leftMotor.run_timed(time_sp=time, speed_sp = self.leftMotor.speed_sp)
        self.rightMotor.run_timed(time_sp=time, speed_sp = self.rightMotor.speed_sp)
        self.leftMotor.wait_until_not_moving()

    def turnRight(self, speed, time= None):
        self.leftMotor.speed_sp = self.leftMotor.max_speed*speed
        self.rightMotor.speed_sp = -self.rightMotor.max_speed*speed
        self.leftMotor.run_timed(time_sp=time, speed_sp = self.leftMotor.speed_sp)
        self.rightMotor.run_timed(time_sp=time, speed_sp = self.rightMotor.speed_sp)
        self.leftMotor.wait_until_not_moving()

    def stop(self):
        self.leftMotor.stop(stop_action = 'hold')
        self.rightMotor.stop(stop_action = 'hold')

    def curve(self,leftSpeed,rightSpeed, time=None):
        self.leftMotor.speed_sp = self.leftMotor.max_speed*leftSpeed
        self.rightMotor.speed_sp = self.rightMotor.max_speed*rightSpeed
        self.leftMotor.run_timed(time_sp=time, speed_sp = self.leftMotor.speed_sp)
        self.rightMotor.run_timed(time_sp=time, speed_sp = self.rightMotor.speed_sp)
        self.leftMotor.wait_until_not_moving()

    def zeroPointer(self):
        self.servoMotor.position_sp = 0
        self.servoMotor.run_to_abs_pos(position_sp = self.servoMotor.position_sp)
        self.servoMotor.stop_action = 'brake'
        self.servoMotor.wait_until_not_moving()

    def leftPointer(self,speed = .25,time = None):
        self.servoMotor.speed_sp = -(speed*self.servoMotor.max_speed)
        self.servoMotor.run_timed(time_sp = time,speed_sp = self.servoMotor.speed_sp)
        self.servoMotor.stop_action = 'brake'
        self.servoMotor.wait_until_not_moving()

    def rightPointer(self,speed = .25, time = None):
        self.servoMotor.speed_sp = speed*self.servoMotor.max_speed
        self.servoMotor.run_timed(time_sp = time,speed_sp = self.servoMotor.speed_sp)
        self.servoMotor.stop_action = 'brake'
        self.servoMotor.wait_until_not_moving()

    def pointerTo(self,angle):
        self.servoMotor.position_sp = angle
        self.servoMotor.run_to_abs_pos(position_sp = self.servoMotor.position_sp)
        self.servoMotor.wait_until_not_moving()

    def speak(self, words):
        ev3.Sound.speak(words)

    def beep(self):
        ev3.Sound.beep()

    def move(self, translateSpeed, rotateSpeed, runTime=None):
        #print(rotateSpeed)
        wheelDist = 12 * 19.5
        assert self.leftMotor is not None
        assert self.rightMotor is not None
        assert -1.0 <= translateSpeed <= 1.0
        assert -1.0 <= rotateSpeed <= 1.0
        transMotorSp = translateSpeed * self.leftMotor.max_speed
        rotMotorSp = rotateSpeed * 2 
        leftSpeed = transMotorSp - (rotMotorSp * wheelDist) / 2.0
        rightSpeed = transMotorSp + (rotMotorSp * wheelDist) / 2.0
        print("SPEEDS:", leftSpeed, rightSpeed)
        self.leftMotor.speed_sp = leftSpeed
        self.rightMotor.speed_sp = rightSpeed
        self._moveRobot(runTime)

    def _moveRobot(self, runTime):
        if runTime is None:
            self.leftMotor.run_forever()
            self.rightMotor.run_forever()
        else:
            milliSecTime = runTime * 1000.0
            self.leftMotor.run_timed(time_sp = milliSecTime)
            self.rightMotor.run_timed(time_sp = milliSecTime)
            self.rightMotor.wait_until_not_moving()

    def setupSensorsMotors(self, configs):
        """Takes in a dictionary where the key is a string that identifies a motor or sensor
        and the value is the port for that motor or sensor. It sets up all the specified motors
        and sensors accordingly."""
        for item in configs:
            port = configs[item]
            if item == self.LEFT_MOTOR:
                self.leftMotor = ev3.LargeMotor(port)
            elif item == self.RIGHT_MOTOR:
                self.rightMotor = ev3.LargeMotor(port)
            elif item == self.SERVO_MOTOR:
                self.servoMotor = ev3.MediumMotor(port)
            elif item == self.LEFT_TOUCH:
                self.leftTouch = ev3.TouchSensor(port)
            elif item == self.RIGHT_TOUCH:
                self.rightTouch = ev3.TouchSensor(port)
            elif item == self.ULTRA_SENSOR:
                self.ultraSensor = ev3.UltrasonicSensor(port)
            elif item == self.COLOR_SENSOR:
                self.colorSensor = ev3.ColorSensor(port)
            elif item == self.GYRO_SENSOR:
                self.gyroSensor = ev3.GyroSensor(port)
            else:
                print("Unknown configuration item:", item)

    def setMotorPort(self, side, port):
        """Takes in which side and which port, and changes the correct variable
        to connect to that port."""
        if side == self.LEFT_MOTOR:
            self.leftMotor = ev3.LargeMotor(port)
        elif side == self.RIGHT_MOTOR:
            self.rightMotor = ev3.LargeMotor(port)
        elif side == self.SERVO_MOTOR:
            self.servoMotor = ev3.MediumMotor(port)
        else:
            print("Incorrect motor description:", side)

    def setTouchSensor(self, side, port):
        """Takes in which side and which port, and changes the correct
        variable to connect to that port"""
        if side == self.LEFT_TOUCH:
            self.leftTouch = ev3.TouchSensor(port)
        elif side == self.RIGHT_TOUCH:
            self.rightTouch = ev3.TouchSensor(port)
        else:
            print("Incorrect touch sensor description:", side)

    def setColorSensor(self, port):
        """Takes in the port for the color sensor and updates object"""
        self.colorSensor = ev3.ColorSensor(port)

    def setUltrasonicSensor(self, port):
        """Takes in the port for the ultrasonic sensor and updates object"""
        self.ultraSensor = ev3.UltrasonicSensor(port)

    def setGyroSensor(self, port):
        """Takes in the port for the gyro sensor and updates object"""
        self.gyroSensor = ev3.GyroSensor(port)

    # ---------------------------------------------------------------------------
    # Methods to read sensor values

    def readTouch(self):
        """Reports the value of both touch sensors, OR just one if only one is connected, OR
        prints an alert and returns nothing if neither is connected."""
        if self.leftTouch is not None and self.rightTouch is not None:
            return self.leftTouch.is_pressed, self.rightTouch.is_pressed
        elif self.leftTouch is not None:
            return self.leftTouch.is_pressed, None
        elif self.rightTouch is not None:
            return None, self.rightTouch
        else:
            print("Warning, no touch sensor connected")
            return None, None

    def readReflect(self):
        return self.colorSensor.reflected_light_intensity

    def readAmbient(self):
        return self.colorSensor.ambient_light_intensity

    def readColor(self):
        return self.colorSensor.color

    def readDistance(self):
        return self.ultraSensor.distance_centimeters

    def readHeading(self):
        rate_angle = self.gyroSensor.rate_and_angle
        return (rate_angle[1] % 360,rate_angle[0])
    # Add the rest here


    # ---------------------------------------------------------------------------
    # Methods to move robot

    # Put your code here, make changes to make it consistent




# Sample of how to use this

    #if touchValues == (False, False):
    #    touchyRobot.forward(0.6, 1500)
   # elif touchValues[1]:
   #     touchyRobot.turnLeft(0.4, 1500)
   # elif touchValues[0]:
    #    touchyRobot.turnRight(0.4, 1500)
   ## else:
     #   touchyRobot.backward(0.6, 1500)