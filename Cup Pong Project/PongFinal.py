from sturdystarter import SturdyBot
from ev3dev2.port import LegoPort
from ev3dev2.sensor import Sensor, INPUT_1
from smbus import SMBus
import time
import random
import ev3dev.ev3 as ev3


config = {SturdyBot.LEFT_MOTOR: 'outD',
       SturdyBot.RIGHT_MOTOR: 'outB',
       SturdyBot.SERVO_MOTOR: 'outD',
       SturdyBot.LEFT_TOUCH: 'in4',
       SturdyBot.RIGHT_TOUCH: 'in1',
       #SturdyBot.COLOR_SENSOR: 'in1',
       #SturdyBot.GYRO_SENSOR: 'in1',
       SturdyBot.ULTRA_SENSOR: 'in2'}
def shoot():
    Motor = ev3.LargeMotor('outC')
    Motor.run_timed(time_sp = 500,speed_sp = (Motor.max_speed * -1))
    time.sleep(2)
    Motor.run_timed(time_sp= 500, speed_sp = (Motor.max_speed * 1))
def detect(robot,dist,x,y,w,h):
    robot.stop()
    if(dist>88):
        robot.forward_forever(.15)
    if(dist<86):
        robot.forward_forever(-.15)
    if((dist>= 86 and dist<=88) and (x>=170 and x<=175) and (y>=125 and y <= 140)):
##        if ((h<=23 and h>=18) and (w>=22 and w<=26)):
            robot.stop()
            time.sleep(3)
            shoot()
            print("Baller : ", robot.readDistance())
            print("x: ",x,"y: ", y, "w: ",w , "h: ",h)
            input("ready? gimme ball! reset lock lozer! ")
        

robot = SturdyBot('Robot', config)

button = ev3.Button()

# Set LEGO port for Pixy2 on input port 1
in1 = LegoPort(INPUT_1)
in1.mode = 'other-i2c'
time.sleep(0.5)


# Settings for I2C (SMBus(3) for INPUT_1)
bus = SMBus(3)
address = 0x54

sigs = 1
data = [174, 193, 32, 2, sigs, 1]

bus.write_i2c_block_data(address, 0, data)
block = bus.read_i2c_block_data(address, 0, 20)


  




p = True
while p or not button.any():
  bus.write_i2c_block_data(address, 0, data)
  block = bus.read_i2c_block_data(address, 0, 20)

  sig = block[7]*256 + block[6]
  x = block[9]*256 + block[8]
  y = block[11]*256 + block[10]
  w = block[13]*256 + block[12]
  h = block[15]*256 + block[14]
  #i = input("enter x for shot")
  dist = robot.readDistance()
  print("Baller: ",dist)
  print("x: ",x,"y: ", y, "w: ",w , "h: ",h)
#  if ((dist>= 80 and dist<=85) and (h<=20 and h>=15) and (w>=20 and w<=22) and (x>=100 and x<=200) and (y>=125 and y <= 140)):

  if(x>175 and x<315):
    robot.turnRight(.08,100)
    time.sleep(1)
  elif (x<170):
    robot.turnLeft(.08,100)
    time.sleep(1)


  detect(robot,dist,x,y,w,h)
  

##  print("x: ",x,"y: ", y, "w: ",w , "h: ",h)
##  robot.forward_forever(.05)
##  if (w >= 37  and w <=  40) and (h >= 40 and h<= 43)  and (x >= 148 and x <= 151) and (y >= 131 and y <= 134):
##    robot.stop()
##    time.sleep(2)
##    shoot()
##    p = False

