
import ev3dev.ev3 as ev3
class SturdyRobot(object):
	def __init__(self, lmot, rmot, mmot):
		self.lmot = lmot
		self.rmot = rmot
		self.mmot = mmot
	def forward(self,speed, time = None):
		self.lmot.speed_sp = self.lmot.max_speed*speed
		self.rmot.speed_sp = self.rmot.max_speed*speed
#		self.lmot.run_timed(time_sp=time, speed_sp = self.lmot.speed_sp)
#		self.rmot.run_timed(time_sp=time, speed_sp = self.rmot.speed_sp)
		self.lmot.run_forever()
		self.rmot.run_forever()
#		self.lmot.wait_until_not_moving()
	def backward(self, speed,time = None):
		self.lmot.speed_sp = -(self.lmot.max_speed*speed)
		self.rmot.speed_sp = -(self.rmot.max_speed*speed)
		self.lmot.run_timed(time_sp=time, speed_sp = self.lmot.speed_sp)
		self.rmot.run_timed(time_sp=time, speed_sp = self.rmot.speed_sp)
		self.lmot.wait_until_not_moving()
	
	def turnLeft(self, speed, time= None):
		self.lmot.speed_sp = -self.lmot.max_speed*speed
		self.rmot.speed_sp = self.rmot.max_speed*speed
		self.lmot.run_timed(time_sp=time, speed_sp = self.lmot.speed_sp)
		self.rmot.run_timed(time_sp=time, speed_sp = self.rmot.speed_sp)
		self.lmot.wait_until_not_moving()

	def turnRight(self, speed, time= None):
		self.lmot.speed_sp = self.lmot.max_speed*speed
		self.rmot.speed_sp = -self.rmot.max_speed*speed
		self.lmot.run_timed(time_sp=time, speed_sp = self.lmot.speed_sp)
		self.rmot.run_timed(time_sp=time, speed_sp = self.rmot.speed_sp)
		self.lmot.wait_until_not_moving()
	def stop(self):
		self.lmot.stop(stop_action = 'hold')
		self.rmot.stop(stop_action = 'hold')
	def curve(self,leftSpeed,rightSpeed, time=None):
		self.lmot.speed_sp = self.lmot.max_speed*leftSpeed
		self.rmot.speed_sp = self.rmot.max_speed*rightSpeed
		self.lmot.run_timed(time_sp=time, speed_sp = self.lmot.speed_sp)
		self.rmot.run_timed(time_sp=time, speed_sp = self.rmot.speed_sp)
		self.lmot.wait_until_not_moving()
	def zeroPointer(self):
		self.mmot.position_sp = 0
		self.mmot.run_to_abs_pos(position_sp = self.mmot.position_sp)
		self.mmot.wait_until_not_moving()

	def leftPointer(self,speed = .25,time = None):

		self.mmot.speed_sp = -(speed*self.mmot.max_speed)
		self.mmot.run_timed(time_sp = time,speed_sp = self.mmot.speed_sp)
		self.mmot.wait_until_not_moving()

	def rightPointer(self,speed = .25, time = None):
		self.mmot.speed_sp = speed*self.mmot.max_speed
		self.mmot.run_timed(time_sp = time,speed_sp = self.mmot.speed_sp)
		self.mmot.wait_until_not_moving()

	def pointerTo(self,angle):
		self.mmot.position_sp = angle
		self.mmot.run_to_abs_pos(position_sp = self.mmot.position_sp)
		self.mmot.wait_until_not_moving()

	def speak(self, words):
		ev3.Sound.speak(words).wait()
	def beep(self):
		ev3.Sound.beep()

leftM = ev3.LargeMotor('outC')
rightM = ev3.LargeMotor('outB')
flatMot = ev3.MediumMotor('outD')
bttn = ev3.Button()

leftTouch = ev3.TouchSensor('in4')
rightTouch = ev3.TouchSensor('in1')
leftM.speed_sp = 200
rightM.speed_sp = 200


dakota = SturdyRobot(leftM,rightM,flatMot)
dakota.speak("luke sux")
dakota.beep()


while True:
	dakota.forward(.5)
	if bttn.backspace:
		break
	if rightTouch.is_pressed:
		ev3.Sound.speak("WAAAAAAAAAAAAAAAAAAAAAAAAAAAH")
		dakota.stop()
		dakota.backward(.5,1000)
		dakota.turnLeft(.5,300)


	elif leftTouch.is_pressed:
		ev3.Sound.speak("oof")
		dakota.stop()
		dakota.backward(.5,1000)
		dakota.turnRight(.5,300)


	elif rightTouch.is_pressed and rightTouch.is_pressed:
		ev3.Sound.speak("GET OUT OF MY WAY")
		dakota.stop()
		dakota.backward(.5,1000)
		dakota.turnRight(.5,750)





dakota.stop()