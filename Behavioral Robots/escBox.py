
import ev3dev.ev3 as ev3
import time


class SturdyBot(object):
    """This provides a higher-level interface to the sturdy Lego robot we've been working
    with."""
    default = 0.2
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
        self.bttn = ev3.Button()
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

    # Add the rest here
    def readReflect(self):
        if self.colorSensor is not None:
            return self.colorSensor.ambient_light_intensity
        else:
            print("Warning, no color sensor connected")
            return None
    
    def readColor(self):
        if self.colorSensor is not None:
            return self.colorSensor.color
        else:
            print("Warning, no color sensor connected")
            return None

    def readDistance(self):
        if self.ultraSensor is not None:
            return self.ultraSensor.distance_centimeters
        else:
            print("Warning, no UltraSonic sensor connected")
            return None

    def readHeading(self):
        if self.gyroSensor is not None:
            return (self.gyroSensor.angle % 360)
        else:
            print("Warning, no gyroSensor sensor connected")
            return None
    

    # ---------------------------------------------------------------------------
    # Methods to move robot

    # Put your code here, make changes to make it consistent
    def forward(self, speed, time=None):
        mapSpeed = speed*900
        if time is not None:
            self.leftMotor.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.rightMotor.run_timed(time_sp=time, speed_sp=mapSpeed)
            self.leftMotor.wait_until_not_moving()
        else:
            self.leftMotor.wait_until_not_moving()
            self.rightMotor.run_forever(speed_sp = mapSpeed)
        return

    def backward(self,speed, time= None):
        mapSpeed = speed * -900
        if time is not None:
            self.leftMotor.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.rightMotor.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.leftMotor.run_timed(time_sp = time, speed_sp = mapSpeed)
        else:
            self.leftMotor.run_forever(speed_sp = mapSpeed)
            self.rightMotor.run_forever(speed_sp = mapSpeed)
        return

    def turnLeft(self, speed, time=None):
        mapSpeed = speed * 900
        if time is not None:
            self.leftMotor.run_timed(time_sp=time, speed_sp = (-1*mapSpeed))
            self.rightMotor.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.leftMotor.wait_until_not_moving()
        else:
            self.leftMotor.run_forever(speed_sp = (-1*mapSpeed))
            self.rightMotor.run_forever(speed_sp = mapSpeed)
        return

    def turnRight(self, speed, time=None):
        mapSpeed = speed * 900
        if time is not None:
            self.leftMotor.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.rightMotor.run_timed(time_sp=time, speed_sp = (-1*mapSpeed))
            self.leftMotor.wait_until_not_moving()
        else:
            self.leftMotor.run_forever(speed_sp = mapSpeed)
            self.rightMotor.run_forever(speed_sp = (-1*mapSpeed))
        return

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()
        return

    def curve(self, leftSpeed, rightSpeed, time=None):
        mapLeftSpeed = leftSpeed * 900
        mapRightSpeed = rightSpeed * 900
        if time is not None:
            self.leftMotor.run_timed(time_sp=time, speed_sp = mapLeftSpeed)
            self.rightMotor.run_timed(time_sp=time, speed_sp = mapRightSpeed)
            self.leftMotor.wait_until_not_moving()
        else:
            self.leftMotor.run_forever(speed_sp = mapLeftSpeed)
            self.rightMotor.run_forever(speed_sp = mapRightSpeed)

        return

    def zeroPointer(self):
        self.servoMotor.run_to_abs_pos(position_sp = 0, stop_action = "hold")
        self.servoMotor.wait_until_not_moving()
        return

    def pointerLeft(self, speed=default, time=None):
        mapSpeed = speed * -1000
        if time is not None:
            self.servoMotor.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.servoMotor.wait_until_not_moving()
        else:
            self.servoMotor.run_forever(speed_sp = mapSpeed)
        return
    
    def pointerRight(self, speed=default, time=None):
        mapSpeed = speed * 1000
        if time is not None:
            self.servoMotor.run_timed(time_sp=time, speed_sp = mapSpeed)
            self.servoMotor.wait_until_not_moving()
        else:
            self.servoMotor.run_forever(speed_sp = mapSpeed)
        return

    def pointerTo(self, angle):
        self.servoMotor.run_to_abs_pos(position_sp = angle, stop_action = "hold")
        self.servoMotor.wait_until_not_moving()
        return



# Sample of how to use this
if __name__ == "__main__":
    print("in main")
    firstConfig = {SturdyBot.LEFT_MOTOR: 'outC',
                   SturdyBot.RIGHT_MOTOR: 'outB',
                   SturdyBot.SERVO_MOTOR: 'outD',
                   SturdyBot.LEFT_TOUCH: 'in4',
                   SturdyBot.RIGHT_TOUCH: 'in1',
                   SturdyBot.ULTRA_SENSOR: 'in3',
                   SturdyBot.COLOR_SENSOR: 'in2',
 #                  SturdyBot.GYRO_SENSOR: 'in2'#
                   }
    touchyRobot = SturdyBot('Touchy', firstConfig)
    touchyRobot.zeroPointer()
    while True:
 
        touchyRobot.pointerLeft(.25,500)
        lightLeft = touchyRobot.readReflect()
        print("left: ",lightLeft)
        time.sleep(.5)
        touchyRobot.zeroPointer()
        touchyRobot.pointerRight(.25,500)
        lightRight = touchyRobot.readReflect()
        print("right: ",lightRight)
        time.sleep(.5)
        touchyRobot.zeroPointer()
        if lightLeft > lightRight:
            touchyRobot.turnLeft(.25,300)
            touchyRobot.forward(.25,300)
        elif lightRight> lightLeft:
            touchyRobot.turnRight(.25,300)
            touchyRobot.forward(.25,300)
        elif lightRight == lightLeft:
            touchyRobot.turnRight(.25,500)
            
        else:
            touchyRobot.forward(.25,750)
        if touchyRobot.bttn.backspace:
            break

            


        
##    touchValues = touchyRobot.readTouch()
##    print("Reflection: ",touchyRobot.readReflect(),", Color: ",touchyRobot.readColor(),", Distance: ",touchyRobot.readDistance(),", Heading: ",touchyRobot.readHeading())
##    if touchValues == (False, False):
##        touchyRobot.forward(0.6, 2000)
##        print("going forward")
##    elif touchValues[1]:
##        touchyRobot.turnLeft(0.4, 0.75)
##    elif touchValues[0]:
##        touchyRobot.turnRight(0.4, 0.75)
##    else:
##        touchyRobot.backward(0.6, 0.75)


