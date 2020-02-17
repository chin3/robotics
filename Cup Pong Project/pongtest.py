import ev3dev.ev3 as ev3
import time
 
Motor = ev3.LargeMotor('outC')
Touch = ev3.TouchSensor('in4')


print("les go")

while True:
    Motor.run_timed(time_sp = 500,speed_sp = (Motor.max_speed * -1))
    time.sleep(2)
    Motor.run_timed(time_sp= 500, speed_sp = (Motor.max_speed * 1))
    input()
